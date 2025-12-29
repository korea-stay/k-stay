"""
🇰🇷 K-Stay: Korea Stay Assistant
외국인을 위한 출입국 민원 서류 자동 생성 플랫폼
"""

import streamlit as st
from config.settings import init_page_config, init_session_state
from services.auth_service import AuthService, SessionManager
from services.payment_service import PaymentService
from pages import login, signup, main_dashboard, scenario_form, ai_chat, document_preview

# 페이지 설정
init_page_config()

# 세션 상태 초기화
init_session_state()


def restore_session():
    """Supabase 세션 자동 복원"""
    # 이미 인증된 경우 스킵
    if st.session_state.get('authenticated', False):
        return
    
    auth_service = AuthService()
    
    # Supabase 연결된 경우 세션 복원 시도
    if auth_service.is_supabase_connected() and auth_service.supabase:
        try:
            # 현재 세션 확인
            session = auth_service.supabase.auth.get_session()
            
            if session and session.user:
                user_id = session.user.id
                
                # 사용자 프로필 가져오기
                profile_response = auth_service.supabase.table('users').select('*').eq('id', user_id).single().execute()
                
                if profile_response.data:
                    user_data = profile_response.data
                    SessionManager.login_user(user_data)
                    st.toast("✅ 자동 로그인되었습니다!", icon="👋")
        except Exception as e:
            # 세션 복원 실패 시 무시
            pass


# 세션 복원 시도
restore_session()


# CSS 스타일 적용
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-blue: #2563eb;
        --primary-blue-dark: #1d4ed8;
        --primary-blue-light: #dbeafe;
        --slate-50: #f8fafc;
        --slate-100: #f1f5f9;
        --slate-200: #e2e8f0;
        --slate-300: #cbd5e1;
        --slate-400: #94a3b8;
        --slate-500: #64748b;
        --slate-600: #475569;
        --slate-700: #334155;
        --slate-800: #1e293b;
        --green-500: #22c55e;
        --green-100: #dcfce7;
        --pink-500: #ec4899;
        --pink-50: #fdf2f8;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .stApp {
        background-color: #f8fafc !important;
    }
    
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #1e293b !important;
    }
    
    .stMarkdown, .stMarkdown p {
        color: #334155 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1rem;
    }
    
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--primary-blue);
        color: white;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: var(--primary-blue-dark);
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        border: 1px solid var(--slate-300) !important;
        border-radius: 0.5rem !important;
        font-size: 0.9rem !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid var(--slate-200);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--slate-100);
        border-radius: 0.5rem;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()


def main():
    """메인 라우팅"""
    
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
    """인증된 사용자를 위한 메인 앱"""
    
    with st.sidebar:
        render_sidebar()
    
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
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem;">
            <div style="
                width: 32px;
                height: 32px;
                background: #2563eb;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
            ">🇰🇷</div>
            <span style="font-weight: 700; font-size: 1.1rem; color: #1e293b !important;">K-Stay</span>
        </div>
    """, unsafe_allow_html=True)
    
    # 사용자 정보
    user_data = st.session_state.get('user_data', {})
    st.markdown(f"""
        <div style="
            padding: 0.75rem;
            background: #f1f5f9;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        ">
            <p style="color: #64748b !important; font-size: 0.8rem; margin: 0;">로그인 계정</p>
            <p style="color: #1e293b !important; font-weight: 600; margin: 0.25rem 0 0 0; font-size: 0.9rem;">
                {user_data.get('given_name', 'Guest')} {user_data.get('surname', '')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 네비게이션
    st.markdown('<p style="color: #64748b !important; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">Menu</p>', unsafe_allow_html=True)
    
    if st.button("🏠 대시보드", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.session_state.dashboard_mode = 'scenarios'
        st.rerun()
    
    if st.button("💬 AI 상담", use_container_width=True):
        st.session_state.current_page = 'ai_chat'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 결제 상태
    payment_status = st.session_state.get('is_paid', False)
    if payment_status:
        st.markdown("""
            <div style="
                padding: 0.75rem;
                background: #dcfce7;
                border-radius: 0.5rem;
                border: 1px solid #bbf7d0;
                text-align: center;
            ">
                <span style="color: #166534; font-size: 0.85rem; font-weight: 500;">✓ Premium 활성화</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                padding: 0.75rem;
                background: #fef3c7;
                border-radius: 0.5rem;
                border: 1px solid #fde68a;
                text-align: center;
            ">
                <span style="color: #92400e; font-size: 0.85rem; font-weight: 500;">🔒 결제 필요</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 로그아웃
    if st.button("🚪 로그아웃", use_container_width=True):
        # Supabase 로그아웃
        auth_service = AuthService()
        auth_service.sign_out()
        
        # 세션 초기화
        SessionManager.logout_user()
        st.rerun()


if __name__ == "__main__":
    main()
