"""
K-Stay Main Dashboard
시나리오 선택 및 메인 화면
"""

import streamlit as st
from config.settings import SCENARIOS
from services.payment_service import PaymentGateway


def render():
    """메인 대시보드 렌더링"""
    
    # 헤더
    render_header()
    
    # 시나리오 선택
    render_scenario_selection()
    
    # 최근 활동 (옵션)
    render_recent_activity()


def render_header():
    """헤더 섹션"""
    
    user_data = st.session_state.get('user_data', {})
    name = f"{user_data.get('given_name', 'Guest')}"
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(201,162,39,0.1) 0%, rgba(10,22,40,0.8) 100%);
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(201,162,39,0.2);
        ">
            <h1 style="
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                color: white;
                margin-bottom: 0.5rem;
            ">
                Welcome back, {name}! 👋
            </h1>
            <p style="
                color: #a0aec0;
                font-size: 1.1rem;
                margin-bottom: 1.5rem;
            ">
                어떤 비자 업무를 도와드릴까요?
            </p>
            <div style="
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
            ">
                <div style="
                    background: rgba(255,255,255,0.05);
                    padding: 0.8rem 1.5rem;
                    border-radius: 12px;
                    display: inline-block;
                ">
                    <span style="color: #6c757d;">국적</span>
                    <span style="color: white; margin-left: 0.5rem; font-weight: 600;">
                        {user_data.get('nationality', 'N/A')}
                    </span>
                </div>
                <div style="
                    background: rgba(255,255,255,0.05);
                    padding: 0.8rem 1.5rem;
                    border-radius: 12px;
                    display: inline-block;
                ">
                    <span style="color: #6c757d;">여권</span>
                    <span style="color: white; margin-left: 0.5rem; font-weight: 600;">
                        {user_data.get('passport_no', 'N/A')[:4]}****
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_scenario_selection():
    """시나리오 선택 섹션"""
    
    st.markdown("""
        <h2 style="
            font-family: 'Noto Sans KR', sans-serif;
            color: white;
            margin-bottom: 1.5rem;
        ">
            📋 시나리오 선택
        </h2>
    """, unsafe_allow_html=True)
    
    # Track 1: High Volume
    st.markdown("""
        <div style="
            display: inline-block;
            background: rgba(201,162,39,0.1);
            padding: 0.4rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <span style="
                color: #C9A227;
                font-size: 0.85rem;
                font-weight: 600;
                letter-spacing: 2px;
            ">💼 TRACK 1 — HIGH VOLUME</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_scenario_card("A")
    with col2:
        render_scenario_card("B")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 2: High Margin
    st.markdown("""
        <div style="
            display: inline-block;
            background: rgba(255,107,107,0.1);
            padding: 0.4rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <span style="
                color: #FF6B6B;
                font-size: 0.85rem;
                font-weight: 600;
                letter-spacing: 2px;
            ">💍 TRACK 2 — HIGH MARGIN</span>
        </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        render_scenario_card("C")
    with col4:
        render_scenario_card("D")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 3: Recurring
    st.markdown("""
        <div style="
            display: inline-block;
            background: rgba(102,126,234,0.1);
            padding: 0.4rem 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <span style="
                color: #667eea;
                font-size: 0.85rem;
                font-weight: 600;
                letter-spacing: 2px;
            ">🏛️ TRACK 3 — RECURRING</span>
        </div>
    """, unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    
    with col5:
        render_scenario_card("E")
    with col6:
        render_scenario_card("F")


def render_scenario_card(scenario_id: str):
    """시나리오 카드 렌더링"""
    
    scenario = SCENARIOS.get(scenario_id)
    if not scenario:
        return
    
    # 트랙별 색상
    track_colors = {
        "high_volume": ("#C9A227", "rgba(201,162,39,0.1)"),
        "high_margin": ("#FF6B6B", "rgba(255,107,107,0.1)"),
        "recurring": ("#667eea", "rgba(102,126,234,0.1)")
    }
    
    accent_color, bg_color = track_colors.get(scenario.track, ("#C9A227", "rgba(201,162,39,0.1)"))
    
    # 문서 수
    doc_count = len(scenario.required_docs)
    
    st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        " onmouseover="this.style.borderColor='{accent_color}'; this.style.transform='translateY(-4px)';"
           onmouseout="this.style.borderColor='rgba(201,162,39,0.15)'; this.style.transform='translateY(0)';">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{scenario.icon}</div>
            <h3 style="
                color: white;
                font-family: 'Noto Sans KR', sans-serif;
                font-weight: 700;
                margin-bottom: 0.3rem;
            ">{scenario.name}</h3>
            <p style="
                color: {accent_color};
                font-size: 0.85rem;
                margin-bottom: 0.5rem;
            ">{scenario.visa_type}</p>
            <p style="
                color: #8892a0;
                font-size: 0.9rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            ">{scenario.description}</p>
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <span style="
                    background: {bg_color};
                    color: {accent_color};
                    padding: 0.3rem 0.8rem;
                    border-radius: 20px;
                    font-size: 0.75rem;
                ">📄 {doc_count}개 문서</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"시작하기 →", key=f"start_{scenario_id}", use_container_width=True):
        # 결제 확인
        if not st.session_state.get('is_paid', False) and not st.session_state.get('is_admin', False):
            st.warning("이 기능을 사용하려면 Premium 구매가 필요합니다.")
            PaymentGateway.render_payment_modal()
            return
        
        # 시나리오 선택 및 폼 페이지로 이동
        st.session_state.selected_scenario = scenario_id
        st.session_state.current_page = 'scenario_form'
        st.rerun()


def render_recent_activity():
    """최근 활동 섹션"""
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <h3 style="
            font-family: 'Noto Sans KR', sans-serif;
            color: #a0aec0;
            margin-bottom: 1rem;
        ">
            📊 최근 활동
        </h3>
    """, unsafe_allow_html=True)
    
    # 최근 생성된 문서가 있는 경우
    generated_docs = st.session_state.get('generated_documents', [])
    
    if generated_docs:
        for doc in generated_docs[-3:]:  # 최근 3개만
            st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.02);
                    border-left: 3px solid #C9A227;
                    padding: 1rem;
                    margin-bottom: 0.5rem;
                    border-radius: 0 8px 8px 0;
                ">
                    <p style="color: white; margin: 0;">{doc.get('name', 'Document')}</p>
                    <p style="color: #6c757d; font-size: 0.8rem; margin: 0;">
                        {doc.get('created_at', 'N/A')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                background: rgba(255,255,255,0.02);
                border: 1px dashed rgba(201,162,39,0.3);
                border-radius: 12px;
                padding: 2rem;
                text-align: center;
            ">
                <p style="color: #6c757d; margin: 0;">
                    아직 생성된 문서가 없습니다.<br>
                    위에서 시나리오를 선택하여 시작하세요!
                </p>
            </div>
        """, unsafe_allow_html=True)


def render_stats_banner():
    """통계 배너"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("📄", "생성된 문서", st.session_state.get('total_docs', 0)),
        ("✅", "완료된 신청", st.session_state.get('completed', 0)),
        ("💬", "AI 상담", st.session_state.get('ai_chats', 0)),
        ("⭐", "성공률", "98%")
    ]
    
    for col, (icon, label, value) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.02);
                    border: 1px solid rgba(201,162,39,0.1);
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="color: white; font-size: 1.5rem; font-weight: 700;">
                        {value}
                    </div>
                    <div style="color: #6c757d; font-size: 0.8rem;">{label}</div>
                </div>
            """, unsafe_allow_html=True)
