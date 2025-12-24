"""
🇰🇷 K-Stay: Korea Stay Assistant
외국인을 위한 출입국 민원 서류 자동 생성 플랫폼
"""

import streamlit as st
from config.settings import init_page_config, init_session_state
from services.auth_service import AuthService
from services.payment_service import PaymentService
from pages import login, signup, main_dashboard, scenario_form, ai_chat, document_preview

# 페이지 설정
init_page_config()

# 세션 상태 초기화
init_session_state()

# CSS 스타일 적용
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Playfair+Display:wght@400;600;700&display=swap');
    
    :root {
        --primary-navy: #0A1628;
        --accent-gold: #C9A227;
        --accent-coral: #FF6B6B;
        --soft-cream: #FDF6E3;
        --text-dark: #1a1a2e;
        --text-light: #f8f9fa;
        --gradient-blue: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-gold: linear-gradient(135deg, #C9A227 0%, #E8D5A3 50%, #C9A227 100%);
    }
    
    .stApp {
        background: linear-gradient(180deg, #0A1628 0%, #1a2744 50%, #0A1628 100%);
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        background: var(--gradient-gold);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: 2px;
    }
    
    .sub-title {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 1.2rem;
        color: #a0aec0;
        text-align: center;
        margin-top: 0.5rem;
        letter-spacing: 4px;
    }
    
    /* 카드 스타일 */
    .scenario-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(201, 162, 39, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(10px);
    }
    
    .scenario-card:hover {
        transform: translateY(-8px);
        border-color: var(--accent-gold);
        box-shadow: 0 20px 40px rgba(201, 162, 39, 0.15);
    }
    
    .scenario-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .scenario-title {
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        color: var(--text-light);
        margin-bottom: 0.5rem;
    }
    
    .scenario-desc {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        color: #8892a0;
        line-height: 1.6;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 500;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .gold-button {
        background: var(--gradient-gold) !important;
        color: var(--primary-navy) !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    .gold-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(201, 162, 39, 0.4);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(201, 162, 39, 0.3);
        border-radius: 10px;
        color: var(--text-light);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-gold);
        box-shadow: 0 0 20px rgba(201, 162, 39, 0.2);
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
        border-right: 1px solid rgba(201, 162, 39, 0.2);
    }
    
    /* 진행 상태 표시 */
    .progress-step {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .progress-step.active {
        background: rgba(201, 162, 39, 0.1);
        border-left: 3px solid var(--accent-gold);
    }
    
    .progress-step.completed {
        opacity: 0.6;
    }
    
    .step-number {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .step-number.active {
        background: var(--accent-gold);
        color: var(--primary-navy);
    }
    
    .step-number.pending {
        background: rgba(255, 255, 255, 0.1);
        color: #6c757d;
    }
    
    /* 폼 컨테이너 */
    .form-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(201, 162, 39, 0.15);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
    }
    
    .form-section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: var(--accent-gold);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(201, 162, 39, 0.3);
    }
    
    /* 채팅 스타일 */
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: fadeIn 0.3s ease;
    }
    
    .chat-message.user {
        background: rgba(201, 162, 39, 0.1);
        border: 1px solid rgba(201, 162, 39, 0.3);
        margin-left: 2rem;
    }
    
    .chat-message.assistant {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-right: 2rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 다운로드 버튼 */
    .download-section {
        background: linear-gradient(135deg, rgba(201, 162, 39, 0.1) 0%, rgba(201, 162, 39, 0.05) 100%);
        border: 2px solid var(--accent-gold);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* 알림 배지 */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .badge-premium {
        background: var(--gradient-gold);
        color: var(--primary-navy);
    }
    
    .badge-free {
        background: rgba(255, 255, 255, 0.1);
        color: #a0aec0;
    }
    
    /* 트랙 라벨 */
    .track-label {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--accent-gold);
        margin-bottom: 1.5rem;
        padding: 0.5rem 1rem;
        background: rgba(201, 162, 39, 0.1);
        border-radius: 8px;
        display: inline-block;
    }
    
    /* 숨김 요소 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()

# 라우팅 로직
def main():
    # 인증 상태 확인
    auth_service = AuthService()
    
    if not st.session_state.get('authenticated', False):
        # 로그인/회원가입 페이지
        tab1, tab2 = st.tabs(["🔐 로그인", "📝 회원가입"])
        
        with tab1:
            login.render()
        
        with tab2:
            signup.render()
    else:
        # 메인 대시보드
        render_authenticated_app()

def render_authenticated_app():
    """인증된 사용자를 위한 메인 앱 렌더링"""
    
    # 사이드바
    with st.sidebar:
        render_sidebar()
    
    # 현재 페이지에 따라 렌더링
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard':
        main_dashboard.render()
    elif current_page == 'scenario_form':
        scenario_form.render()
    elif current_page == 'ai_chat':
        ai_chat.render()
    elif current_page == 'document_preview':
        document_preview.render()

def render_sidebar():
    """사이드바 렌더링"""
    
    # 로고
    st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <h1 style="font-family: 'Playfair Display', serif; 
                       font-size: 2rem; 
                       background: linear-gradient(135deg, #C9A227 0%, #E8D5A3 50%, #C9A227 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;">
                K-Stay
            </h1>
            <p style="color: #6c757d; font-size: 0.8rem; letter-spacing: 2px;">
                KOREA STAY ASSISTANT
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 사용자 정보
    user_data = st.session_state.get('user_data', {})
    st.markdown(f"""
        <div style="padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 12px; margin-bottom: 1rem;">
            <p style="color: #a0aec0; font-size: 0.85rem; margin: 0;">환영합니다</p>
            <p style="color: white; font-weight: 600; margin: 0.3rem 0 0 0;">
                {user_data.get('given_name', 'Guest')} {user_data.get('surname', '')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 네비게이션
    st.markdown("### 📍 Navigation")
    
    if st.button("🏠 메인 대시보드", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    if st.button("💬 AI 상담사", use_container_width=True):
        st.session_state.current_page = 'ai_chat'
        st.rerun()
    
    if st.button("📋 내 프로필 수정", use_container_width=True):
        st.session_state.current_page = 'profile_edit'
        st.rerun()
    
    st.divider()
    
    # 결제 상태
    payment_status = st.session_state.get('is_paid', False)
    if payment_status:
        st.success("✨ Premium 활성화됨")
    else:
        st.warning("🔒 결제 필요")
        if st.button("💳 Premium 구매 ($9.99)", use_container_width=True, type="primary"):
            payment_service = PaymentService()
            checkout_url = payment_service.create_checkout_session(
                st.session_state.get('user_id'),
                st.session_state.get('user_email')
            )
            if checkout_url:
                st.markdown(f'<a href="{checkout_url}" target="_blank">결제 페이지로 이동</a>', 
                           unsafe_allow_html=True)
    
    st.divider()
    
    # 로그아웃
    if st.button("🚪 로그아웃", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
