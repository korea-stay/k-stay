"""
🇰🇷 K-Stay: Korea Stay Assistant
외국인을 위한 출입국 민원 서류 자동 생성 플랫폼
"""

import streamlit as st
from config.settings import init_page_config, init_session_state
from services.auth_service import AuthService, SessionManager
from services.payment_service import PaymentService
from pages import login, signup, main_dashboard, scenario_form, ai_chat, document_preview, my_documents, my_page
from utils.i18n import t, init_language, get_current_language

# 페이지 설정
init_page_config()

# 세션 상태 초기화
init_session_state()

# 언어 초기화
init_language()


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
    
    /* 언어 선택 버튼 스타일 */
    .lang-switch {
        display: flex;
        gap: 4px;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


load_css()


def render_language_switch():
    """언어 선택 스위치 렌더링"""
    current_lang = get_current_language()
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col2:
        if current_lang == "ko":
            st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    text-align: center;
                ">🇰🇷 한국어</div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🇰🇷 한국어", key="switch_ko", use_container_width=True):
                st.session_state.language = "ko"
                st.rerun()
    
    with col3:
        if current_lang == "en":
            st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    text-align: center;
                ">🇺🇸 EN</div>
            """, unsafe_allow_html=True)
        else:
            if st.button("🇺🇸 EN", key="switch_en", use_container_width=True):
                st.session_state.language = "en"
                st.rerun()


def render_authenticated_app():
    """인증된 사용자를 위한 메인 앱"""
    with st.sidebar:
        render_sidebar()
    
    # 페이지 상단 언어 선택
    render_language_switch()
    
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
            <p style="color: #64748b; font-size: 0.8rem; margin: 0;">{t('auth.logged_in_as')}</p>
            <p style="color: #1e293b; font-weight: 600; margin: 0.25rem 0 0 0; font-size: 0.9rem;">{user_data.get('given_name', 'Guest')} {user_data.get('surname', '')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<p style="color: #64748b; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;">{t("common.menu")}</p>', unsafe_allow_html=True)
    
    if st.button(f"🏠 {t('sidebar.dashboard')}", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.session_state.password_verified = False
        st.session_state.docs_password_verified = False
        st.rerun()
    
    if st.button(f"📁 {t('sidebar.my_documents')}", use_container_width=True):
        st.session_state.current_page = 'my_documents'
        st.session_state.password_verified = False
        st.session_state.docs_password_verified = False
        st.rerun()
    
    if st.button(f"💬 {t('sidebar.ai_chat')}", use_container_width=True):
        st.session_state.current_page = 'ai_chat'
        st.session_state.password_verified = False
        st.session_state.docs_password_verified = False
        st.rerun()
    
    if st.button(f"👤 {t('sidebar.my_page')}", use_container_width=True):
        st.session_state.current_page = 'my_page'
        st.session_state.docs_password_verified = False
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    is_admin = st.session_state.get('is_admin', False)
    is_paid = st.session_state.get('is_paid', False)
    
    if is_admin:
        st.markdown(f'<div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border: 1px solid #f59e0b; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; font-weight: 600; color: #92400e; font-size: 0.85rem;">👑 {t("sidebar.admin_account")}</p></div>', unsafe_allow_html=True)
    elif is_paid:
        st.markdown(f'<div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); border: 1px solid #22c55e; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; font-weight: 600; color: #166534; font-size: 0.85rem;">✨ {t("sidebar.premium_active")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 1rem;"><p style="margin: 0; color: #64748b; font-size: 0.85rem;">{t("sidebar.free_plan")}</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(f"🚪 {t('common.logout')}", use_container_width=True):
        AuthService().sign_out()
        st.rerun()


def render_auth_page():
    """로그인/회원가입 페이지"""
    # 페이지 상단 언어 선택
    render_language_switch()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border-radius: 1.5rem; display: inline-flex; align-items: center; justify-content: center; font-size: 2.5rem; margin-bottom: 1.5rem; box-shadow: 0 10px 40px rgba(37, 99, 235, 0.3);">🇰🇷</div>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0;">{t('common.app_name')}</h1>
            <p style="color: #64748b; font-size: 1.1rem;">{t('common.app_subtitle')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # 현재 인증 페이지 상태 (login/signup)
        auth_page = st.session_state.get('auth_page', 'login')
        
        # 페이지 전환 버튼
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if auth_page == 'login':
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                        color: white;
                        padding: 0.75rem 1rem;
                        border-radius: 0.5rem;
                        text-align: center;
                        font-weight: 600;
                    ">🔐 {t('common.login')}</div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"🔐 {t('common.login')}", use_container_width=True):
                    st.session_state.auth_page = 'login'
                    st.rerun()
        
        with btn_col2:
            if auth_page == 'signup':
                st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                        color: white;
                        padding: 0.75rem 1rem;
                        border-radius: 0.5rem;
                        text-align: center;
                        font-weight: 600;
                    ">📝 {t('common.signup')}</div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"📝 {t('common.signup')}", use_container_width=True):
                    st.session_state.auth_page = 'signup'
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 페이지 렌더링
        if auth_page == 'login':
            login.render()
        else:
            signup.render()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        auth_service = AuthService()
        if auth_service.is_supabase_connected():
            st.success(f"✅ {t('auth.supabase_connected')}")
        else:
            st.info(f"💡 {t('auth.test_mode')}")


def main():
    """메인 앱 실행"""
    if SessionManager.is_authenticated():
        render_authenticated_app()
    else:
        render_auth_page()


if __name__ == "__main__":
    main()