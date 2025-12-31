"""
K-Stay Internationalization (i18n) Module
다국어 지원을 위한 번역 유틸리티
"""

import json
import os
import streamlit as st
from functools import lru_cache
from typing import Optional

# 지원 언어
SUPPORTED_LANGUAGES = {
    "ko": "한국어",
    "en": "English"
}

DEFAULT_LANGUAGE = "ko"


@lru_cache(maxsize=10)
def load_translations(lang: str) -> dict:
    """번역 파일 로드 (캐싱 적용)"""
    # 프로젝트 루트 기준 경로
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locale_path = os.path.join(base_path, "locales", f"{lang}.json")
    
    try:
        with open(locale_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 언어로 폴백
        fallback_path = os.path.join(base_path, "locales", f"{DEFAULT_LANGUAGE}.json")
        try:
            with open(fallback_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    except json.JSONDecodeError:
        return {}


def get_current_language() -> str:
    """현재 선택된 언어 반환"""
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def set_language(lang: str):
    """언어 설정"""
    if lang in SUPPORTED_LANGUAGES:
        st.session_state.language = lang


def t(key: str, **kwargs) -> str:
    """
    번역 키로 텍스트 가져오기
    
    사용법:
        t("common.login")  # → "로그인" 또는 "Login"
        t("dashboard.welcome", name="John")  # → 변수 치환 지원
    
    Args:
        key: 점(.)으로 구분된 번역 키 (예: "common.login", "auth.email")
        **kwargs: 문자열 포맷팅을 위한 변수들
    
    Returns:
        번역된 문자열, 없으면 키 반환
    """
    lang = get_current_language()
    translations = load_translations(lang)
    
    # 점(.)으로 구분된 키를 따라 값 찾기
    keys = key.split(".")
    value = translations
    
    try:
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return key  # 키를 찾지 못함
        
        if value is None:
            return key
        
        # 변수 치환
        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value
        
        return value
        
    except (KeyError, TypeError):
        return key


def render_language_selector():
    """
    언어 선택 UI 렌더링 (페이지 상단용)
    버튼 스타일로 표시
    """
    current_lang = get_current_language()
    
    # 버튼 스타일 언어 선택기
    st.markdown("""
        <style>
        .lang-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            border: none;
        }
        .lang-btn-active {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white !important;
        }
        .lang-btn-inactive {
            background: #f1f5f9;
            color: #64748b !important;
        }
        .lang-btn-inactive:hover {
            background: #e2e8f0;
        }
        .lang-selector-container {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if current_lang == "ko":
            if st.button("🇰🇷 한국어", key="lang_ko", use_container_width=True, type="primary"):
                pass  # 이미 선택됨
        else:
            if st.button("🇰🇷 한국어", key="lang_ko", use_container_width=True):
                set_language("ko")
                st.rerun()
    
    with col2:
        if current_lang == "en":
            if st.button("🇺🇸 English", key="lang_en", use_container_width=True, type="primary"):
                pass  # 이미 선택됨
        else:
            if st.button("🇺🇸 English", key="lang_en", use_container_width=True):
                set_language("en")
                st.rerun()


def render_language_selector_minimal():
    """
    최소한의 언어 선택 UI (사이드바용)
    """
    current_lang = get_current_language()
    
    languages = list(SUPPORTED_LANGUAGES.values())
    current_index = 0 if current_lang == "ko" else 1
    
    selected = st.selectbox(
        "🌐",
        languages,
        index=current_index,
        key="lang_selector_minimal",
        label_visibility="collapsed"
    )
    
    new_lang = "ko" if selected == "한국어" else "en"
    if new_lang != current_lang:
        set_language(new_lang)
        st.rerun()


def get_language_display_name(lang_code: str) -> str:
    """언어 코드의 표시 이름 반환"""
    return SUPPORTED_LANGUAGES.get(lang_code, lang_code)


def init_language():
    """언어 초기화 (앱 시작 시 호출)"""
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
