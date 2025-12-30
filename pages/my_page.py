"""
K-Stay My Page
회원정보 조회 및 수정
"""

import streamlit as st
from datetime import date, datetime
from services.auth_service import AuthService, SessionManager


def render():
    """마이페이지 렌더링"""
    
    st.markdown("## 👤 마이페이지")
    st.markdown("회원정보를 확인하고 수정할 수 있습니다.")
    
    st.markdown("---")
    
    # 현재 사용자 정보
    user_data = st.session_state.get('user_data', {})
    user_email = st.session_state.get('user_email', '')
    
    if not user_data:
        st.warning("로그인이 필요합니다.")
        return
    
    # 비밀번호 확인 상태
    password_verified = st.session_state.get('password_verified', False)
    
    if not password_verified:
        render_password_verification(user_email)
    else:
        render_profile_edit_form(user_data)


def render_password_verification(user_email: str):
    """비밀번호 확인 단계"""
    
    st.markdown("""
        <div style="
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <p style="margin: 0; color: #92400e;">
                🔐 회원정보를 수정하려면 비밀번호를 다시 입력해주세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("password_verify_form"):
            st.markdown(f"**이메일**: {user_email}")
            
            password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="현재 비밀번호를 입력하세요"
            )
            
            submitted = st.form_submit_button("확인", use_container_width=True, type="primary")
            
            if submitted:
                if not password:
                    st.error("비밀번호를 입력해주세요.")
                else:
                    auth_service = AuthService()
                    success, message, user_data = auth_service.sign_in(user_email, password)
                    
                    if success:
                        # 로그인 성공 시 세션 데이터 갱신 (DB에서 최신 데이터)
                        st.session_state.user_data = user_data
                        st.session_state.password_verified = True
                        st.success("비밀번호가 확인되었습니다.")
                        st.rerun()
                    else:
                        st.error("비밀번호가 일치하지 않습니다.")


def render_profile_edit_form(user_data: dict):
    """회원정보 수정 폼"""
    
    st.markdown("""
        <div style="
            background: #dcfce7;
            border: 1px solid #22c55e;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <p style="margin: 0; color: #166534;">
                ✅ 비밀번호가 확인되었습니다. 회원정보를 수정할 수 있습니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 수정 불가 필드 표시
    st.markdown("### 📧 계정 정보")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("이메일", value=user_data.get('email', ''), disabled=True)
    with col2:
        st.text_input("가입일", value=format_date(user_data.get('created_at', '')), disabled=True)
    
    st.markdown("---")
    
    # 수정 가능 필드
    with st.form("profile_edit_form"):
        
        # 인적사항
        st.markdown("### 👤 인적사항")
        
        col1, col2 = st.columns(2)
        with col1:
            surname = st.text_input(
                "성 (Surname) *",
                value=user_data.get('surname', ''),
                placeholder="HONG"
            )
        with col2:
            given_name = st.text_input(
                "이름 (Given Name) *",
                value=user_data.get('given_name', ''),
                placeholder="GILDONG"
            )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            birth_date_value = parse_date(user_data.get('birth_date'))
            birth_date = st.date_input(
                "생년월일 *",
                value=birth_date_value,
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
        with col2:
            gender_options = ["Male", "Female"]
            current_gender = user_data.get('gender', 'Male')
            gender_index = gender_options.index(current_gender) if current_gender in gender_options else 0
            gender = st.selectbox("성별 *", gender_options, index=gender_index)
        with col3:
            nationality = st.text_input(
                "국적 *",
                value=user_data.get('nationality', ''),
                placeholder="USA"
            )
        
        alien_registration_no = st.text_input(
            "외국인등록번호",
            value=user_data.get('alien_registration_no', '') or '',
            placeholder="000000-0000000"
        )
        
        st.markdown("---")
        
        # 여권정보
        st.markdown("### 🛂 여권정보")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            passport_no = st.text_input(
                "여권번호 *",
                value=user_data.get('passport_no', ''),
                placeholder="M12345678"
            )
        with col2:
            passport_issue_value = parse_date(user_data.get('passport_issue_date'))
            passport_issue_date = st.date_input(
                "여권 발급일",
                value=passport_issue_value,
                min_value=date(1990, 1, 1),
                max_value=date.today()
            )
        with col3:
            passport_expiry_value = parse_date(user_data.get('passport_expiry_date'))
            if passport_expiry_value is None:
                passport_expiry_value = date.today()
            passport_expiry_date = st.date_input(
                "여권 만료일 *",
                value=passport_expiry_value,
                min_value=date.today()
            )
        
        st.markdown("---")
        
        # 연락처 정보
        st.markdown("### 📞 연락처 정보")
        
        st.markdown("**한국 내 연락처**")
        korea_address = st.text_area(
            "한국 주소 *",
            value=user_data.get('korea_address', '') or '',
            placeholder="서울시 강남구 테헤란로 123, 101호",
            height=80
        )
        korea_phone = st.text_input(
            "한국 전화번호 *",
            value=user_data.get('korea_phone', '') or '',
            placeholder="010-1234-5678"
        )
        
        st.markdown("**본국 연락처**")
        home_country_address = st.text_area(
            "본국 주소",
            value=user_data.get('home_country_address', '') or '',
            placeholder="123 Main St, City, Country",
            height=80
        )
        home_country_phone = st.text_input(
            "본국 전화번호",
            value=user_data.get('home_country_phone', '') or '',
            placeholder="+1-234-567-8900"
        )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button("✅ 정보 수정하기", use_container_width=True, type="primary")
        
        if submitted:
            if not all([surname, given_name, nationality, passport_no, korea_address, korea_phone]):
                st.error("필수 항목(*)을 모두 입력해주세요.")
            else:
                # 업데이트 데이터 구성
                update_data = {
                    'surname': surname.strip().upper(),
                    'given_name': given_name.strip().upper(),
                    'birth_date': birth_date.isoformat() if birth_date else None,
                    'gender': gender,
                    'nationality': nationality.strip().upper(),
                    'alien_registration_no': alien_registration_no.strip() if alien_registration_no else None,
                    'passport_no': passport_no.strip().upper(),
                    'passport_issue_date': passport_issue_date.isoformat() if passport_issue_date else None,
                    'passport_expiry_date': passport_expiry_date.isoformat() if passport_expiry_date else None,
                    'korea_address': korea_address.strip(),
                    'korea_phone': korea_phone.strip(),
                    'home_country_address': home_country_address.strip() if home_country_address else None,
                    'home_country_phone': home_country_phone.strip() if home_country_phone else None,
                }
                
                auth_service = AuthService()
                user_id = st.session_state.get('user_id')
                
                success, message = auth_service.update_user_profile(user_id, update_data)
                
                if success:
                    # DB에서 최신 데이터 다시 가져오기
                    updated_user_data = auth_service.get_user_profile(user_id)
                    if updated_user_data:
                        st.session_state.user_data = updated_user_data
                    else:
                        # DB 조회 실패 시 로컬 데이터만 업데이트
                        st.session_state.user_data.update(update_data)
                    
                    st.success("✅ 회원정보가 성공적으로 수정되었습니다!")
                    st.balloons()
                else:
                    st.error(f"수정 실패: {message}")
                    
                    # 디버그 정보 표시
                    with st.expander("🔍 디버그 정보"):
                        st.write("**User ID:**", user_id)
                        st.write("**업데이트 시도 데이터:**")
                        st.json(update_data)
                        st.warning("""
                        **RLS 정책 문제일 수 있습니다.**
                        
                        Supabase SQL Editor에서 다음 명령어를 실행해보세요:
                        ```sql
                        -- RLS 비활성화 (개발용)
                        ALTER TABLE users DISABLE ROW LEVEL SECURITY;
                        
                        -- 또는 정책 수정
                        DROP POLICY IF EXISTS "Users can update own data" ON users;
                        CREATE POLICY "Users can update own data" ON users
                            FOR UPDATE USING (true);
                        ```
                        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔒 비밀번호 확인 취소", use_container_width=False):
        st.session_state.password_verified = False
        st.rerun()


def parse_date(date_value):
    """날짜 문자열을 date 객체로 변환"""
    if date_value is None:
        return None
    
    if isinstance(date_value, date):
        return date_value
    
    if isinstance(date_value, str):
        try:
            if 'T' in date_value:
                return datetime.fromisoformat(date_value.replace('Z', '')).date()
            else:
                return datetime.strptime(date_value[:10], '%Y-%m-%d').date()
        except:
            return None
    
    return None


def format_date(date_value):
    """날짜를 보기 좋은 형식으로 변환"""
    if not date_value:
        return "-"
    
    parsed = parse_date(date_value)
    if parsed:
        return parsed.strftime('%Y년 %m월 %d일')
    
    return str(date_value)[:10]