"""
🇰🇷 K-Stay: Korea Stay Assistant
외국인을 위한 출입국 민원 서류 자동 생성 플랫폼
"""

import streamlit as st
import base64
from pathlib import Path
from config.settings import init_page_config, init_session_state
from services.auth_service import AuthService, SessionManager
from services.payment_service import PaymentService
from pages import login, signup, main_dashboard, scenario_form, ai_chat, document_preview, my_documents, my_page
from utils.i18n import t, init_language, get_current_language


def get_base64_image(image_path: str) -> str:
    """이미지를 base64로 인코딩"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

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
    
    /* 기본 폰트 설정 */
    .main, .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6,
    .stTextInput input, .stTextArea textarea, .stSelectbox,
    .stButton button, .stDownloadButton button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 버튼 및 입력 필드 스타일 */
    .stButton button { border-radius: 0.5rem; font-weight: 500; transition: all 0.2s; }
    .stButton button:hover { transform: translateY(-1px); }
    .stButton button[kind="primary"] { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; }
    .stTextInput input, .stSelectbox div, .stTextArea textarea { border-radius: 0.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { border-radius: 0.5rem; padding: 0.5rem 1rem; }
    .stAlert { border-radius: 0.5rem; }
    .stDownloadButton button { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; border: none; border-radius: 0.5rem; }
    
    /* 기본 헤더/푸터 숨김 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] { display: none; }
    
    /* ========================================
       사이드바 고정 및 버튼 '완전 박멸' CSS
       ======================================== */
    
    /* 1. 사이드바 접기/펼치기 버튼 (모든 상태 포함) */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 2. 혹시 모를 헤더 영역 내의 사이드바 토글 버튼 숨김 */
    header[data-testid="stHeader"] button[data-testid="baseButton-header"] {
        display: none !important;
    }
    
    /* 3. 사이드바 상단 여백 정리 (버튼이 사라진 자리 메우기) */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem !important; /* 버튼 공간만큼 위로 당김 */
    }

    /* 4. 사이드바 스타일 고정 */
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
        width: 300px !important;
        background: white !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    /* 5. 메인 컨텐츠 영역 위치 조정 */
    .main .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
    }
    
    /* 언어 선택 버튼 스타일 */
    .lang-switch {
        display: flex;
        gap: 4px;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 8px;
    }
    </style>
    
    <script>
        window.scrollTo(0, 0);
        const mainContainer = window.parent.document.querySelector('section.main');
        if (mainContainer) { mainContainer.scrollTop = 0; }
    </script>
    """, unsafe_allow_html=True)

load_css()


def render_language_switch(is_auth_page=False):
    """
    언어 선택 스위치 렌더링
    is_auth_page=True일 경우 로그인 화면용으로 중앙 정렬
    """
    current_lang = get_current_language()
    
    if is_auth_page:
        # 로그인 페이지: 중앙 정렬 (양옆 여백을 크게 주어 가운데로 모음)
        col_space_l, col_ko, col_en, col_space_r = st.columns([4, 1, 1, 4])
        target_ko = col_ko
        target_en = col_en
    else:
        # 메인 앱: 우측 상단 정렬
        col_space, col_ko, col_en = st.columns([6, 1, 1])
        target_ko = col_ko
        target_en = col_en
    
    with target_ko:
        if current_lang == "ko":
            # 색상 코드를 로그인 탭과 동일한 #2563eb 시작
            st.markdown('<div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 6px 12px; border-radius: 0.5rem; font-size: 0.8rem; font-weight: 600; text-align: center; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);">🇰🇷 한국어</div>', unsafe_allow_html=True)
        else:
            if st.button("🇰🇷 한국어", key="switch_ko", use_container_width=True):
                st.session_state.language = "ko"
                st.rerun()
    
    with target_en:
        if current_lang == "en":
            # 색상 코드를 로그인 탭과 동일한 #2563eb 시작
            st.markdown('<div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 6px 12px; border-radius: 0.5rem; font-size: 0.8rem; font-weight: 600; text-align: center; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);">🇺🇸 EN</div>', unsafe_allow_html=True)
        else:
            if st.button("🇺🇸 EN", key="switch_en", use_container_width=True):
                st.session_state.language = "en"
                st.rerun()


