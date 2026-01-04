"""
AI Review Service for K-Stay Narrative Fields
OpenAI GPT API를 활용한 서술형 답변 검토 서비스

변경사항:
- 병렬 처리(ThreadPoolExecutor) 도입으로 검토 속도 대폭 개선
- 항목별 개별 API 호출로 독립성 및 정밀도 향상
"""

import os
import json
import time
import hashlib
import streamlit as st
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed


class ReviewType(Enum):
    """검토 결과 유형 - 3단계 위험 척도"""
    DANGER = "danger"      # 🔴 위험 - 수정 필요
    CAUTION = "caution"    # 🟡 주의 - 보완 권장
    GOOD = "good"          # 🟢 양호 - 문제 없음
    PENDING = "pending"    # ⚪ 대기 - 검토 전


@dataclass
class ReviewFeedback:
    """개별 필드 검토 결과"""
    field_key: str
    field_label: str
    field_label_en: str
    review_type: ReviewType
    message: str
    message_en: str
    suggestions: List[str] = field(default_factory=list)
    suggestions_en: List[str] = field(default_factory=list)


@dataclass
class OverallReview:
    """전체 검토 결과"""
    scenario_id: str
    overall_status: ReviewType
    feedbacks: List[ReviewFeedback]
    overall_message: str
    overall_message_en: str
    reviewed_at: str
    is_ai_review: bool = True  # 항상 AI 검토


