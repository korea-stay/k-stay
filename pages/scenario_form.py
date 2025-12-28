"""
K-Stay Scenario Form Page
3-Phase Architecture:
- Phase 1: Universal Fact (불변 정보) - 회원가입 시 입력, 확인 후 다음 단계
- Phase 2: Variable Fact (가변 정보) - 시나리오별 Smart Form
- Phase 3: Narrative (정성 사연) - AI Active 검토 & 코칭
"""

import streamlit as st
from datetime import date
from config.settings import SCENARIOS
from services.ai_service import AIService, RAGService


def render():
    """시나리오 폼 페이지 렌더링"""
    
    scenario_id = st.session_state.get('selected_scenario')
    
    if not scenario_id:
        st.warning("시나리오를 먼저 선택해주세요.")
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    if not scenario:
        st.error("유효하지 않은 시나리오입니다.")
        return
    
    current_step = st.session_state.get('form_step', 1)
    
    # 상단 Phase 진행 표시
    render_phase_indicator(current_step)
    
    if current_step == 1:
        render_phase1_universal_fact(scenario)
    elif current_step == 2:
        render_phase2_variable_fact(scenario)
    elif current_step == 3:
        render_phase3_narrative(scenario)


def render_phase_indicator(current_step):
    """3-Phase 진행 상태 표시 - 파스텔 톤"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Phase 1: Universal Fact
        is_active = current_step == 1
        is_done = current_step > 1
        
        if is_active:
            bg_color = "#dcfce7"  # 연한 초록 (active)
            border_color = "#22c55e"
            title_color = "#166534"
            desc_color = "#15803d"
            badge_bg = "#22c55e"
            badge_text = "● PHASE 1"
            shadow = "box-shadow: 0 4px 12px rgba(34, 197, 94, 0.25);"
        elif is_done:
            bg_color = "#f0fdf4"  # 더 연한 초록 (done)
            border_color = "#86efac"
            title_color = "#166534"
            desc_color = "#22c55e"
            badge_bg = "#22c55e"
            badge_text = "✓ PHASE 1"
            shadow = ""
        else:
            bg_color = "#f1f5f9"  # 회색 (inactive)
            border_color = "#cbd5e1"
            title_color = "#64748b"
            desc_color = "#94a3b8"
            badge_bg = "#94a3b8"
            badge_text = "PHASE 1"
            shadow = ""
        
        st.markdown(f"""
            <div style="
                background: {bg_color};
                border-radius: 0.75rem;
                padding: 1.25rem;
                border: 2px solid {border_color};
                min-height: 120px;
                {shadow}
            ">
                <div style="
                    background: {badge_bg};
                    color: white;
                    font-size: 0.7rem;
                    font-weight: 700;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.25rem;
                    display: inline-block;
                    margin-bottom: 0.5rem;
                ">{badge_text}</div>
                <h3 style="
                    color: {title_color};
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0.5rem 0 0.25rem 0;
                ">Universal Fact</h3>
                <p style="color: {desc_color}; font-size: 0.8rem; margin: 0;">
                    불변 정보 확인
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Phase 2: Variable Fact
        is_active = current_step == 2
        is_done = current_step > 2
        
        if is_active:
            bg_color = "#dbeafe"  # 연한 파랑 (active)
            border_color = "#3b82f6"
            title_color = "#1e40af"
            desc_color = "#2563eb"
            badge_bg = "#3b82f6"
            badge_text = "● PHASE 2"
            shadow = "box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);"
        elif is_done:
            bg_color = "#eff6ff"  # 더 연한 파랑 (done)
            border_color = "#93c5fd"
            title_color = "#1e40af"
            desc_color = "#3b82f6"
            badge_bg = "#22c55e"
            badge_text = "✓ PHASE 2"
            shadow = ""
        else:
            bg_color = "#f1f5f9"  # 회색 (inactive)
            border_color = "#cbd5e1"
            title_color = "#64748b"
            desc_color = "#94a3b8"
            badge_bg = "#94a3b8"
            badge_text = "PHASE 2"
            shadow = ""
        
        st.markdown(f"""
            <div style="
                background: {bg_color};
                border-radius: 0.75rem;
                padding: 1.25rem;
                border: 2px solid {border_color};
                min-height: 120px;
                {shadow}
            ">
                <div style="
                    background: {badge_bg};
                    color: white;
                    font-size: 0.7rem;
                    font-weight: 700;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.25rem;
                    display: inline-block;
                    margin-bottom: 0.5rem;
                ">{badge_text}</div>
                <h3 style="
                    color: {title_color};
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0.5rem 0 0.25rem 0;
                ">Variable Fact</h3>
                <p style="color: {desc_color}; font-size: 0.8rem; margin: 0;">
                    가변 정보 입력
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Phase 3: Narrative
        is_active = current_step == 3
        is_done = current_step > 3
        
        if is_active:
            bg_color = "#f3e8ff"  # 연한 보라 (active)
            border_color = "#a855f7"
            title_color = "#6b21a8"
            desc_color = "#7c3aed"
            badge_bg = "#a855f7"
            badge_text = "● PHASE 3"
            shadow = "box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25);"
        elif is_done:
            bg_color = "#faf5ff"  # 더 연한 보라 (done)
            border_color = "#c4b5fd"
            title_color = "#6b21a8"
            desc_color = "#a855f7"
            badge_bg = "#22c55e"
            badge_text = "✓ PHASE 3"
            shadow = ""
        else:
            bg_color = "#f1f5f9"  # 회색 (inactive)
            border_color = "#cbd5e1"
            title_color = "#64748b"
            desc_color = "#94a3b8"
            badge_bg = "#94a3b8"
            badge_text = "PHASE 3"
            shadow = ""
        
        st.markdown(f"""
            <div style="
                background: {bg_color};
                border-radius: 0.75rem;
                padding: 1.25rem;
                border: 2px solid {border_color};
                min-height: 120px;
                {shadow}
            ">
                <div style="
                    background: {badge_bg};
                    color: white;
                    font-size: 0.7rem;
                    font-weight: 700;
                    padding: 0.25rem 0.5rem;
                    border-radius: 0.25rem;
                    display: inline-block;
                    margin-bottom: 0.5rem;
                ">{badge_text}</div>
                <h3 style="
                    color: {title_color};
                    font-size: 1.1rem;
                    font-weight: 700;
                    margin: 0.5rem 0 0.25rem 0;
                    font-style: italic;
                ">Narrative</h3>
                <p style="color: {desc_color}; font-size: 0.8rem; margin: 0;">
                    정성 사연
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_phase1_universal_fact(scenario):
    """Phase 1: Universal Fact - 회원가입 시 입력된 불변 정보 확인"""
    
    user_data = st.session_state.get('user_data', {})
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            ">
                <span style="font-size: 1.5rem;">{scenario.icon}</span>
                <h2 style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0;
                ">{scenario.name} ({scenario.visa_type})</h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                회원가입 시 입력한 기본 정보를 확인해주세요. (Form + DB Only)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 뒤로가기
    if st.button("← 다른 시나리오 선택"):
        st.session_state.selected_scenario = None
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Universal Fact 카드
    st.markdown("""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
                padding-bottom: 0.75rem;
                border-bottom: 1px solid #f1f5f9;
            ">
                <span style="font-size: 1.1rem;">🗂️</span>
                <h3 style="
                    font-size: 1rem;
                    font-weight: 600;
                    color: #1e293b;
                    margin: 0;
                ">Universal Fact (불변 정보)</h3>
                <span style="
                    background: #dcfce7;
                    color: #166534;
                    font-size: 0.7rem;
                    font-weight: 500;
                    padding: 0.125rem 0.5rem;
                    border-radius: 1rem;
                    margin-left: auto;
                ">회원가입 시 입력 완료</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 정보 표시 - 4개 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. 계정 정보
        st.markdown("""
            <div style="
                background: #f8fafc;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                    1. 계정
                </h4>
        """, unsafe_allow_html=True)
        
        email = user_data.get('email', 'user@example.com')
        st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">이메일</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{email}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748b; font-size: 0.85rem;">비밀번호</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">••••••••</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. 여권 정보
        st.markdown("""
            <div style="
                background: #f8fafc;
                border-radius: 0.5rem;
                padding: 1rem;
            ">
                <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                    3. 여권
                </h4>
        """, unsafe_allow_html=True)
        
        passport_no = user_data.get('passport_no', 'M12345678')
        issue_date = user_data.get('passport_issue_date', '2020-01-15')
        expiry_date = user_data.get('passport_expiry_date', '2030-01-14')
        
        st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">여권번호</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{passport_no}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">발급일</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{issue_date}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748b; font-size: 0.85rem;">만료일</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{expiry_date}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 2. 인적사항
        st.markdown("""
            <div style="
                background: #f8fafc;
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                    2. 인적사항
                </h4>
        """, unsafe_allow_html=True)
        
        surname = user_data.get('surname', 'HONG')
        given_name = user_data.get('given_name', 'GILDONG')
        birth_date = user_data.get('birth_date', '1990-01-01')
        gender = user_data.get('gender', '남성')
        nationality = user_data.get('nationality', 'USA')
        alien_reg_no = user_data.get('alien_registration_no', '901234-5678901')
        
        st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">성명</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{surname} {given_name}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">생년월일</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{birth_date}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">성별</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{gender}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">국적</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{nationality}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748b; font-size: 0.85rem;">외국인등록번호</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{alien_reg_no}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 4. 연락처
        st.markdown("""
            <div style="
                background: #f8fafc;
                border-radius: 0.5rem;
                padding: 1rem;
            ">
                <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                    4. 연락처
                </h4>
        """, unsafe_allow_html=True)
        
        korea_address = user_data.get('korea_address', '서울시 강남구 테헤란로 123')
        home_address = user_data.get('home_country_address', '123 Main St, New York, USA')
        phone = user_data.get('phone', '010-1234-5678')
        
        st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">한국 주소</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem; text-align: right; max-width: 60%;">{korea_address}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: #64748b; font-size: 0.85rem;">본국 주소</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem; text-align: right; max-width: 60%;">{home_address}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748b; font-size: 0.85rem;">전화번호</span>
                    <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{phone}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 안내 메시지
    st.markdown("""
        <div style="
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                <span style="font-size: 1rem;">ℹ️</span>
                <div>
                    <p style="color: #1e40af; font-size: 0.85rem; margin: 0; font-weight: 500;">
                        위 정보는 통합신청서의 기본 인적사항(상단)에 자동으로 채워집니다.
                    </p>
                    <p style="color: #3b82f6; font-size: 0.8rem; margin: 0.25rem 0 0 0;">
                        정보 수정이 필요하면 <a href="#" style="color: #1e40af; text-decoration: underline;">마이페이지</a>에서 변경해주세요.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 다음 단계 버튼
    if st.button("정보 확인 완료 → Phase 2 시작", type="primary", use_container_width=True):
        st.session_state.form_step = 2
        st.rerun()


def render_phase2_variable_fact(scenario):
    """Phase 2: Variable Fact - 시나리오별 가변 정보 입력"""
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            ">
                <span style="font-size: 1.5rem;">{scenario.icon}</span>
                <h2 style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0;
                ">{scenario.name} ({scenario.visa_type})</h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                시나리오별로 달라지는 정보를 입력해주세요. (Form + JSONB 저장)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 뒤로가기
    if st.button("← Phase 1로 돌아가기"):
        st.session_state.form_step = 1
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Smart Form 헤더
    st.markdown("""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem 0.75rem 0 0;
            padding: 1rem 1.5rem;
            border-bottom: none;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 1.1rem;">📋</span>
                <h3 style="
                    font-size: 1rem;
                    font-weight: 600;
                    color: #1e293b;
                    margin: 0;
                ">Smart Form (Variable Fact)</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 폼 컨테이너
    with st.form("phase2_form"):
        # 시나리오별 동적 필드 렌더링
        render_scenario_fields(scenario)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "다음: AI 코칭 시작 (Phase 3) →",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # 폼 데이터 저장
            save_form_data(scenario)
            
            # Phase 3로 이동
            st.session_state.form_step = 3
            
            # AI 초기 메시지 설정
            init_ai_chat(scenario)
            
            st.rerun()


def render_scenario_fields(scenario):
    """시나리오별 동적 폼 필드 렌더링"""
    
    user_data = st.session_state.get('user_data', {})
    
    # 시나리오 A: 구직 (D-10)
    if scenario.id == "A":
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("최종 학력", ["학사", "석사", "박사", "기타"], key="education_level")
            st.text_input("전공", key="major", placeholder="예: 컴퓨터공학")
            st.date_input("졸업일", key="graduation_date")
        with col2:
            st.text_input("희망 산업", key="target_industry", placeholder="예: IT/소프트웨어")
            st.text_input("희망 직무", key="target_position", placeholder="예: 백엔드 개발자")
            st.text_area("보유 자격증", key="certificates", placeholder="예: 정보처리기사, SQLD")
        
        st.markdown("---")
        st.markdown("**🏠 숙소 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.text_input("숙소 제공인 성명", key="housing_provider_name")
            st.text_input("숙소 제공인 연락처", key="housing_provider_phone")
        with col4:
            st.text_input("거주지 주소", key="housing_address")
    
    # 시나리오 B: 아르바이트 (시간제)
    elif scenario.id == "B":
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("학교명", key="school_name", placeholder="예: 서울대학교")
            st.selectbox("재학 상태", ["재학중", "휴학중", "수료"], key="student_status")
            st.text_input("현재 학기", key="semester", placeholder="예: 3학년 2학기")
        with col2:
            st.number_input("평균 성적 (GPA)", key="gpa", min_value=0.0, max_value=4.5, step=0.1)
        
        st.markdown("---")
        st.markdown("**💼 고용주 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.text_input("고용주 상호", key="employer_name")
            st.text_input("사업자등록번호", key="employer_business_no")
            st.text_input("대표자명", key="employer_representative")
        with col4:
            st.text_input("고용주 연락처", key="employer_phone")
            st.text_input("근무지 주소", key="work_address")
        
        st.markdown("---")
        st.markdown("**⏰ 근무 조건**")
        col5, col6 = st.columns(2)
        with col5:
            st.number_input("시급 (원)", key="hourly_wage", min_value=9860, step=100)
            st.number_input("주당 근무시간", key="weekly_hours", min_value=1, max_value=20)
        with col6:
            st.date_input("근무 시작일", key="work_period_start")
            st.date_input("근무 종료일", key="work_period_end")
    
    # 시나리오 C: 결혼 이민 (F-6)
    elif scenario.id == "C":
        st.markdown("**💍 배우자 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("배우자 성명", key="spouse_name")
            st.text_input("배우자 주민등록번호", key="spouse_resident_no")
            st.text_input("배우자 연락처", key="spouse_phone")
        with col2:
            st.text_input("배우자 직업", key="spouse_occupation")
            st.number_input("배우자 연 소득 (만원)", key="spouse_income", min_value=0)
        
        st.markdown("---")
        st.markdown("**📅 혼인 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.date_input("혼인신고일", key="marriage_date")
            st.text_input("혼인신고 장소", key="marriage_location")
        with col4:
            st.selectbox("주거 형태", ["자가", "전세", "월세", "기타"], key="residence_type")
        
        st.markdown("---")
        st.markdown("**💕 첫 만남**")
        col5, col6 = st.columns(2)
        with col5:
            st.date_input("첫 만남 시기", key="first_meeting_date")
        with col6:
            st.text_input("첫 만남 장소", key="first_meeting_location")
    
    # 시나리오 D: 가족 초청 (F-1-5)
    elif scenario.id == "D":
        st.markdown("**👨‍👩‍👧 피초청인 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("피초청인 성명", key="invitee_name")
            st.selectbox("관계", ["부", "모", "형제", "자녀", "기타"], key="invitee_relation")
            st.date_input("피초청인 생년월일", key="invitee_birth_date")
        with col2:
            st.text_input("피초청인 여권번호", key="invitee_passport_no")
            st.text_input("피초청인 본국 주소", key="invitee_address")
        
        st.markdown("---")
        st.markdown("**📋 초청 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.selectbox("초청 목적", ["방문", "요양", "가족 돌봄", "기타"], key="invitation_purpose")
            st.text_input("예정 체류 기간", key="stay_period", placeholder="예: 6개월")
        with col4:
            st.number_input("초청인 연 소득 (만원)", key="inviter_income", min_value=0)
            st.number_input("초청인 자산 (만원)", key="inviter_assets", min_value=0)
    
    # 시나리오 E: 전문 인력 (E-7)
    elif scenario.id == "E":
        st.markdown("**🏢 기업 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("기업명", key="company_name")
            st.text_input("사업자등록번호", key="company_business_no")
            st.text_input("기업 주소", key="company_address")
        with col2:
            st.text_input("업종", key="company_industry")
            st.number_input("상시 근로자 수", key="company_employees", min_value=1)
        
        st.markdown("---")
        st.markdown("**👔 채용 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.text_input("채용 직위", key="position_title")
            st.number_input("연봉 (만원)", key="annual_salary", min_value=0)
            st.text_input("계약 기간", key="contract_period")
        with col4:
            st.text_area("담당 업무", key="position_duties")
        
        st.markdown("---")
        st.markdown("**🌏 외국인 정보**")
        col5, col6 = st.columns(2)
        with col5:
            st.text_input("외국인 성명", key="foreigner_name")
            st.text_input("외국인 국적", key="foreigner_nationality")
        with col6:
            st.text_input("외국인 학력", key="foreigner_education")
            st.number_input("외국인 경력 (년)", key="foreigner_experience", min_value=0)
    
    # 시나리오 F: 국적 귀화
    elif scenario.id == "F":
        st.markdown("**🇰🇷 한국 체류 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("한국 거주 기간 (년)", key="korea_stay_years", min_value=0)
            st.date_input("최초 입국일", key="first_entry_date")
            st.text_input("현재 체류자격", key="current_visa_type")
        with col2:
            st.selectbox("범죄 이력", ["없음", "있음"], key="criminal_record")
            st.selectbox("한국어 능력", ["TOPIK 1급", "TOPIK 2급", "TOPIK 3급", "TOPIK 4급", "TOPIK 5급", "TOPIK 6급", "사회통합프로그램 이수"], key="korean_language_level")
        
        st.markdown("---")
        st.markdown("**👨‍👩‍👧 가족 및 재정**")
        col3, col4 = st.columns(2)
        with col3:
            st.selectbox("한국인 배우자 유무", ["있음", "없음"], key="korean_spouse")
            st.number_input("한국 내 자녀 수", key="children_in_korea", min_value=0)
        with col4:
            st.number_input("보유 재산 (만원)", key="property_value", min_value=0)
            st.number_input("연 소득 (만원)", key="annual_income", min_value=0)


def save_form_data(scenario):
    """폼 데이터 세션에 저장"""
    form_data = {}
    
    # 모든 session_state에서 form 관련 키 추출
    form_keys = [
        'education_level', 'major', 'graduation_date', 'target_industry', 
        'target_position', 'certificates', 'housing_provider_name', 
        'housing_provider_phone', 'housing_address',
        'school_name', 'student_status', 'semester', 'gpa',
        'employer_name', 'employer_business_no', 'employer_representative',
        'employer_phone', 'work_address', 'hourly_wage', 'weekly_hours',
        'work_period_start', 'work_period_end',
        'spouse_name', 'spouse_resident_no', 'spouse_phone', 'spouse_occupation',
        'spouse_income', 'marriage_date', 'marriage_location', 'residence_type',
        'first_meeting_date', 'first_meeting_location',
        'invitee_name', 'invitee_relation', 'invitee_birth_date', 
        'invitee_passport_no', 'invitee_address', 'invitation_purpose',
        'stay_period', 'inviter_income', 'inviter_assets',
        'company_name', 'company_business_no', 'company_address',
        'company_industry', 'company_employees', 'position_title',
        'annual_salary', 'contract_period', 'position_duties',
        'foreigner_name', 'foreigner_nationality', 'foreigner_education',
        'foreigner_experience',
        'korea_stay_years', 'first_entry_date', 'current_visa_type',
        'criminal_record', 'korean_language_level', 'korean_spouse',
        'children_in_korea', 'property_value', 'annual_income'
    ]
    
    for key in form_keys:
        if key in st.session_state:
            value = st.session_state[key]
            if hasattr(value, 'strftime'):
                value = value.strftime('%Y-%m-%d')
            form_data[key] = value
    
    st.session_state.form_data = form_data


def init_ai_chat(scenario):
    """AI 채팅 초기화"""
    prompts = scenario.ai_prompts
    narrative_label = prompts.get('narrative_label', '상세 내용')
    
    initial_message = {
        'role': 'assistant',
        'content': f"""안녕하세요! {scenario.name} 서류 작성을 도와드리는 AI 코치입니다. 🤖

지금부터 **{narrative_label}**을 함께 작성해볼게요.

저는 단순히 글을 써주는 게 아니라, 작성하신 내용의 **법적/행정적 리스크**를 실시간으로 검토하고 수정을 제안합니다.

먼저 질문 드릴게요:
{get_first_question(scenario)}"""
    }
    
    st.session_state.chat_history = [initial_message]


def get_first_question(scenario):
    """시나리오별 첫 질문"""
    questions = {
        "A": "월별 구체적인 구직 활동 계획이 어떻게 되시나요? (예: 1월 - OO기업 지원, 2월 - 면접 준비 등)",
        "B": "담당하게 될 업무를 구체적으로 설명해주시겠어요?",
        "C": "배우자분과 첫 만남부터 결혼까지의 과정을 진솔하게 말씀해주시겠어요?",
        "D": "부모님을 초청해야 하는 인도적 사유가 무엇인가요?",
        "E": "이 외국인 인력을 꼭 채용해야 하는 이유와 기대 효과를 설명해주세요.",
        "F": "한국 국적을 취득하고자 하는 동기와 한국 사회에 기여할 계획을 말씀해주세요."
    }
    return questions.get(scenario.id, "어떤 내용을 작성하고 싶으신가요?")


def render_phase3_narrative(scenario):
    """Phase 3: Narrative - 자소서 형식 + AI 실시간 검토"""
    
    # 시나리오별 질문 목록 가져오기
    questions = get_narrative_questions(scenario.id)
    
    # narrative_answers 초기화
    if 'narrative_answers' not in st.session_state:
        st.session_state.narrative_answers = {}
    
    # AI 피드백 저장소 초기화
    if 'ai_feedbacks' not in st.session_state:
        st.session_state.ai_feedbacks = []
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            ">
                <span style="font-size: 1.5rem;">📝</span>
                <h2 style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0;
                ">{scenario.name} - 사연 작성</h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                각 질문에 대해 상세히 작성해주세요. AI가 실시간으로 내용을 검토합니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2단 레이아웃
    form_col, feedback_col = st.columns([2, 1])
    
    with form_col:
        # 자소서 형식 폼 헤더
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
                border-radius: 0.75rem;
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 1.25rem;">✍️</span>
                <span style="font-weight: 600; color: white; font-size: 0.95rem;">
                    {scenario.ai_prompts.get('narrative_label', '상세 내용 작성')}
                </span>
                <span style="
                    background: rgba(255,255,255,0.2);
                    color: white;
                    font-size: 0.7rem;
                    padding: 0.125rem 0.5rem;
                    border-radius: 1rem;
                    margin-left: auto;
                ">{len(questions)}개 항목</span>
            </div>
        """, unsafe_allow_html=True)
        
        # 각 질문에 대한 입력 필드 - Streamlit 네이티브 사용
        for i, q in enumerate(questions):
            q_id = q['id']
            q_title = q['title']
            q_hint = q['hint']
            q_placeholder = q['placeholder']
            q_required = q.get('required', False)
            
            # 구분선 (첫 번째 제외)
            if i > 0:
                st.divider()
            
            # 질문 번호와 제목을 Streamlit 컴포넌트로 표시
            required_text = " *필수" if q_required else ""
            st.markdown(f"**Q{i+1}. {q_title}**{required_text}")
            st.caption(q_hint)
            
            # 텍스트 입력 영역
            current_value = st.session_state.narrative_answers.get(q_id, '')
            
            answer = st.text_area(
                f"답변 {i+1}",
                value=current_value,
                height=120,
                key=f"narrative_{q_id}",
                placeholder=q_placeholder,
                label_visibility="collapsed"
            )
            
            # 답변 저장
            st.session_state.narrative_answers[q_id] = answer
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI 검토 요청 버튼
        col_validate, col_empty = st.columns([1, 1])
        with col_validate:
            if st.button("🤖 AI 검토 요청", use_container_width=True):
                # AI 검토 실행
                run_ai_validation(scenario, questions)
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 하단 버튼들
        col_back, col_next = st.columns(2)
        
        with col_back:
            if st.button("← Phase 2로 돌아가기", use_container_width=True):
                st.session_state.form_step = 2
                st.rerun()
        
        with col_next:
            if st.button("✓ 작성 완료 → 문서 생성", use_container_width=True, type="primary"):
                # 필수 항목 검증
                missing_required = []
                for q in questions:
                    if q.get('required', False):
                        answer = st.session_state.narrative_answers.get(q['id'], '')
                        if len(answer) < q.get('min_chars', 100):
                            missing_required.append(q['title'])
                
                if missing_required:
                    st.error(f"필수 항목을 작성해주세요: {', '.join(missing_required)}")
                else:
                    from services.document_service import DocumentService
                    
                    doc_service = DocumentService()
                    zip_bytes = doc_service.generate_full_package(
                        scenario.id,
                        st.session_state.get('user_data', {}),
                        st.session_state.get('form_data', {}),
                        {'narrative_answers': st.session_state.narrative_answers}
                    )
                    
                    if zip_bytes:
                        st.session_state.generated_zip = zip_bytes
                        st.session_state.current_page = 'document_preview'
                        st.rerun()
    
    with feedback_col:
        # AI Validator 피드백 패널
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                border: 1px solid #fecaca;
                border-radius: 0.75rem;
                padding: 1.25rem;
                margin-bottom: 1rem;
            ">
                <h4 style="
                    font-weight: 700;
                    color: #dc2626;
                    font-size: 0.9rem;
                    margin: 0 0 0.75rem 0;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                ">🧠 AI Validator 피드백</h4>
        """, unsafe_allow_html=True)
        
        # 피드백 목록 표시
        feedbacks = st.session_state.get('ai_feedbacks', [])
        
        if feedbacks:
            for fb in feedbacks:
                fb_type = fb.get('type', 'info')
                if fb_type == 'warning':
                    icon = "⚠️"
                    bg = "#fef3c7"
                    border = "#fcd34d"
                    text_color = "#92400e"
                elif fb_type == 'error':
                    icon = "❌"
                    bg = "#fee2e2"
                    border = "#fca5a5"
                    text_color = "#991b1b"
                elif fb_type == 'success':
                    icon = "✅"
                    bg = "#dcfce7"
                    border = "#86efac"
                    text_color = "#166534"
                else:
                    icon = "💡"
                    bg = "#dbeafe"
                    border = "#93c5fd"
                    text_color = "#1e40af"
                
                st.markdown(f"""
                    <div style="
                        background: {bg};
                        border: 1px solid {border};
                        border-radius: 0.5rem;
                        padding: 0.75rem;
                        margin-bottom: 0.5rem;
                    ">
                        <div style="
                            font-size: 0.8rem;
                            color: {text_color};
                            font-weight: 600;
                            margin-bottom: 0.25rem;
                        ">{icon} {fb.get('question', '전체')}</div>
                        <div style="
                            font-size: 0.75rem;
                            color: {text_color};
                            line-height: 1.5;
                        ">{fb.get('message', '')}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="
                    text-align: center;
                    padding: 1rem;
                    color: #94a3b8;
                    font-size: 0.8rem;
                ">
                    <p style="margin: 0;">아직 검토 결과가 없습니다.</p>
                    <p style="margin: 0.25rem 0 0 0;">'AI 검토 요청' 버튼을 클릭하세요.</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 검토 가이드
        st.markdown("""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.25rem;
                margin-bottom: 1rem;
            ">
                <h4 style="
                    font-weight: 700;
                    color: #1e293b;
                    font-size: 0.9rem;
                    margin: 0 0 0.75rem 0;
                ">📋 검토 기준</h4>
                
                <ul style="
                    font-size: 0.8rem;
                    color: #64748b;
                    padding-left: 1rem;
                    margin: 0;
                    line-height: 1.8;
                ">
                    <li><strong>구체성:</strong> 날짜, 장소, 이름 등 구체적 정보</li>
                    <li><strong>진정성:</strong> 실제 경험과 감정 표현</li>
                    <li><strong>적합성:</strong> 비자 목적에 맞는 내용</li>
                    <li><strong>금지표현:</strong> 법적 문제 표현 감지</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # 작성 진행률
        total_questions = len(questions)
        completed = sum(1 for q in questions if len(st.session_state.narrative_answers.get(q['id'], '')) >= q.get('min_chars', 100))
        progress = int((completed / total_questions) * 100) if total_questions > 0 else 0
        
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.25rem;
            ">
                <h4 style="
                    font-weight: 700;
                    color: #1e293b;
                    font-size: 0.9rem;
                    margin: 0 0 0.75rem 0;
                ">📊 작성 진행률</h4>
                
                <div style="
                    background: #e2e8f0;
                    border-radius: 0.5rem;
                    height: 8px;
                    margin-bottom: 0.5rem;
                    overflow: hidden;
                ">
                    <div style="
                        background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
                        height: 100%;
                        width: {progress}%;
                        border-radius: 0.5rem;
                        transition: width 0.3s ease;
                    "></div>
                </div>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    font-size: 0.75rem;
                    color: #64748b;
                ">
                    <span>{completed}/{total_questions} 항목 완료</span>
                    <span style="font-weight: 600; color: {'#22c55e' if progress == 100 else '#64748b'};">{progress}%</span>
                </div>
            </div>
        """, unsafe_allow_html=True)


def get_narrative_questions(scenario_id):
    """시나리오별 질문 목록 반환"""
    
    questions = {
        "A": [  # 구직 (D-10)
            {
                "id": "job_search_plan",
                "title": "월별 구직 활동 계획",
                "hint": "향후 6개월간 월별로 어떤 구직 활동을 할 계획인지 구체적으로 작성해주세요.",
                "placeholder": "예: 1월 - 잡코리아, 사람인 이력서 등록 및 IT 기업 10곳 지원\n2월 - 면접 준비 및 코딩테스트 대비\n3월 - ...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "target_companies",
                "title": "희망 기업 및 직무",
                "hint": "지원하고자 하는 기업과 직무를 구체적으로 작성해주세요.",
                "placeholder": "예: 네이버, 카카오, 라인 등 IT 대기업의 백엔드 개발자 포지션에 지원할 예정입니다...",
                "min_chars": 100,
                "required": True
            },
            {
                "id": "qualifications",
                "title": "보유 역량 및 자격",
                "hint": "해당 직무에 적합한 본인의 역량, 경험, 자격증 등을 작성해주세요.",
                "placeholder": "예: 컴퓨터공학 학사 학위와 함께 정보처리기사 자격증을 보유하고 있으며...",
                "min_chars": 100,
                "required": False
            },
            {
                "id": "stay_reason",
                "title": "한국 체류 사유",
                "hint": "왜 한국에서 구직 활동을 하고자 하는지 설명해주세요.",
                "placeholder": "예: 한국 IT 산업의 빠른 성장과 혁신적인 기업 문화에 매력을 느껴...",
                "min_chars": 80,
                "required": False
            }
        ],
        "B": [  # 아르바이트 (시간제)
            {
                "id": "work_description",
                "title": "담당 업무 내용",
                "hint": "맡게 될 업무를 구체적으로 설명해주세요. (단순 노무가 아님을 증명)",
                "placeholder": "예: 카페에서 바리스타로 근무하며 음료 제조, 고객 응대, 재고 관리 등의 업무를 담당합니다...",
                "min_chars": 100,
                "required": True
            },
            {
                "id": "work_schedule",
                "title": "근무 일정",
                "hint": "주당 근무 시간과 요일별 스케줄을 작성해주세요. (주 20시간 이내)",
                "placeholder": "예: 월, 수, 금 오후 2시~6시 (주 12시간) 학업에 지장이 없는 시간대에 근무합니다...",
                "min_chars": 80,
                "required": True
            },
            {
                "id": "study_balance",
                "title": "학업과의 병행 계획",
                "hint": "아르바이트와 학업을 어떻게 병행할 것인지 설명해주세요.",
                "placeholder": "예: 수업이 없는 시간대에만 근무하여 학업에 집중하면서도...",
                "min_chars": 80,
                "required": False
            }
        ],
        "C": [  # 결혼 이민 (F-6)
            {
                "id": "first_meeting",
                "title": "첫 만남과 교제 과정",
                "hint": "배우자와 처음 만난 계기와 교제 과정을 진솔하게 작성해주세요.",
                "placeholder": "예: 2022년 3월 친구의 소개로 처음 만났습니다. 첫 만남은 서울 종로구의 한 카페에서...",
                "min_chars": 200,
                "required": True
            },
            {
                "id": "marriage_decision",
                "title": "결혼 결심 계기",
                "hint": "결혼을 결심하게 된 구체적인 계기나 에피소드를 작성해주세요.",
                "placeholder": "예: 1년간의 교제 후, 서로의 가치관과 미래 계획이 일치한다는 것을 확인하고...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "future_plan",
                "title": "결혼 후 계획",
                "hint": "결혼 후 한국에서의 생활 계획을 작성해주세요.",
                "placeholder": "예: 배우자와 함께 서울에서 거주하며, 한국어 공부를 계속하고...",
                "min_chars": 100,
                "required": True
            },
            {
                "id": "family_approval",
                "title": "양가 부모님 반응",
                "hint": "양가 부모님의 결혼에 대한 반응과 만남 과정을 작성해주세요.",
                "placeholder": "예: 2023년 설날에 배우자의 부모님을 처음 뵙고 인사드렸습니다...",
                "min_chars": 100,
                "required": False
            }
        ],
        "D": [  # 가족 초청 (F-1-5)
            {
                "id": "invitation_reason",
                "title": "초청 사유",
                "hint": "부모님/가족을 초청해야 하는 구체적인 사유를 작성해주세요.",
                "placeholder": "예: 어머니의 건강이 좋지 않아 한국에서 함께 지내며 돌봐드리고자 합니다...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "stay_plan",
                "title": "체류 중 계획",
                "hint": "초청 기간 동안의 구체적인 생활 계획을 작성해주세요.",
                "placeholder": "예: 저의 집에서 함께 거주하며, 정기적으로 병원 검진을 받고...",
                "min_chars": 100,
                "required": True
            },
            {
                "id": "financial_support",
                "title": "재정 지원 계획",
                "hint": "체류 기간 동안의 재정적 지원 계획을 설명해주세요.",
                "placeholder": "예: 월 급여 350만원 중 100만원을 생활비로 지원하고...",
                "min_chars": 80,
                "required": True
            }
        ],
        "E": [  # 전문 인력 (E-7)
            {
                "id": "hiring_reason",
                "title": "채용 필요성",
                "hint": "해당 외국인 인력을 채용해야 하는 구체적인 이유를 작성해주세요.",
                "placeholder": "예: 당사는 베트남 시장 진출을 위해 베트남어 원어민이면서 IT 개발 역량을 갖춘 인력이 필요합니다...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "job_duties",
                "title": "담당 업무 상세",
                "hint": "담당하게 될 업무의 전문성과 구체적인 내용을 작성해주세요.",
                "placeholder": "예: 베트남 현지 고객사와의 기술 미팅 통역, 현지화 소프트웨어 개발...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "expected_contribution",
                "title": "기대 효과",
                "hint": "채용으로 인한 회사 및 국가 경제에 대한 기대 효과를 작성해주세요.",
                "placeholder": "예: 베트남 시장 매출 30% 증가 예상, 양국 간 기술 교류 활성화...",
                "min_chars": 100,
                "required": False
            }
        ],
        "F": [  # 국적 귀화
            {
                "id": "naturalization_reason",
                "title": "귀화 동기",
                "hint": "한국 국적을 취득하고자 하는 동기를 진솔하게 작성해주세요.",
                "placeholder": "예: 한국에서 15년간 생활하며 이곳이 제 삶의 터전이 되었습니다...",
                "min_chars": 200,
                "required": True
            },
            {
                "id": "korea_adaptation",
                "title": "한국 사회 적응 과정",
                "hint": "한국 사회에 어떻게 적응해왔는지 구체적으로 작성해주세요.",
                "placeholder": "예: 처음 한국에 왔을 때 언어와 문화의 차이로 어려움이 있었지만...",
                "min_chars": 150,
                "required": True
            },
            {
                "id": "contribution_plan",
                "title": "사회 기여 계획",
                "hint": "한국 사회에 어떻게 기여할 계획인지 작성해주세요.",
                "placeholder": "예: 다문화 가정 지원 봉사활동에 참여하고, 제 경험을 바탕으로...",
                "min_chars": 100,
                "required": True
            }
        ]
    }
    
    return questions.get(scenario_id, [
        {
            "id": "general_statement",
            "title": "신청 사유",
            "hint": "신청 사유를 상세히 작성해주세요.",
            "placeholder": "신청 사유를 작성해주세요...",
            "min_chars": 100,
            "required": True
        }
    ])


def run_ai_validation(scenario, questions):
    """AI 검토 실행 (목업)"""
    
    feedbacks = []
    answers = st.session_state.get('narrative_answers', {})
    
    # 위험 표현 패턴
    danger_patterns = {
        "A": ["취업 확정", "내정", "채용 확정", "이미 취업"],
        "B": ["풀타임", "40시간", "주 40", "전일제"],
        "C": ["돈을 받고", "위장", "계약 결혼", "비자 때문에", "돈을 벌기 위해"],
        "D": ["취업하러", "일하러", "돈 벌러"],
        "E": ["단순 노무", "청소", "설거지", "포장"],
        "F": ["한국이 싫", "빨리 떠나"]
    }
    
    patterns = danger_patterns.get(scenario.id, [])
    
    for q in questions:
        q_id = q['id']
        answer = answers.get(q_id, '')
        q_title = q['title']
        min_chars = q.get('min_chars', 100)
        
        # 1. 글자 수 검증
        if len(answer) == 0:
            feedbacks.append({
                'question': q_title,
                'type': 'warning',
                'message': '아직 작성되지 않았습니다. 내용을 입력해주세요.'
            })
            continue
        elif len(answer) < min_chars:
            feedbacks.append({
                'question': q_title,
                'type': 'warning',
                'message': f'내용이 부족합니다. ({len(answer)}/{min_chars}자) 더 구체적으로 작성해주세요.'
            })
            continue
        
        # 2. 위험 표현 검사
        found_dangers = [p for p in patterns if p in answer]
        if found_dangers:
            feedbacks.append({
                'question': q_title,
                'type': 'error',
                'message': f'위험 표현 감지: "{", ".join(found_dangers)}". 이 표현은 심사에서 불리할 수 있습니다.'
            })
            continue
        
        # 3. 구체성 검사 (날짜, 숫자 포함 여부)
        import re
        has_date = bool(re.search(r'\d{4}년|\d{1,2}월|\d{1,2}일', answer))
        has_number = bool(re.search(r'\d+', answer))
        
        if not has_date and not has_number and len(answer) > 50:
            feedbacks.append({
                'question': q_title,
                'type': 'info',
                'message': '구체적인 날짜나 수치를 추가하면 더 설득력이 있습니다.'
            })
            continue
        
        # 4. 통과
        feedbacks.append({
            'question': q_title,
            'type': 'success',
            'message': '내용이 잘 작성되었습니다. ✓'
        })
    
    # 전체 피드백 저장
    st.session_state.ai_feedbacks = feedbacks
    
    # 전체 검토 결과 요약
    errors = sum(1 for f in feedbacks if f['type'] == 'error')
    warnings = sum(1 for f in feedbacks if f['type'] == 'warning')
    
    if errors > 0:
        st.error(f"⚠️ {errors}개 항목에서 문제가 발견되었습니다. 수정이 필요합니다.")
    elif warnings > 0:
        st.warning(f"💡 {warnings}개 항목에서 보완이 필요합니다.")
    else:
        st.success("✅ 모든 항목이 잘 작성되었습니다!")


def format_form_data(form_data):
    """폼 데이터를 HTML로 포맷"""
    if not form_data:
        return "<span style='color: #94a3b8;'>입력된 정보가 없습니다.</span>"
    
    html = ""
    for key, value in form_data.items():
        if value:
            label = key.replace('_', ' ').title()
            html += f"<div style='margin-bottom: 0.25rem; color: #64748b;'><strong style='color: #1e293b;'>{label}:</strong> {value}</div>"
    
    return html if html else "<span style='color: #94a3b8;'>입력된 정보가 없습니다.</span>"
