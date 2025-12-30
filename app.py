"""
🇰🇷 K-Stay: Korea Stay Assistant
외국인을 위한 출입국 민원 서류 자동 생성 플랫폼
"""

import streamlit as st
from config.settings import init_page_config, init_session_state
from services.auth_service import AuthService, SessionManager
from services.payment_service import PaymentService
from pages import login, signup, main_dashboard, scenario_form, ai_chat, document_preview, my_documents, my_page

# 페이지 설정
init_page_config()

# 세션 상태 초기화
init_session_state()


# CSS 스타일
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6,
    .stTextInput input, .stTextArea textarea, .stSelectbox,
    .stButton button, .stDownloadButton button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    .stButton button { border-radius: 0.5rem; font-weight: 500; transition: all 0.2s; }
    .stButton button:hover { transform: translateY(-1px); }
    .stButton button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; }
    .stTextInput input, .stSelectbox div, .stTextArea textarea { border-radius: 0.5rem; }
    [data-testid="stSidebar"] { background: white; border-right: 1px solid #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { border-radius: 0.5rem; padding: 0.5rem 1rem; }
    .stAlert { border-radius: 0.5rem; }
    .stDownloadButton button { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; border-radius: 0.5rem; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)


load_css()


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
    elif current_page == 'my_documents':
        my_documents.render()
    elif current_page == 'my_page':
        my_page.render()


def render_sidebar():
    """사이드바 렌더링"""
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem;">
            <div style="width: 32px; height: 32px; background: #2563eb; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1rem;">🇰🇷</div>
            <span style="font-weight: 700; font-size: 1.1rem; color: #1e293b;">K-Stay</span>
        </div>
    """, unsafe_allow_html=True)
    
    user_data = st.session_state.get('user_data', {})
    st.markdown(f"""
        <div style="padding: 0.75rem; background: #f1f5f9; border-radius: 0.5rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;">
            <p style="color: #64748b; font-size: 0.8rem; margin: 0;">로그인 계정</p>
            <p style="color: #1e293b; font-weight: 600; margin: 0.25rem 0 0 0; font-size: 0.9rem;">{user_data.get('given_name', 'Guest')} {user_data.get('surname', '')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #64748b; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">Menu</p>', unsafe_allow_html=True)
    
    if st.button("🏠 대시보드", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.session_state.password_verified = False
        st.rerun()
    
    if st.button("📁 내 문서함", use_container_width=True):
        st.session_state.current_page = 'my_documents'
        st.session_state.password_verified = False
        st.rerun()
    
    if st.button("💬 AI 상담", use_container_width=True):
        st.session_state.current_page = 'ai_chat'
        st.session_state.password_verified = False
        st.rerun()
    
    if st.button("👤 마이페이지", use_container_width=True):
        st.session_state.current_page = 'my_page'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    is_admin = st.session_state.get('is_admin', False)
    is_paid = st.session_state.get('is_paid', False)
    
    if is_admin:
        st.markdown('<div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 1px solid #f59e0b; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; font-weight: 600; color: #92400e; font-size: 0.85rem;">👑 관리자 계정</p></div>', unsafe_allow_html=True)
    elif is_paid:
        st.markdown('<div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border: 1px solid #22c55e; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; font-weight: 600; color: #166534; font-size: 0.85rem;">✨ Premium 활성화됨</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; color: #64748b; font-size: 0.85rem;">무료 플랜</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚪 로그아웃", use_container_width=True):
        AuthService().sign_out()
        st.rerun()


def render_auth_page():
    """로그인/회원가입 페이지"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border-radius: 1.5rem; display: inline-flex; align-items: center; justify-content: center; font-size: 2.5rem; margin-bottom: 1.5rem; box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);">🇰🇷</div>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0;">K-Stay</h1>
            <p style="color: #64748b; font-size: 1.1rem;">외국인 비자 서류 자동화 플랫폼</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 로그인", "📝 회원가입"])
        
        with tab1:
            login.render()
        
        with tab2:
            signup.render()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        auth_service = AuthService()
        if auth_service.is_supabase_connected():
            st.success("✅ Supabase 연결됨")
        else:
            st.info("💡 테스트 모드")


def main():
    """메인 앱 실행"""
    if SessionManager.is_authenticated():
        render_authenticated_app()
    else:
        render_auth_page()


if __name__ == "__main__":
    main()