class AIReviewService:
    """OpenAI GPT 기반 서술형 검토 서비스 (AI 전용)"""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        # 속도와 비용을 고려하여 gpt-4o-mini 권장 (존재하지 않는 모델명일 경우 에러 발생 가능하므로 수정)
        self.model = "gpt-4o-mini" 
        self._cache = {}
        self._client = None
        
    def _get_api_key(self) -> str:
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                return st.secrets['OPENAI_API_KEY']
        except Exception:
            pass
        return os.getenv('OPENAI_API_KEY', '')
    
    def _get_client(self):
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except Exception:
                return None
        return self._client
        
    def is_api_available(self) -> bool:
        return bool(self.api_key)
    
    def _get_cache_key(self, scenario_id: str, narrative_data: Dict) -> str:
        content = json.dumps(narrative_data, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(f"{scenario_id}:{content}".encode()).hexdigest()
    
    def review_narratives(
        self,
        scenario_id: str,
        narrative_data: Dict[str, str],
        narrative_config: Dict,
        force_refresh: bool = False
    ) -> Optional[OverallReview]:
        """
        서술형 내용 AI 검토 (병렬 처리 적용)
        """
        if not self.is_api_available():
            return None
        
        # 캐시 확인 (5분)
        cache_key = self._get_cache_key(scenario_id, narrative_data)
        if not force_refresh and cache_key in self._cache:
            cached = self._cache[cache_key]
            if time.time() - cached['time'] < 300:
                return cached['result']
        
        fields = narrative_config.get('fields', [])
        danger_patterns = narrative_config.get('danger_patterns', [])
        validation_prompt = narrative_config.get('validation_prompt', '')
        
        # [변경] 병렬 검토 수행
        feedbacks = self._ai_review_parallel(
            scenario_id, narrative_data, fields, 
            danger_patterns, validation_prompt
        )
        
        if not feedbacks:
            return None
        
        # 전체 상태 결정
        overall_status = self._determine_overall_status(feedbacks)
        overall_msg, overall_msg_en = self._generate_overall_message(overall_status, feedbacks)
        
        result = OverallReview(
            scenario_id=scenario_id,
            overall_status=overall_status,
            feedbacks=feedbacks,
            overall_message=overall_msg,
            overall_message_en=overall_msg_en,
            reviewed_at=time.strftime('%Y-%m-%d %H:%M:%S'),
            is_ai_review=True
        )
        
        self._cache[cache_key] = {'result': result, 'time': time.time()}
        return result
    
    def _ai_review_parallel(
        self,
        scenario_id: str,
        narrative_data: Dict[str, str],
        fields: List[Dict],
        danger_patterns: List[str],
        validation_prompt: str
    ) -> List[ReviewFeedback]:
        """
        [NEW] ThreadPoolExecutor를 사용한 병렬 검토 로직
        여러 항목을 동시에 API 호출하여 속도를 대폭 개선함
        """
        feedbacks = []
        
        # 검토 대상 필드 준비
        target_fields = []
        for field in fields:
            # 모든 필드를 검토 대상으로 함 (미작성 필드도 '미작성' 상태로 검토)
            target_fields.append(field)

        # 최대 5개의 병렬 스레드로 실행 (Rate Limit 고려)
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_field = {
                executor.submit(
                    self._review_single_field, 
                    scenario_id, narrative_data, field, 
                    danger_patterns, validation_prompt
                ): field for field in target_fields
            }
            
            for future in as_completed(future_to_field):
                field = future_to_field[future]
                try:
                    feedback = future.result()
                    if feedback:
                        feedbacks.append(feedback)
                except Exception as e:
                    print(f"Error reviewing field {field['data_key']}: {e}")
        
        # 결과를 원래 필드 순서대로 정렬
        field_order = {f['data_key']: i for i, f in enumerate(fields)}
        feedbacks.sort(key=lambda x: field_order.get(x.field_key, 999))
        
        return feedbacks

    def _review_single_field(
        self,
        scenario_id: str,
        narrative_data: Dict[str, str],
        field_info: Dict,
        danger_patterns: List[str],
        validation_prompt: str
    ) -> Optional[ReviewFeedback]:
        """[NEW] 단일 필드 검토 (개별 API 호출용)"""
        client = self._get_client()
        if not client:
            return None
            
        data_key = field_info['data_key']
        label = field_info.get('label', data_key)
        label_en = field_info.get('label_en', label)
        min_chars = field_info.get('min_chars', 50)
        required = field_info.get('required', False)
        answer = narrative_data.get(data_key, '').strip()
        
        # 시나리오 컨텍스트 가져오기
        scenario_context = self._get_scenario_context(scenario_id)
        
        system_prompt = f"""당신은 한국 출입국관리사무소 서류 심사 전문가입니다.
신청자가 작성한 비자 신청서의 특정 항목을 심사관 관점에서 엄격하게 검토하세요.

## 시나리오: {scenario_context}
## 검토 항목: {label} ({label_en})
## 필수 여부: {'필수' if required else '선택'}
## 최소 글자수: {min_chars}자

## 검토 기준
{validation_prompt}

## 위험 표현 (포함 시 즉시 danger)
{', '.join(danger_patterns) if danger_patterns else '없음'}

## 평가 3단계
1. 🔴 danger: 미작성(필수일 때), 최소분량 미달, 위험 표현 포함, 내용이 매우 부실함
2. 🟡 caution: 글자수는 충족하나 구체성이 부족하거나 표현이 어색함
3. 🟢 good: 구체적이고 논리적이며 설득력 있음

## 출력 형식 (JSON Only)
{{
    "status": "danger|caution|good",
    "message_ko": "구체적인 한국어 피드백 (한 문장)",
    "message_en": "Specific feedback in English (one sentence)",
    "suggestions_ko": ["제안1", "제안2"],
    "suggestions_en": ["Suggestion 1", "Suggestion 2"]
}}
"""
        user_content = f"작성 내용:\n{answer if answer else '(미작성)'}\n\n현재 글자수: {len(answer)}자"

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            status_map = {
                'danger': ReviewType.DANGER,
                'caution': ReviewType.CAUTION,
                'good': ReviewType.GOOD
            }
            review_type = status_map.get(result.get('status'), ReviewType.CAUTION)
            
            return ReviewFeedback(
                field_key=data_key,
                field_label=label,
                field_label_en=label_en,
                review_type=review_type,
                message=result.get('message_ko', ''),
                message_en=result.get('message_en', ''),
                suggestions=result.get('suggestions_ko', []),
                suggestions_en=result.get('suggestions_en', [])
            )
            
        except Exception as e:
            print(f"Single field review error ({data_key}): {e}")
            return None

    def _determine_overall_status(self, feedbacks: List[ReviewFeedback]) -> ReviewType:
        """전체 상태 결정"""
        danger_count = sum(1 for fb in feedbacks if fb.review_type == ReviewType.DANGER)
        caution_count = sum(1 for fb in feedbacks if fb.review_type == ReviewType.CAUTION)
        
        if danger_count > 0:
            return ReviewType.DANGER
        elif caution_count > 0:
            return ReviewType.CAUTION
        else:
            return ReviewType.GOOD
    
    def _generate_overall_message(self, status: ReviewType, feedbacks: List[ReviewFeedback]) -> Tuple[str, str]:
        """전체 평가 메시지 생성"""
        danger_count = sum(1 for fb in feedbacks if fb.review_type == ReviewType.DANGER)
        caution_count = sum(1 for fb in feedbacks if fb.review_type == ReviewType.CAUTION)
        good_count = sum(1 for fb in feedbacks if fb.review_type == ReviewType.GOOD)
        
        if status == ReviewType.GOOD:
            return (
                f"✅ 모든 항목이 양호합니다! ({good_count}개 항목 통과)",
                f"✅ All items look good! ({good_count} items passed)"
            )
        elif status == ReviewType.CAUTION:
            return (
                f"⚠️ {caution_count}개 항목 보완 권장 (양호: {good_count}개)",
                f"⚠️ {caution_count} items need attention ({good_count} good)"
            )
        else:
            return (
                f"🚨 {danger_count}개 항목 수정 필요 (주의: {caution_count}개)",
                f"🚨 {danger_count} items require revision ({caution_count} caution)"
            )
    
    def get_field_status_for_display(
        self, 
        field_key: str, 
        review_result: Optional[OverallReview]
    ) -> Tuple[str, str, str, str]:
        """필드별 표시용 상태 반환"""
        default = ('⚪', '#6b7280', '#f9fafb', '검토 대기')
        
        if not review_result:
            return default
        
        for fb in review_result.feedbacks:
            if fb.field_key == field_key:
                status_map = {
                    ReviewType.DANGER: ('🔴', '#ef4444', '#fef2f2', '위험'),
                    ReviewType.CAUTION: ('🟡', '#f59e0b', '#fffbeb', '주의'),
                    ReviewType.GOOD: ('🟢', '#22c55e', '#f0fdf4', '양호'),
                    ReviewType.PENDING: ('⚪', '#6b7280', '#f9fafb', '대기'),
                }
                return status_map.get(fb.review_type, default)
        
        return default

    def _get_scenario_context(self, scenario_id: str) -> str:
        """시나리오 ID에 따른 컨텍스트 반환"""
        return {
            "A": "구직 비자(D-10) 연장/변경. 구직 계획의 구체성과 실현 가능성 중점.",
            "B": "시간제 취업 허가. 학업과 아르바이트의 균형, 불법 취업 방지 중점.",
            "C": "결혼 이민(F-6). 혼인의 진정성, 의사소통 능력 중점.",
            "D": "가족 초청(F-1-5). 초청 사유 타당성, 불법체류 가능성 배제.",
            "E": "전문 인력(E-7). 전문성 입증, 국민 고용 침해 여부 확인.",
            "F": "귀화 신청. 정착 의지, 품행 단정, 생계 유지 능력.",
            "G": "의료 목적. 치료 필요성, 병원 예약 사실 확인.",
        }.get(scenario_id, "비자 신청 서류 심사")


# 싱글톤 인스턴스
_instance = None

def get_ai_review_service() -> AIReviewService:
    global _instance
    if _instance is None:
        _instance = AIReviewService()
    return _instance