def render_authenticated_app():
    """인증된 사용자를 위한 메인 앱"""
    with st.sidebar:
        render_sidebar()
    
    # 페이지 상단 언어 선택 (기본 우측 정렬)
    render_language_switch(is_auth_page=False)
    
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
    st.markdown('<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1.5rem;"><div style="width: 32px; height: 32px; background: #2563eb; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1rem;">🇰🇷</div><span style="font-weight: 700; font-size: 1.1rem; color: #1e293b;">K-Stay</span></div>', unsafe_allow_html=True)
    
    user_data = st.session_state.get('user_data', {})
    logged_in_text = t('auth.logged_in_as')
    given_name = user_data.get('given_name', 'Guest')
    surname = user_data.get('surname', '')
    st.markdown(f'<div style="padding: 0.75rem; background: #f1f5f9; border-radius: 0.5rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;"><p style="color: #64748b; font-size: 0.8rem; margin: 0;">{logged_in_text}</p><p style="color: #1e293b; font-weight: 600; margin: 0.25rem 0 0 0; font-size: 0.9rem;">{given_name} {surname}</p></div>', unsafe_allow_html=True)
    
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
    
    # 배경 이미지 로드 시도
    bg_image_base64 = None
    possible_paths = [
        "assets/images/kstay_background.png",
        "static/images/kstay_background.png", 
        "images/kstay_background.png",
        "kstay_background.png"
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            bg_image_base64 = get_base64_image(path)
            if bg_image_base64:
                break
    
    # 배경 스타일 결정
    if bg_image_base64:
        bg_style = f'background-image: url("data:image/png;base64,{bg_image_base64}"); background-size: cover; background-position: center; background-attachment: fixed;'
    else:
        bg_style = 'background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 50%, #1e3a5f 100%);'
    
    # 기본 페이지가 'landing'으로 설정되어 있어도 탭 뷰를 위해 'login'으로 보정
    if st.session_state.get('auth_page') == 'landing':
        st.session_state.auth_page = 'login'

    # 로그인 페이지 전용 CSS
    st.markdown(f"""
        <style>
            /* 사이드바 완전히 숨기기 */
            [data-testid="stSidebar"] {{
                display: none !important;
                width: 0 !important;
                min-width: 0 !important;
            }}
            
            [data-testid="collapsedControl"] {{
                display: none !important;
            }}
            
            [data-testid="stAppViewContainer"] {{
                margin-left: 0 !important;
            }}
            
            /* 로그인 페이지 너비 제한 */
            .main .block-container {{
                max-width: 450px !important;
                margin: 0 auto !important;
                padding-top: 2rem !important;
            }}
            
            /* 배경 이미지 */
            .stApp {{
                {bg_style}
            }}
            
            header[data-testid="stHeader"] {{
                background: transparent !important;
            }}
            
            /* 폼 스타일 - 흰색 카드 */
            [data-testid="stForm"] {{
                background: #ffffff !important;
                padding: 2rem !important;
                border-radius: 16px !important;
                border: 1px solid #e2e8f0 !important;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
            }}
            
            /* 입력 필드 */
            .stTextInput > div > div > input {{
                background: #f8fafc !important;
                border: 2px solid #e2e8f0 !important;
                border-radius: 10px !important;
                padding: 12px 16px !important;
            }}
            
            .stTextInput > div > div > input:focus {{
                border-color: #2563eb !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
                background: #ffffff !important;
            }}
            
            /* 로그인 버튼 (Submit) */
            .stFormSubmitButton > button {{
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 12px 24px !important;
                font-weight: 600 !important;
            }}
            
            /* 일반 버튼 (비활성 탭, 언어 선택 등) - 흰색 배경 강제 적용 */
            /* 좀 더 강력한 선택자 사용 */
            [data-testid="stAppViewContainer"] .stButton > button {{
                border-radius: 10px !important;
                background: #ffffff !important;
                color: #1e293b !important;
                border: 1px solid #e2e8f0 !important;
                box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
            }}
            
            /* 일반 버튼 호버 효과 */
            [data-testid="stAppViewContainer"] .stButton > button:hover {{
                background: #f1f5f9 !important;
                border-color: #cbd5e1 !important;
                color: #0f172a !important;
                transform: translateY(-1px);
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # 페이지 상단 언어 선택 (로그인 화면용 중앙 정렬 적용)
    render_language_switch(is_auth_page=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 로고 섹션
    app_name = t('common.app_name')
    app_subtitle = t('common.app_subtitle')
    st.markdown(
        f'<div style="text-align: center; margin-bottom: 2rem;">'
        
        f'<h1 style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0;">{app_name}</h1>'
        f'<p style="color: #64748b; font-size: 1.1rem;">{app_subtitle}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # 탭 메뉴 및 컨텐츠 영역
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col2:
        # 현재 인증 페이지 상태 (login/signup)
        auth_page = st.session_state.get('auth_page', 'login')
        
        # 탭 버튼 영역
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if auth_page == 'login':
                login_text = t('common.login')
                # 선택됨: 파란색 그라데이션
                st.markdown(f'<div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 0.75rem 1rem; border-radius: 0.5rem; text-align: center; font-weight: 600; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);">🔐 {login_text}</div>', unsafe_allow_html=True)
            else:
                if st.button(f"🔐 {t('common.login')}", use_container_width=True):
                    st.session_state.auth_page = 'login'
                    st.rerun()
        
        with btn_col2:
            if auth_page == 'signup':
                signup_text = t('common.signup')
                # 선택됨: 붉은색(갈색) 그라데이션
                st.markdown(f'<div style="background: linear-gradient(135deg, #b45309 0%, #92400e 100%); color: white; padding: 0.75rem 1rem; border-radius: 0.5rem; text-align: center; font-weight: 600; box-shadow: 0 4px 6px -1px rgba(180, 83, 9, 0.2);">📝 {signup_text}</div>', unsafe_allow_html=True)
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
        


def main():
    """메인 앱 실행"""
    if SessionManager.is_authenticated():
        render_authenticated_app()
    else:
        render_auth_page()


if __name__ == "__main__":
    main()