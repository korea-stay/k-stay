"""
K-Stay Main Dashboard
결제 없이 시나리오 시작 가능, Phase 4에서 결제
"""

import streamlit as st
from services.payment_service import PaymentService


def render():
    """메인 대시보드 렌더링"""
    
    # 결제 콜백 처리
    handle_payment_callback()
    
    user_data = st.session_state.get('user_data', {})
    name = user_data.get('given_name', 'Guest')
    nationality = user_data.get('nationality', '')
    passport = user_data.get('passport_no', '')
    passport_masked = passport[:3] + '****' if passport else ''
    
    # 환영 배너
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
        ">
            <h1 style="font-size: 2rem; font-weight: 700; color: white !important; margin: 0 0 0.5rem 0;">
                Welcome back, {name}! 👋
            </h1>
            <p style="color: rgba(255,255,255,0.9) !important; font-size: 1rem; margin: 0 0 1rem 0;">
                어떤 비자 업무를 도와드릴까요?
            </p>
            <div style="display: flex; gap: 2rem;">
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">국적: <b style="color: white;">{nationality}</b></span>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">여권: <b style="color: white;">{passport_masked}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 결제 상태 표시
    is_paid = st.session_state.get('is_paid', False)
    if is_paid:
        st.success("✅ Premium 활성화됨 - 모든 기능 이용 가능")
    else:
        st.info("💡 시나리오를 먼저 진행하고, 문서 생성 전에 결제하실 수 있습니다.")
    
    render_scenario_list()


def handle_payment_callback():
    """URL 파라미터로 결제 결과 처리"""
    params = st.query_params
    
    if params.get("payment") == "success":
        session_id = params.get("session_id", "")
        payment_service = PaymentService()
        
        success, info = payment_service.verify_payment(session_id)
        if success:
            user_id = st.session_state.get('user_id', '')
            payment_service.record_payment_to_db(user_id, info)
            st.success("🎉 결제가 완료되었습니다! Premium 기능을 이용하실 수 있습니다.")
            st.balloons()
        
        st.query_params.clear()
    
    elif params.get("payment") == "cancel":
        st.warning("결제가 취소되었습니다.")
        st.query_params.clear()


def render_scenario_list():
    """시나리오 목록 렌더링"""
    
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin: 1.5rem 0;">
            <span style="font-size: 1.5rem;">📋</span>
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #1e293b !important; margin: 0;">
                시나리오 선택
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Track 1
    st.markdown('<div style="background: #f1f5f9; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #475569;">💼 TRACK 1 — HIGH VOLUME</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        render_scenario_card("💼", "#fef3c7", "구직 준비", "D-10", "구직 활동을 위한 비자 연장", 5, "A")
    with col2:
        render_scenario_card("⏰", "#fce7f3", "아르바이트", "시간제 취업", "유학생 시간제 취업 허가", 5, "B")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 2
    st.markdown('<div style="background: #fef3c7; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #92400e;">💎 TRACK 2 — HIGH MARGIN</span></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        render_scenario_card("💍", "#fce7f3", "결혼 이민", "F-6", "결혼을 통한 비자 신청", 5, "C")
    with col4:
        render_scenario_card("👨‍👩‍👧", "#d1fae5", "가족 초청", "F-1-5", "부모님 방문 초청장 발급", 4, "D")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 3
    st.markdown('<div style="background: #e0e7ff; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #3730a3;">🔄 TRACK 3 — RECURRING</span></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        render_scenario_card("🎓", "#e0e7ff", "전문 인력", "E-7", "전문 인력 비자 신청", 3, "E")
    with col6:
        render_scenario_card("🏛️", "#fef3c7", "국적 귀화", "귀화", "대한민국 국적 취득", 4, "F")


def render_scenario_card(icon, icon_bg, title, visa_type, description, doc_count, key):
    """시나리오 카드"""
    
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 0.5rem;
        ">
            <div style="width: 40px; height: 40px; background: {icon_bg}; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 0.75rem;">{icon}</div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">{title}</h3>
            <p style="font-size: 0.8rem; color: #2563eb; margin: 0 0 0.5rem 0; font-weight: 500;">{visa_type}</p>
            <p style="font-size: 0.85rem; color: #64748b; margin: 0 0 0.75rem 0;">{description}</p>
            <div style="display: inline-block; background: #dbeafe; color: #1e40af; font-size: 0.75rem; font-weight: 500; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">📄 {doc_count}개 문서</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🚀 시작하기", key=f"start_{key}", use_container_width=True, type="primary"):
        start_scenario(key)


def start_scenario(scenario_id: str):
    """시나리오 시작 - 결제 없이 바로 시작"""
    st.session_state.selected_scenario = scenario_id
    st.session_state.current_page = 'scenario_form'
    st.session_state.form_step = 1
    st.rerun()
