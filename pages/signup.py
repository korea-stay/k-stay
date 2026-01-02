"""
K-Stay Signup Page
Phase 1: Universal Fact Collection (불변 정보 수집)
다국어 지원
"""

import streamlit as st
from datetime import datetime, date
from services.auth_service import AuthService, SessionManager
from utils.i18n import t, get_current_language


def render():
    """회원가입 페이지 렌더링"""
    
    # 헤더
    st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="
                font-size: 1.8rem;
                font-weight: 700;
                color: #1e293b;
            ">{t('signup.title')}</h2>
            <p style="color: #64748b; margin-top: 0.5rem; font-size: 0.9rem;">
                {t('signup.subtitle')}
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
        ("1", t('signup.step_account')),
        ("2", t('signup.step_personal')),
        ("3", t('signup.step_passport')),
        ("4", t('signup.step_contact')),
        ("5", t('signup.step_confirm'))
    ]
    
    cols = st.columns(len(steps))
    
    for i, (num, label) in enumerate(steps):
        with cols[i]:
            is_active = (i + 1) == current_step
            is_completed = (i + 1) < current_step
            
            if is_completed:
                color = "#22c55e"
                bg = "rgba(34, 197, 94, 0.15)"
                icon = "✓"
            elif is_active:
                color = "#2563eb"
                bg = "rgba(37, 99, 235, 0.15)"
                icon = num
            else:
                color = "#94a3b8"
                bg = "rgba(148, 163, 184, 0.1)"
                icon = num
            
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        width: 36px;
                        height: 36px;
                        border-radius: 50%;
                        background: {bg};
                        border: 2px solid {color};
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        color: {color};
                        font-weight: 700;
                        font-size: 0.85rem;
                        margin-bottom: 0.25rem;
                    ">{icon}</div>
                    <p style="color: {color}; font-size: 0.7rem; margin: 0;">{label}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_step1_account():
    """Step 1: 계정 정보"""
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #1e293b; margin: 0;">📧 {t('signup.account_info')}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input(
            f"{t('auth.email')} *",
            placeholder=t('auth.email_placeholder'),
            key="signup_email",
            value=st.session_state.get('signup_data', {}).get('email', '')
        )
    
    with col2:
        email_confirm = st.text_input(
            f"{t('auth.email_confirm')} *",
            placeholder=t('auth.email_confirm_placeholder'),
            key="signup_email_confirm"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        password = st.text_input(
            f"{t('auth.password')} *",
            type="password",
            placeholder=t('auth.password_placeholder'),
            key="signup_password"
        )
    
    with col4:
        password_confirm = st.text_input(
            f"{t('auth.password_confirm')} *",
            type="password",
            placeholder=t('auth.password_confirm_placeholder'),
            key="signup_password_confirm"
        )
    
    st.caption(t('signup.required_note'))
    
    col_prev, col_next = st.columns(2)
    
    with col_next:
        if st.button(t('common.next'), use_container_width=True, type="primary"):
            if not email or not password:
                st.error(t('signup.error_required'))
                return
            
            if email != email_confirm:
                st.error(t('signup.error_email_mismatch'))
                return
            
            if password != password_confirm:
                st.error(t('signup.error_password_mismatch'))
                return
            
            auth_service = AuthService()
            
            if not auth_service.validate_email(email):
                st.error(t('signup.error_invalid_email'))
                return
            
            is_valid, msg = auth_service.validate_password(password)
            if not is_valid:
                st.error(msg)
                return
            
            if 'signup_data' not in st.session_state:
                st.session_state.signup_data = {}
            
            st.session_state.signup_data['email'] = email
            st.session_state.signup_data['password'] = password
            st.session_state.signup_step = 2
            st.rerun()


def render_step2_personal():
    """Step 2: 인적 사항"""
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #1e293b; margin: 0 0 0.5rem 0;">👤 {t('signup.personal_info')}</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
                {t('signup.personal_info_desc')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        surname = st.text_input(
            f"{t('signup.surname')} *",
            placeholder="KIM",
            key="signup_surname",
            value=st.session_state.get('signup_data', {}).get('surname', '')
        )
    
    with col2:
        given_name = st.text_input(
            f"{t('signup.given_name')} *",
            placeholder="MINJUN",
            key="signup_given_name",
            value=st.session_state.get('signup_data', {}).get('given_name', '')
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        birth_date = st.date_input(
            f"{t('signup.birth_date')} *",
            min_value=date(1920, 1, 1),
            max_value=date.today(),
            value=date(1990, 1, 1),
            key="signup_birth_date"
        )
    
    with col4:
        current_lang = get_current_language()
        gender_options = ["", "Male", "Female"] if current_lang == "en" else ["", "남성 (Male)", "여성 (Female)"]
        gender = st.selectbox(
            f"{t('signup.gender')} *",
            options=gender_options,
            key="signup_gender"
        )
    
    col5, col6 = st.columns(2)
    
    with col5:
        nationality = st.text_input(
            f"{t('signup.nationality')} *",
            placeholder="USA, China, Vietnam...",
            key="signup_nationality",
            value=st.session_state.get('signup_data', {}).get('nationality', '')
        )
    
    with col6:
        alien_registration_no = st.text_input(
            t('signup.alien_reg_no'),
            placeholder=t('signup.alien_reg_placeholder'),
            key="signup_alien_reg",
            value=st.session_state.get('signup_data', {}).get('alien_registration_no', '')
        )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button(t('common.prev'), use_container_width=True):
            st.session_state.signup_step = 1
            st.rerun()
    
    with col_next:
        if st.button(t('common.next'), use_container_width=True, type="primary"):
            if not all([surname, given_name, gender, nationality]):
                st.error(t('signup.error_required'))
                return
            
            # 성별 값 정규화
            gender_value = gender
            if "남성" in gender or "Male" in gender:
                gender_value = "Male"
            elif "여성" in gender or "Female" in gender:
                gender_value = "Female"
            
            st.session_state.signup_data.update({
                'surname': surname.upper(),
                'given_name': given_name.upper(),
                'birth_date': birth_date.isoformat(),
                'gender': gender_value,
                'nationality': nationality.upper(),
                'alien_registration_no': alien_registration_no or '미소지'
            })
            st.session_state.signup_step = 3
            st.rerun()


def render_step3_passport():
    """Step 3: 여권 정보"""
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #1e293b; margin: 0;">📘 {t('signup.passport_info')}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    passport_no = st.text_input(
        f"{t('signup.passport_no')} *",
        placeholder="M12345678",
        key="signup_passport_no",
        value=st.session_state.get('signup_data', {}).get('passport_no', '')
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        passport_issue_date = st.date_input(
            f"{t('signup.issue_date')} *",
            min_value=date(2000, 1, 1),
            max_value=date.today(),
            key="signup_passport_issue"
        )
    
    with col2:
        passport_expiry_date = st.date_input(
            f"{t('signup.expiry_date')} *",
            min_value=date.today(),
            max_value=date(2040, 12, 31),
            key="signup_passport_expiry"
        )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button(t('common.prev'), use_container_width=True):
            st.session_state.signup_step = 2
            st.rerun()
    
    with col_next:
        if st.button(t('common.next'), use_container_width=True, type="primary"):
            if not passport_no:
                st.error(t('signup.error_required'))
                return
            
            if passport_expiry_date <= date.today():
                st.error(t('signup.error_passport_expired'))
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
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #1e293b; margin: 0;">📞 {t('signup.contact_info')}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"#### 🇰🇷 {t('signup.korea_contact')}")
    
    korea_address = st.text_input(
        f"{t('signup.korea_address')} *",
        placeholder=t('signup.korea_address_placeholder'),
        key="signup_korea_address",
        value=st.session_state.get('signup_data', {}).get('korea_address', '')
    )
    
    korea_phone = st.text_input(
        f"{t('signup.korea_phone')} *",
        placeholder="010-1234-5678",
        key="signup_korea_phone",
        value=st.session_state.get('signup_data', {}).get('korea_phone', '')
    )
    
    st.markdown(f"#### 🌍 {t('signup.home_contact')}")
    
    home_country_address = st.text_input(
        t('signup.home_address'),
        placeholder=t('signup.home_address_placeholder'),
        key="signup_home_address",
        value=st.session_state.get('signup_data', {}).get('home_country_address', '')
    )
    
    home_country_phone = st.text_input(
        t('signup.home_phone'),
        placeholder="+1-123-456-7890",
        key="signup_home_phone",
        value=st.session_state.get('signup_data', {}).get('home_country_phone', '')
    )
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button(t('common.prev'), use_container_width=True):
            st.session_state.signup_step = 3
            st.rerun()
    
    with col_next:
        if st.button(t('common.next'), use_container_width=True, type="primary"):
            if not korea_address or not korea_phone:
                st.error(t('signup.error_required'))
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
    
    auth_service = AuthService()
    if auth_service.is_supabase_connected():
        st.success(f"✅ {t('auth.supabase_connected')}")
    else:
        st.info(f"💡 {t('auth.test_mode')}")
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #1e293b; margin: 0 0 0.5rem 0;">✅ {t('signup.confirm_info')}</h4>
            <p style="color: #64748b; font-size: 0.85rem; margin: 0;">
                {t('signup.confirm_desc')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.get('signup_data', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📧 {t('signup.step_account')}**")
        st.write(f"{t('auth.email')}: {data.get('email', 'N/A')}")
        
        st.markdown(f"**👤 {t('signup.step_personal')}**")
        st.write(f"{t('signup.surname')}: {data.get('surname', '')} {data.get('given_name', '')}")
        st.write(f"{t('signup.birth_date')}: {data.get('birth_date', 'N/A')}")
        st.write(f"{t('signup.gender')}: {data.get('gender', 'N/A')}")
        st.write(f"{t('signup.nationality')}: {data.get('nationality', 'N/A')}")
    
    with col2:
        st.markdown(f"**📘 {t('signup.step_passport')}**")
        st.write(f"{t('signup.passport_no')}: {data.get('passport_no', 'N/A')}")
        st.write(f"{t('signup.issue_date')}: {data.get('passport_issue_date', 'N/A')}")
        st.write(f"{t('signup.expiry_date')}: {data.get('passport_expiry_date', 'N/A')}")
        
        st.markdown(f"**📞 {t('signup.step_contact')}**")
        st.write(f"{t('signup.korea_address')}: {data.get('korea_address', 'N/A')}")
        st.write(f"{t('signup.korea_phone')}: {data.get('korea_phone', 'N/A')}")
    
    st.markdown("---")
    
    agree_terms = st.checkbox(t('signup.terms_agree'), key="agree_terms")
    agree_marketing = st.checkbox(t('signup.marketing_agree'), key="agree_marketing")
    
    col_prev, col_next = st.columns(2)
    
    with col_prev:
        if st.button(t('common.prev'), use_container_width=True):
            st.session_state.signup_step = 4
            st.rerun()
    
    with col_next:
        if st.button(f"🎉 {t('signup.complete_btn')}", use_container_width=True, type="primary"):
            if not agree_terms:
                st.error(t('signup.error_terms'))
                return
            
            auth_service = AuthService()
            success, message, user_id = auth_service.sign_up(data)
            
            if success:
                st.success(t('signup.success'))
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
                if 'auth_page' in st.session_state:
                    del st.session_state.auth_page
                
                st.rerun()
            else:
                st.error(f"❌ {message}")