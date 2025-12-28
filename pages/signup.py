"""
K-Stay Signup Page
Phase 1: Universal Fact Collection (불변 정보 수집)
"""

import streamlit as st
from datetime import datetime, date
from services.auth_service import AuthService, SessionManager


def render():
    """회원가입 페이지 렌더링"""
    
    # 헤더
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="
                font-family: 'Playfair Display', serif;
                font-size: 3rem;
                font-weight: 700;
                background: linear-gradient(135deg, #C9A227 0%, #E8D5A3 50%, #C9A227 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">회원가입</h1>
            <p style="color: #a0aec0; margin-top: 0.5rem;">
                통합신청서 상단 정보를 한 번만 입력하세요
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 진행 단계 표시
    render_progress_steps()
    
    # 현재 단계 가져오기
    current_step = st.session_state.get('signup_step', 1)
    
    # 단계별 렌더링
    if current_step == 1:
        render_step1_account()
    elif current_step == 2:
        render_step2_personal()
    elif current_step == 3:
        render_step3_passport()
    elif current_step == 4:
        render_step4_contact()
    elif current_step == 5:
        render_step5_confirm()


def render_progress_steps():
    """진행 단계 UI"""
    current_step = st.session_state.get('signup_step', 1)
    
    steps = [
        ("1", "계정", "account"),
        ("2", "인적사항", "personal"),
        ("3", "여권", "passport"),
        ("4", "연락처", "contact"),
        ("5", "확인", "confirm")
    ]
    
    cols = st.columns(len(steps))
    
    for i, (num, label, key) in enumerate(steps):
        with cols[i]:
            is_active = (i + 1) == current_step
            is_completed = (i + 1) < current_step
            
            if is_completed:
                color = "#4CAF50"
                bg = "rgba(76, 175, 80, 0.2)"
                icon = "✓"
            elif is_active:
                color = "#C9A227"
                bg = "rgba(201, 162, 39, 0.2)"
                icon = num
            else:
                color = "#6c757d"
                bg = "rgba(108, 117, 125, 0.1)"
                icon = num
            
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        background: {bg};
                        border: 2px solid {color};
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        color: {color};
                        font-weight: 700;
                        margin-bottom: 0.5rem;
                    ">{icon}</div>
                    <p style="color: {color}; font-size: 0.8rem; margin: 0;">{label}</p>
                </div>
            """, unsafe_allow_html=True)


def render_step1_account():
    """Step 1: 계정 정보"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        ">
            <h3 style="color: #C9A227; margin-bottom: 1.5rem;">📧 계정 정보</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input(
            "이메일 *",
            placeholder="your@email.com",
            key="signup_email",
            value=st.session_state.get('signup_data', {}).get('email', '')
        )
    
    with col2:
        email_confirm = st.text_input(
            "이메일 확인 *",
            placeholder="이메일을 다시 입력하세요",
            key="signup_email_confirm"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        password = st.text_input(
            "비밀번호 *",
            type="password",
            placeholder="8자 이상, 영문+숫자",
            key="signup_password"
        )
    
    with col4:
        password_confirm = st.text_input(
            "비밀번호 확인 *",
            type="password",
            placeholder="비밀번호를 다시 입력하세요",
            key="signup_password_confirm"
        )
    
    st.caption("* 표시는 필수 입력 항목입니다.")
    
    col_prev, col_next = st.columns(2)
    
    with col_next:
        if st.button("다음 →", use_container_width=True, type="primary"):
            # 유효성 검사
            if not email or not password:
                st.error("모든 필수 항목을 입력해주세요.")
                return
            
            if email != email_confirm:
                st.error("이메일이 일치하지 않습니다.")
                return
            
            if password != password_confirm:
                st.error("비밀번호가 일치하지 않습니다.")
                return
            
            auth_service = AuthService()
            
            if not auth_service.validate_email(email):
                st.error("유효하지 않은 이메일 형식입니다.")
                return
            
            is_valid, msg = auth_service.validate_password(password)
            if not is_valid:
                st.error(msg)
                return
            
            # 데이터 저장
            if 'signup_data' not in st.session_state:
                st.session_state.signup_data = {}
            
            st.session_state.signup_data['email'] = email
            st.session_state.signup_data['password'] = password
            st.session_state.signup_step = 2
            st.rerun()


def render_step2_personal():
    """Step 2: 인적 사항"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        ">
            <h3 style="color: #C9A227; margin-bottom: 1.5rem;">👤 인적 사항</h3>
            <p style="color: #a0aec0; font-size: 0.9rem;">
                여권에 기재된 정보와 동일하게 입력해주세요 (영문)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        surname = st.text_input(
            "성 (Surname) *",
            placeholder="KIM",
            key="signup_surname",
            value=st.session_state.get('signup_data', {}).get('surname', '')
        )
    
    with col2:
        given_name = st.text_input(
            "이름 (Given Name) *",
            placeholder="MINJUN",
            key="signup_given_name",
            value=st.session_state.get('signup_data', {}).get('given_name', '')
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        birth_date = st.date_input(
            "생년월일 *",
            min_value=date(1920, 1, 1),
            max_value=date.today(),
            value=date(1990, 1, 1),
            key="signup_birth_date"
        )
    
    with col4:
        gender = st.selectbox(
            "성별 *",
            options=["", "Male", "Female"],
            key="signup_gender"
        )
    
    col5, col6 = st.columns(2)
    
    with col5:
        nationality = st.text_input(
            "국적 *",
            placeholder="USA, China, Vietnam...",
            key="signup_nationality",
            value=st.session_state.get('signup_data', {}).get('nationality', '')
        )
    
    with col6:
        alien_registration_no = st.text_input(
            "외국인등록번호",
            placeholder="없으면 비워두세요",
            key="signup_alien_reg",
            value=st.session_state.get('signup_data', {}).get('alien_registration_no', '')
        )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button("← 이전", use_container_width=True):
            st.session_state.signup_step = 1
            st.rerun()
    
    with col_next:
        if st.button("다음 →", use_container_width=True, type="primary"):
            if not all([surname, given_name, gender, nationality]):
                st.error("모든 필수 항목을 입력해주세요.")
                return
            
            st.session_state.signup_data.update({
                'surname': surname.upper(),
                'given_name': given_name.upper(),
                'birth_date': birth_date.isoformat(),
                'gender': gender,
                'nationality': nationality.upper(),
                'alien_registration_no': alien_registration_no or '미소지'
            })
            st.session_state.signup_step = 3
            st.rerun()


def render_step3_passport():
    """Step 3: 여권 정보"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        ">
            <h3 style="color: #C9A227; margin-bottom: 1.5rem;">📘 여권 정보</h3>
        </div>
    """, unsafe_allow_html=True)
    
    passport_no = st.text_input(
        "여권번호 *",
        placeholder="M12345678",
        key="signup_passport_no",
        value=st.session_state.get('signup_data', {}).get('passport_no', '')
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        passport_issue_date = st.date_input(
            "발급일 *",
            min_value=date(2000, 1, 1),
            max_value=date.today(),
            key="signup_passport_issue"
        )
    
    with col2:
        passport_expiry_date = st.date_input(
            "만료일 *",
            min_value=date.today(),
            max_value=date(2040, 12, 31),
            key="signup_passport_expiry"
        )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button("← 이전", use_container_width=True):
            st.session_state.signup_step = 2
            st.rerun()
    
    with col_next:
        if st.button("다음 →", use_container_width=True, type="primary"):
            if not passport_no:
                st.error("여권번호를 입력해주세요.")
                return
            
            if passport_expiry_date <= date.today():
                st.error("여권이 만료되었거나 곧 만료됩니다.")
                return
            
            st.session_state.signup_data.update({
                'passport_no': passport_no.upper(),
                'passport_issue_date': passport_issue_date.isoformat(),
                'passport_expiry_date': passport_expiry_date.isoformat()
            })
            st.session_state.signup_step = 4
            st.rerun()


def render_step4_contact():
    """Step 4: 연락처 정보"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        ">
            <h3 style="color: #C9A227; margin-bottom: 1.5rem;">📞 연락처 정보</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🇰🇷 한국 연락처")
    
    korea_address = st.text_input(
        "한국 주소 *",
        placeholder="서울시 강남구 테헤란로 123, 101동 1001호",
        key="signup_korea_address",
        value=st.session_state.get('signup_data', {}).get('korea_address', '')
    )
    
    korea_phone = st.text_input(
        "한국 휴대전화 *",
        placeholder="010-1234-5678",
        key="signup_korea_phone",
        value=st.session_state.get('signup_data', {}).get('korea_phone', '')
    )
    
    st.markdown("#### 🌍 본국 연락처")
    
    home_country_address = st.text_input(
        "본국 주소 (영문)",
        placeholder="123 Main Street, City, Country",
        key="signup_home_address",
        value=st.session_state.get('signup_data', {}).get('home_country_address', '')
    )
    
    home_country_phone = st.text_input(
        "본국 전화번호",
        placeholder="+1-123-456-7890",
        key="signup_home_phone",
        value=st.session_state.get('signup_data', {}).get('home_country_phone', '')
    )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button("← 이전", use_container_width=True):
            st.session_state.signup_step = 3
            st.rerun()
    
    with col_next:
        if st.button("다음 →", use_container_width=True, type="primary"):
            if not korea_address or not korea_phone:
                st.error("한국 주소와 전화번호는 필수입니다.")
                return
            
            st.session_state.signup_data.update({
                'korea_address': korea_address,
                'korea_phone': korea_phone,
                'home_country_address': home_country_address or '',
                'home_country_phone': home_country_phone or ''
            })
            st.session_state.signup_step = 5
            st.rerun()


def render_step5_confirm():
    """Step 5: 정보 확인 및 가입 완료"""
    
    # Supabase 연결 상태 확인 (디버그용)
    auth_service = AuthService()
    if auth_service.is_supabase_connected():
        st.success("✅ Supabase 연결됨")
    else:
        st.warning("⚠️ Mock 모드 (Supabase 미연결 - secrets.toml 확인 필요)")
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
        ">
            <h3 style="color: #C9A227; margin-bottom: 1.5rem;">✅ 정보 확인</h3>
            <p style="color: #a0aec0; font-size: 0.9rem;">
                입력하신 정보를 확인해주세요. 이 정보는 통합신청서에 자동으로 채워집니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.get('signup_data', {})
    
    # 정보 요약 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📧 계정**")
        st.write(f"이메일: {data.get('email', 'N/A')}")
        
        st.markdown("**👤 인적사항**")
        st.write(f"성명: {data.get('surname', '')} {data.get('given_name', '')}")
        st.write(f"생년월일: {data.get('birth_date', 'N/A')}")
        st.write(f"성별: {data.get('gender', 'N/A')}")
        st.write(f"국적: {data.get('nationality', 'N/A')}")
        st.write(f"외국인등록번호: {data.get('alien_registration_no', '미소지')}")
    
    with col2:
        st.markdown("**📘 여권**")
        st.write(f"여권번호: {data.get('passport_no', 'N/A')}")
        st.write(f"발급일: {data.get('passport_issue_date', 'N/A')}")
        st.write(f"만료일: {data.get('passport_expiry_date', 'N/A')}")
        
        st.markdown("**📞 연락처**")
        st.write(f"한국 주소: {data.get('korea_address', 'N/A')}")
        st.write(f"한국 전화: {data.get('korea_phone', 'N/A')}")
    
    # 이용약관
    st.markdown("---")
    
    agree_terms = st.checkbox("이용약관 및 개인정보 처리방침에 동의합니다.", key="agree_terms")
    agree_marketing = st.checkbox("마케팅 정보 수신에 동의합니다. (선택)", key="agree_marketing")
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button("← 이전", use_container_width=True):
            st.session_state.signup_step = 4
            st.rerun()
    
    with col_next:
        if st.button("🎉 가입 완료", use_container_width=True, type="primary"):
            if not agree_terms:
                st.error("이용약관에 동의해주세요.")
                return
            
            # 회원가입 처리
            auth_service = AuthService()
            
            # 디버그: 연결 상태 표시
            st.info(f"🔍 Supabase 연결 상태: {'연결됨' if auth_service.is_supabase_connected() else 'Mock 모드'}")
            
            success, message, user_id = auth_service.sign_up(data)
            
            if success:
                st.success(message)
                st.balloons()
                
                # 자동 로그인
                data['id'] = user_id
                data['is_paid'] = False
                data['is_admin'] = False
                SessionManager.login_user(data)
                
                # 가입 데이터 정리
                if 'signup_data' in st.session_state:
                    del st.session_state.signup_data
                if 'signup_step' in st.session_state:
                    del st.session_state.signup_step
                
                st.rerun()
            else:
                st.error(f"❌ 회원가입 실패: {message}")