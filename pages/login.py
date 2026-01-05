"""
K-Stay Login Page
간소화 버전 - app.py에서 CSS 처리
"""

import streamlit as st
from services.auth_service import AuthService, SessionManager
from utils.i18n import t
from utils.scroll import scroll_to_top


def render():
    """로그인 페이지 렌더링"""
    scroll_to_top()
    
    # 로그인 폼
    with st.form("login_form", clear_on_submit=False):
        email_label = t("auth.email")
        st.markdown(f"<p style='color: #334155; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;'>📧 {email_label}</p>", unsafe_allow_html=True)
        
        email = st.text_input(
            email_label,
            placeholder=t("auth.email_placeholder"),
            key="login_email",
            label_visibility="collapsed"
        )
        
        password_label = t("auth.password")
        st.markdown(f"<p style='color: #334155; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem; margin-top: 1rem;'>🔒 {password_label}</p>", unsafe_allow_html=True)
        
        password = st.text_input(
            password_label,
            type="password",
            placeholder="••••••••",
            key="login_password",
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            t('auth.login_btn'),
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

    
    st.markdown("<div style='display: flex; align-items: center; margin: 1.5rem 0;'><div style='flex: 1; height: 1px; background: #e2e8f0;'></div><span style='padding: 0 1rem; color: #94a3b8; font-size: 0.8rem;'>또는</span><div style='flex: 1; height: 1px; background: #e2e8f0;'></div></div>", unsafe_allow_html=True)
    
    test_login_text = t('auth.test_login')
    if st.button(f"🚀 {test_login_text}", use_container_width=True, key="test_login_btn"):
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


if __name__ == "__main__":
    render()