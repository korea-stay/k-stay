"""
K-Stay LLM Client
Google Gemini API 공통 래퍼 (OpenAI → Gemini 전환)

- chat(): OpenAI 스타일 messages([{"role", "content"}])를 받아 Gemini로 호출
- embed(): 텍스트 목록 임베딩 (기본 1536차원 → 기존 VECTOR(1536) 스키마 유지)
"""

import os
import math
import time
from dataclasses import dataclass
from typing import List, Dict, Optional

from google import genai
from google.genai import errors, types

try:
    import streamlit as st
    USE_STREAMLIT = True
except ImportError:
    USE_STREAMLIT = False


def get_secret(key: str, default: str = None) -> str:
    """환경변수 또는 Streamlit secrets에서 값 가져오기"""
    if USE_STREAMLIT:
        try:
            return st.secrets.get(key, os.getenv(key, default))
        except Exception:
            return os.getenv(key, default)
    return os.getenv(key, default)


DEFAULT_CHAT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"
DEFAULT_EMBEDDING_DIM = 1536

# Gemini 3.x는 thinking 토큰도 max_output_tokens에 포함되므로 여유분을 더해줌
THINKING_HEADROOM_TOKENS = 1024
# gemini-embedding-001 요청당 최대 입력 수
EMBED_BATCH_LIMIT = 100
# 429(요청 한도 초과) 재시도 설정
EMBED_MAX_RETRIES = 5
EMBED_RETRY_WAIT_SECONDS = 60


@dataclass
class ChatResult:
    """채팅 응답"""
    text: str
    total_tokens: int
    prompt_tokens: int = 0   # 입력 토큰
    output_tokens: int = 0   # 출력 토큰 (답변, thinking 제외)
    thought_tokens: int = 0  # thinking 토큰


class GeminiClient:
    """Gemini 채팅/임베딩 클라이언트"""

    def __init__(
        self,
        api_key: str = None,
        chat_model: str = None,
        embedding_model: str = None,
        embedding_dim: int = None,
        thinking_level: str = None
    ):
        api_key = api_key or get_secret("GEMINI_API_KEY") or get_secret("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

        self.client = genai.Client(api_key=api_key)
        self.chat_model = chat_model or get_secret("GEMINI_CHAT_MODEL", DEFAULT_CHAT_MODEL)
        self.embedding_model = embedding_model or get_secret("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
        self.embedding_dim = embedding_dim or DEFAULT_EMBEDDING_DIM
        # "low" | "medium" | "high", 빈 문자열이면 모델 기본값 사용
        self.thinking_level = thinking_level if thinking_level is not None else get_secret("GEMINI_THINKING_LEVEL", "low")

    # ==================== 채팅 ====================

    def chat(
        self,
        messages: List[Dict],
        temperature: float = None,
        max_tokens: int = None,
        json_mode: bool = False
    ) -> ChatResult:
        """OpenAI 스타일 messages로 Gemini 응답 생성"""
        system_instruction, contents = self._convert_messages(messages)

        # 함수 호출을 쓰지 않으므로 AFC 비활성화 (SDK 경고 방지)
        config_kwargs = {
            "automatic_function_calling": types.AutomaticFunctionCallingConfig(disable=True)
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if temperature is not None:
            config_kwargs["temperature"] = temperature
        if max_tokens is not None:
            config_kwargs["max_output_tokens"] = max_tokens + THINKING_HEADROOM_TOKENS
        if json_mode:
            config_kwargs["response_mime_type"] = "application/json"

        thinking_config = self._build_thinking_config()
        if thinking_config is not None:
            try:
                return self._generate(contents, {**config_kwargs, "thinking_config": thinking_config})
            except Exception as e:
                # thinking_level을 지원하지 않는 모델이면 기본 설정으로 재시도
                print(f"  ⚠️ thinking_config 적용 실패, 기본 설정으로 재시도: {e}")

        return self._generate(contents, config_kwargs)

    def _generate(self, contents: List[types.Content], config_kwargs: Dict) -> ChatResult:
        response = self.client.models.generate_content(
            model=self.chat_model,
            contents=contents,
            config=types.GenerateContentConfig(**config_kwargs)
        )
        usage = response.usage_metadata
        return ChatResult(
            text=response.text or "",
            total_tokens=(usage.total_token_count or 0) if usage else 0,
            prompt_tokens=(usage.prompt_token_count or 0) if usage else 0,
            output_tokens=(usage.candidates_token_count or 0) if usage else 0,
            thought_tokens=(usage.thoughts_token_count or 0) if usage else 0
        )

    def _build_thinking_config(self) -> Optional[types.ThinkingConfig]:
        if not self.thinking_level:
            return None
        try:
            return types.ThinkingConfig(thinking_level=self.thinking_level.upper())
        except Exception:
            # 구버전 SDK는 thinking_level 미지원
            return None

    def _convert_messages(self, messages: List[Dict]):
        """OpenAI messages → (system_instruction, Gemini contents)"""
        system_parts = []
        contents = []
        for msg in messages:
            role = msg.get("role")
            text = msg.get("content") or ""
            if role == "system":
                system_parts.append(text)
                continue
            gemini_role = "model" if role == "assistant" else "user"
            contents.append(types.Content(role=gemini_role, parts=[types.Part(text=text)]))
        system_instruction = "\n\n".join(system_parts) if system_parts else None
        return system_instruction, contents

    # ==================== 임베딩 ====================

    def embed(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """텍스트 목록 임베딩 (task_type: RETRIEVAL_DOCUMENT | RETRIEVAL_QUERY 등)"""
        embeddings = []
        for i in range(0, len(texts), EMBED_BATCH_LIMIT):
            batch = texts[i:i + EMBED_BATCH_LIMIT]
            result = self._embed_with_retry(batch, task_type)
            embeddings.extend(self._normalize(e.values) for e in result.embeddings)
        return embeddings

    def _embed_with_retry(self, batch: List[str], task_type: str):
        """429(요청 한도 초과) 시 대기 후 재시도 - 무료 티어는 분당 100건 제한"""
        for attempt in range(EMBED_MAX_RETRIES + 1):
            try:
                return self.client.models.embed_content(
                    model=self.embedding_model,
                    contents=batch,
                    config=types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=self.embedding_dim
                    )
                )
            except errors.APIError as e:
                # 일일 한도(PerDay) 초과는 기다려도 풀리지 않으므로 바로 실패
                if e.code != 429 or "PerDay" in str(e) or attempt == EMBED_MAX_RETRIES:
                    raise
                print(f"  ⏳ 임베딩 요청 한도 초과, {EMBED_RETRY_WAIT_SECONDS}초 후 재시도 ({attempt + 1}/{EMBED_MAX_RETRIES})")
                time.sleep(EMBED_RETRY_WAIT_SECONDS)

    @staticmethod
    def _normalize(vector: List[float]) -> List[float]:
        """gemini-embedding-001은 3072 미만 차원일 때 직접 정규화 필요"""
        norm = math.sqrt(sum(v * v for v in vector))
        return [v / norm for v in vector] if norm else list(vector)
