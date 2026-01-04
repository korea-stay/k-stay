"""
K-Stay Login Page
Clean White/Blue Theme with i18n
"""

import streamlit as st
from services.auth_service import AuthService, SessionManager
from utils.i18n import t
from utils.scroll import scroll_to_top


def render():
    """로그인 페이지 렌더링"""
    # 페이지 진입 시 스크롤 맨 위로
    scroll_to_top()

    # 로그인 폼 (컬럼 없이 바로 렌더링 - 상위에서 컬럼 처리함)
    with st.form("login_form"):
        st.markdown(f'<label style="font-size: 0.875rem; font-weight: 500; color: #334155;">{t("auth.email")}</label>', unsafe_allow_html=True)
        email = st.text_input(
            t("auth.email"),
            placeholder=t("auth.email_placeholder"),
            key="login_email",
            label_visibility="collapsed"
        )
        
        st.markdown(f'<label style="font-size: 0.875rem; font-weight: 500; color: #334155; margin-top: 1rem; display: block;">{t("auth.password")}</label>', unsafe_allow_html=True)
        password = st.text_input(
            t("auth.password"),
            type="password",
            placeholder="••••••••",
            key="login_password",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            t("auth.login_btn"),
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not email or not password:
                st.error(t("auth.login_error"))
            else:
                auth_service = AuthService()
                success, message, user_data = auth_service.sign_in(email, password)
                
                if success:
                    SessionManager.login_user(user_data)
                    st.success(t("auth.login_success"))
                    st.rerun()
                else:
                    st.error(message)
    
    # 테스트 계정 안내
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 0.5rem;
            margin-top: 1rem;
            border: 1px solid #e2e8f0;
        ">
            <p style="color: #64748b; font-size: 0.8rem; margin: 0;">
                {t("auth.test_account")}: <strong>admin</strong> / <strong>1234</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(f"🚀 {t('auth.test_login')}", use_container_width=True):
        test_user = {
            'id': 'test-user-001',
            'email': 'test@kstay.com',
            'surname': 'Hong',
            'given_name': 'Gil-dong',
            'nationality': 'USA',
            'birth_date': '1990-01-01',
            'gender': 'Male',
            'passport_no': 'M12345678',
            'korea_address': '서울시 강남구 테헤란로 123',
            'korea_phone': '010-1234-5678',
            'is_paid': True,
            'is_admin': False
        }
        
        SessionManager.login_user(test_user)
        st.success(t("auth.login_success"))
        st.rerun()
