"""
K-Stay Login Page
"""

import streamlit as st
from services.auth_service import AuthService, SessionManager


def render():
    """로그인 페이지 렌더링"""
    
    # 헤더
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="
                font-family: 'Playfair Display', serif;
                font-size: 4rem;
                font-weight: 700;
                background: linear-gradient(135deg, #C9A227 0%, #E8D5A3 50%, #C9A227 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">K-Stay</h1>
            <p style="
                font-family: 'Noto Sans KR', sans-serif;
                color: #6c757d;
                font-size: 1rem;
                letter-spacing: 3px;
            ">KOREA STAY ASSISTANT</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 로그인 폼
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(201,162,39,0.2);
                border-radius: 20px;
                padding: 2.5rem;
                margin-top: 1rem;
            ">
                <h3 style="
                    color: white;
                    text-align: center;
                    margin-bottom: 1.5rem;
                    font-family: 'Noto Sans KR', sans-serif;
                ">🔐 로그인</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input(
                "이메일",
                placeholder="your@email.com",
                key="login_email"
            )
            
            password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="••••••••",
                key="login_password"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                remember = st.checkbox("로그인 유지", value=True)
            with col_b:
                st.markdown("""
                    <p style="text-align: right; color: #C9A227; font-size: 0.9rem;">
                        비밀번호 찾기
                    </p>
                """, unsafe_allow_html=True)
            
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
        
        # 소셜 로그인 (향후 구현)
        st.markdown("""
            <div style="
                text-align: center;
                margin-top: 2rem;
                padding-top: 1.5rem;
                border-top: 1px solid rgba(255,255,255,0.1);
            ">
                <p style="color: #6c757d; font-size: 0.85rem; margin-bottom: 1rem;">
                    또는
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col_g, col_k = st.columns(2)
        with col_g:
            st.button("🔵 Google", use_container_width=True, disabled=True)
        with col_k:
            st.button("💬 Kakao", use_container_width=True, disabled=True)
        
        st.caption("소셜 로그인은 곧 지원 예정입니다.")
    
    # 푸터
    st.markdown("""
        <div style="
            text-align: center;
            margin-top: 4rem;
            color: #6c757d;
            font-size: 0.8rem;
        ">
            <p>© 2024 K-Stay. All rights reserved.</p>
            <p>출입국 민원 서류 자동 생성 플랫폼</p>
        </div>
    """, unsafe_allow_html=True)


def render_demo_login():
    """데모 로그인 (개발용)"""
    st.markdown("---")
    st.markdown("### 🧪 개발용 테스트 계정")
    
    if st.button("테스트 계정으로 로그인", use_container_width=True):
        # 테스트 사용자 생성
        test_user = {
            'id': 'test-user-001',
            'email': 'test@kstay.com',
            'surname': 'Kim',
            'given_name': 'TestUser',
            'nationality': 'USA',
            'birth_date': '1990-01-01',
            'gender': 'Male',
            'passport_no': 'M12345678',
            'korea_address': '서울시 강남구 테헤란로 123',
            'korea_phone': '010-1234-5678',
            'is_paid': True,  # 테스트용 결제 완료
            'is_admin': False
        }
        
        SessionManager.login_user(test_user)
        st.success("테스트 계정으로 로그인되었습니다!")
        st.rerun()
