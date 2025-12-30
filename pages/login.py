"""
K-Stay Login Page
Clean White/Blue Theme
"""

import streamlit as st
from services.auth_service import AuthService, SessionManager


def render():
    """로그인 페이지 렌더링"""
    
    # 로그인 폼 (컬럼 없이 바로 렌더링 - 상위에서 컬럼 처리함)
    with st.form("login_form"):
        st.markdown('<label style="font-size: 0.875rem; font-weight: 500; color: #334155;">이메일</label>', unsafe_allow_html=True)
        email = st.text_input(
            "이메일",
            placeholder="your@email.com",
            key="login_email",
            label_visibility="collapsed"
        )
        
        st.markdown('<label style="font-size: 0.875rem; font-weight: 500; color: #334155; margin-top: 1rem; display: block;">비밀번호</label>', unsafe_allow_html=True)
        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="••••••••",
            key="login_password",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "로그인",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not email or not password:
                st.error("이메일과 비밀번호를 입력해주세요.")
            else:
                auth_service = AuthService()
                success, message, user_data = auth_service.sign_in(email, password)
                
                if success:
                    SessionManager.login_user(user_data)
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    # 테스트 계정 안내
    st.markdown("""
        <div style="
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 0.5rem;
            margin-top: 1rem;
            border: 1px solid #e2e8f0;
        ">
            <p style="color: #64748b; font-size: 0.8rem; margin: 0;">
                테스트: <strong>admin</strong> / <strong>1234</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 테스트 계정으로 바로 시작", use_container_width=True):
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
        st.success("테스트 계정으로 로그인되었습니다!")
        st.rerun()