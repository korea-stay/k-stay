"""
K-Stay Main Dashboard
Light Mode Compatible - Fixed card layout and spacing
"""

import streamlit as st
from config.settings import SCENARIOS
from services.payment_service import PaymentGateway


def render():
    """메인 대시보드 렌더링"""
    
    user_data = st.session_state.get('user_data', {})
    name = f"{user_data.get('given_name', 'Guest')}"
    nationality = user_data.get('nationality', '')
    passport = user_data.get('passport_no', '')
    passport_masked = passport[:3] + '****' if passport else ''
    
    # 환영 배너 (밝은 파란색 그라데이션)
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
        ">
            <h1 style="
                font-size: 2rem;
                font-weight: 700;
                color: white !important;
                margin: 0 0 0.5rem 0;
            ">Welcome back, {name}! 👋</h1>
            <p style="
                color: rgba(255,255,255,0.9) !important;
                font-size: 1rem;
                margin: 0 0 1.5rem 0;
            ">어떤 비자 업무를 도와드릴까요?</p>
            <div style="display: flex; gap: 2rem;">
                <div>
                    <span style="color: rgba(255,255,255,0.7) !important; font-size: 0.85rem;">국적</span>
                    <span style="color: white !important; font-weight: 600; margin-left: 0.5rem;">{nationality}</span>
                </div>
                <div>
                    <span style="color: rgba(255,255,255,0.7) !important; font-size: 0.85rem;">여권</span>
                    <span style="color: white !important; font-weight: 600; margin-left: 0.5rem;">{passport_masked}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 시나리오 선택 섹션
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
            <span style="font-size: 1.5rem;">📋</span>
            <h2 style="
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e293b !important;
                margin: 0;
            ">시나리오 선택</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Track 1 - High Volume
    st.markdown("""
        <div style="
            background: #f1f5f9;
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 0.375rem;
            margin-bottom: 1rem;
        ">
            <span style="font-size: 0.8rem; font-weight: 600; color: #475569 !important;">
                💼 TRACK 1 — HIGH VOLUME
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_scenario_card(
            icon="💼",
            icon_bg="#fef3c7",
            title="구직 준비",
            visa_type="D-10",
            description="구직 활동을 위한 비자 연장 및 체류자격 변경",
            doc_count=5,
            key="A"
        )
    
    with col2:
        render_scenario_card(
            icon="⏰",
            icon_bg="#fce7f3",
            title="아르바이트",
            visa_type="시간제 취업",
            description="유학생/연수생 시간제 취업 허가 신청",
            doc_count=5,
            key="B"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 2 - High Margin
    st.markdown("""
        <div style="
            background: #fef3c7;
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 0.375rem;
            margin-bottom: 1rem;
        ">
            <span style="font-size: 0.8rem; font-weight: 600; color: #92400e !important;">
                💎 TRACK 2 — HIGH MARGIN
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        render_scenario_card(
            icon="💍",
            icon_bg="#fce7f3",
            title="결혼 이민",
            visa_type="F-6",
            description="한국인 배우자와의 결혼을 통한 비자 신청",
            doc_count=5,
            key="C"
        )
    
    with col4:
        render_scenario_card(
            icon="👨‍👩‍👧",
            icon_bg="#d1fae5",
            title="가족 초청",
            visa_type="F-1-5",
            description="부모님 방문/체류를 위한 초청장 발급",
            doc_count=4,
            key="D"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 3 - Recurring
    st.markdown("""
        <div style="
            background: #e0e7ff;
            display: inline-block;
            padding: 0.375rem 0.75rem;
            border-radius: 0.375rem;
            margin-bottom: 1rem;
        ">
            <span style="font-size: 0.8rem; font-weight: 600; color: #3730a3 !important;">
                🔄 TRACK 3 — RECURRING
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        render_scenario_card(
            icon="🎓",
            icon_bg="#e0e7ff",
            title="전문 인력",
            visa_type="E-7",
            description="특정 분야 전문 인력 채용을 위한 비자 신청",
            doc_count=3,
            key="E"
        )
    
    with col6:
        render_scenario_card(
            icon="🏛️",
            icon_bg="#fef3c7",
            title="국적 귀화",
            visa_type="귀화",
            description="대한민국 국적 취득을 위한 귀화 신청",
            doc_count=4,
            key="F"
        )


def render_scenario_card(icon, icon_bg, title, visa_type, description, doc_count, key):
    """시나리오 카드 렌더링"""
    
    # 카드 컨테이너
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 0.5rem;
        ">
            <div style="
                width: 40px;
                height: 40px;
                background: {icon_bg};
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
                margin-bottom: 0.75rem;
            ">{icon}</div>
            <h3 style="
                font-size: 1.1rem;
                font-weight: 700;
                color: #1e293b !important;
                margin: 0 0 0.25rem 0;
            ">{title}</h3>
            <p style="
                font-size: 0.8rem;
                color: #2563eb !important;
                margin: 0 0 0.5rem 0;
                font-weight: 500;
            ">{visa_type}</p>
            <p style="
                font-size: 0.85rem;
                color: #64748b !important;
                margin: 0 0 0.75rem 0;
                line-height: 1.4;
            ">{description}</p>
            <div style="
                display: inline-block;
                background: #dbeafe;
                color: #1e40af !important;
                font-size: 0.75rem;
                font-weight: 500;
                padding: 0.25rem 0.5rem;
                border-radius: 0.25rem;
            ">📄 {doc_count}개 문서</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 시작하기 버튼 (카드 밖, 바로 아래)
    if st.button(f"🚀 시작하기", key=f"start_{key}", use_container_width=True, type="primary"):
        start_scenario(key)


def start_scenario(scenario_id: str):
    """시나리오 시작"""
    if not st.session_state.get('is_paid', False) and not st.session_state.get('is_admin', False):
        st.warning("이 기능을 사용하려면 Premium 구매가 필요합니다.")
        return
    
    st.session_state.selected_scenario = scenario_id
    st.session_state.current_page = 'scenario_form'
    st.session_state.form_step = 1  # Phase 1 (Universal Fact 확인)부터 시작
    st.rerun()
