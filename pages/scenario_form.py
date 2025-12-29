"""
K-Stay Scenario Form Page
3-Phase Architecture:
- Phase 1: Universal Fact (불변 정보) - 회원가입 시 입력, 확인 후 다음 단계
- Phase 2: Variable Fact (가변 정보) - 시나리오별 Smart Form
- Phase 3: Narrative (정성 사연) - AI Active 검토 & 코칭
- Phase 4: Payment (결제) - 문서 생성 전 결제
"""

import streamlit as st
from datetime import date
from config.settings import SCENARIOS
from services.ai_service import AIService, RAGService
from services.payment_service import PaymentService


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
    elif current_step == 4:
        render_phase4_payment(scenario)


def render_phase_indicator(current_step):
    """4-Phase 진행 상태 표시"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    phases = [
        ("PHASE 1", "Universal Fact", "불변 정보 확인", "#22c55e", "#dcfce7"),
        ("PHASE 2", "Variable Fact", "가변 정보 입력", "#3b82f6", "#dbeafe"),
        ("PHASE 3", "Narrative", "정성 사연", "#a855f7", "#f3e8ff"),
        ("PHASE 4", "Payment", "결제 & 문서생성", "#f59e0b", "#fef3c7"),
    ]
    
    for i, (col, (badge, title, desc, active_color, active_bg)) in enumerate(zip([col1, col2, col3, col4], phases)):
        step = i + 1
        is_active = current_step == step
        is_done = current_step > step
        
        with col:
            if is_active:
                bg_color = active_bg
                border_color = active_color
                title_color = active_color
                badge_bg = active_color
                badge_text = f"● {badge}"
                shadow = f"box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
            elif is_done:
                bg_color = "#f0fdf4"
                border_color = "#86efac"
                title_color = "#166534"
                badge_bg = "#22c55e"
                badge_text = f"✓ {badge}"
                shadow = ""
            else:
                bg_color = "#f1f5f9"
                border_color = "#cbd5e1"
                title_color = "#64748b"
                badge_bg = "#94a3b8"
                badge_text = badge
                shadow = ""
            
            st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border-radius: 0.75rem;
                    padding: 1rem;
                    border: 2px solid {border_color};
                    min-height: 100px;
                    {shadow}
                ">
                    <div style="
                        background: {badge_bg};
                        color: white;
                        font-size: 0.65rem;
                        font-weight: 700;
                        padding: 0.2rem 0.4rem;
                        border-radius: 0.25rem;
                        display: inline-block;
                        margin-bottom: 0.5rem;
                    ">{badge_text}</div>
                    <h3 style="color: {title_color}; font-size: 0.95rem; font-weight: 700; margin: 0.25rem 0;">{title}</h3>
                    <p style="color: #64748b; font-size: 0.7rem; margin: 0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_phase1_universal_fact(scenario):
    """Phase 1: Universal Fact - 회원가입 시 입력된 불변 정보 확인"""
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">
                📋 {scenario.name} - 기본 정보 확인
            </h2>
            <p style="color: #64748b;">회원가입 시 입력하신 정보입니다. 확인 후 다음 단계로 진행하세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_data = st.session_state.get('user_data', {})
    
    # 인적 사항
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👤 인적 사항")
        st.text_input("성 (Surname)", value=user_data.get('surname', ''), disabled=True)
        st.text_input("이름 (Given Name)", value=user_data.get('given_name', ''), disabled=True)
        st.text_input("국적", value=user_data.get('nationality', ''), disabled=True)
    
    with col2:
        st.markdown("#### 🛂 여권 정보")
        st.text_input("여권 번호", value=user_data.get('passport_no', ''), disabled=True)
        st.text_input("외국인등록번호", value=user_data.get('alien_registration_no', ''), disabled=True)
    
    st.markdown("---")
    
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("← 대시보드로", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col_next:
        if st.button("다음 단계 →", use_container_width=True, type="primary"):
            st.session_state.form_step = 2
            st.rerun()


def render_phase2_variable_fact(scenario):
    """Phase 2: Variable Fact - 시나리오별 가변 정보 입력"""
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">
                📝 {scenario.name} - 상세 정보 입력
            </h2>
            <p style="color: #64748b;">시나리오에 필요한 추가 정보를 입력해주세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 시나리오별 폼 렌더링
    render_scenario_specific_form(scenario)
    
    st.markdown("---")
    
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("← Phase 1로", use_container_width=True):
            st.session_state.form_step = 1
            st.rerun()
    
    with col_next:
        if st.button("다음 단계 →", use_container_width=True, type="primary"):
            save_form_data(scenario)
            st.session_state.form_step = 3
            st.rerun()


def render_phase3_narrative(scenario):
    """Phase 3: Narrative - 자소서 형식 + AI 실시간 검토"""
    
    questions = get_narrative_questions(scenario.id)
    
    if 'narrative_answers' not in st.session_state:
        st.session_state.narrative_answers = {}
    
    if 'ai_feedbacks' not in st.session_state:
        st.session_state.ai_feedbacks = []
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">
                ✍️ {scenario.name} - 사연 작성
            </h2>
            <p style="color: #64748b;">각 질문에 대해 상세히 작성해주세요. AI가 실시간으로 내용을 검토합니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    form_col, feedback_col = st.columns([2, 1])
    
    with form_col:
        for i, q in enumerate(questions):
            q_id = q['id']
            q_title = q['title']
            q_hint = q['hint']
            q_placeholder = q['placeholder']
            q_required = q.get('required', False)
            
            if i > 0:
                st.divider()
            
            required_text = " *필수" if q_required else ""
            st.markdown(f"**Q{i+1}. {q_title}**{required_text}")
            st.caption(q_hint)
            
            current_value = st.session_state.narrative_answers.get(q_id, '')
            
            answer = st.text_area(
                f"답변 {i+1}",
                value=current_value,
                height=120,
                key=f"narrative_{q_id}",
                placeholder=q_placeholder,
                label_visibility="collapsed"
            )
            
            st.session_state.narrative_answers[q_id] = answer
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🤖 AI 검토 요청", use_container_width=True):
            run_ai_validation(scenario, questions)
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_back, col_next = st.columns(2)
        
        with col_back:
            if st.button("← Phase 2로 돌아가기", use_container_width=True):
                st.session_state.form_step = 2
                st.rerun()
        
        with col_next:
            if st.button("✓ 작성 완료 → 결제하기", use_container_width=True, type="primary"):
                # 필수 항목 검증
                missing_required = []
                for q in questions:
                    if q.get('required', False):
                        answer = st.session_state.narrative_answers.get(q['id'], '')
                        if len(answer) < q.get('min_chars', 50):
                            missing_required.append(q['title'])
                
                if missing_required:
                    st.error(f"필수 항목을 작성해주세요: {', '.join(missing_required)}")
                else:
                    # 결제 단계로 이동
                    st.session_state.form_step = 4
                    st.rerun()
    
    with feedback_col:
        render_ai_feedback_panel()


def render_phase4_payment(scenario):
    """Phase 4: Payment - 결제 후 문서 생성"""
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">
                💳 {scenario.name} - 결제 & 문서 생성
            </h2>
            <p style="color: #64748b;">결제 완료 후 문서가 자동 생성됩니다.</p>
        </div>
    """, unsafe_allow_html=True)
    
    is_paid = st.session_state.get('is_paid', False)
    is_admin = st.session_state.get('is_admin', False)
    
    if is_paid or is_admin:
        # 이미 결제됨 - 바로 문서 생성
        st.success("✅ Premium 활성화 상태입니다!")
        
        if st.button("📄 문서 생성하기", type="primary", use_container_width=True):
            generate_documents(scenario)
    else:
        # 결제 필요
        render_payment_section(scenario)
    
    st.markdown("---")
    
    if st.button("← Phase 3로 돌아가기", use_container_width=True):
        st.session_state.form_step = 3
        st.rerun()


def render_payment_section(scenario):
    """결제 섹션 렌더링"""
    
    # 가격 박스
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 1.5rem;
            max-width: 400px;
        ">
            <div style="font-size: 1.2rem; color: rgba(255,255,255,0.8); margin-bottom: 0.5rem;">Premium</div>
            <div style="color: white; font-size: 3rem; font-weight: 700;">$9.99</div>
            <div style="color: rgba(255,255,255,0.8);">일회성 결제 · 평생 이용</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### ✨ Premium 혜택
    - ✅ 6가지 시나리오 무제한 이용
    - ✅ AI 문서 자동 생성 
    - ✅ 전문가 수준 사연서 작성
    - ✅ ZIP 패키지 다운로드
    """)
    
    st.markdown("---")
    
    payment_service = PaymentService()
    
    if payment_service.is_stripe_connected():
        st.success("✅ Stripe 연결됨")
        
        if 'checkout_url' not in st.session_state or not st.session_state.checkout_url:
            if st.button("💳 카드 결제하기", type="primary", use_container_width=True):
                user_id = st.session_state.get('user_id', '')
                user_email = st.session_state.get('user_email', '')
                
                with st.spinner("결제 페이지 생성 중..."):
                    checkout_url = payment_service.create_checkout_session(user_id, user_email)
                
                if checkout_url:
                    st.session_state.checkout_url = checkout_url
                    st.rerun()
        
        if st.session_state.get('checkout_url'):
            url = st.session_state.checkout_url
            
            st.markdown("### 🔗 결제 링크")
            st.markdown(f"[**👉 여기를 클릭하여 결제 페이지로 이동**]({url})")
            st.text_input("또는 URL 복사:", value=url, key="payment_url")
            
            st.info("💡 결제 완료 후 아래 버튼을 눌러주세요.")
            
            if st.button("✅ 결제 완료했습니다", type="primary", use_container_width=True):
                st.session_state.is_paid = True
                st.session_state.checkout_url = None
                st.success("🎉 Premium이 활성화되었습니다!")
                st.rerun()
    else:
        st.warning("⚠️ Stripe 미연결 - 테스트 모드")
        
        if st.button("🧪 테스트 결제 (무료)", type="primary", use_container_width=True):
            st.session_state.is_paid = True
            st.success("🎉 테스트 결제 완료!")
            st.rerun()


def generate_documents(scenario):
    """문서 생성"""
    from services.document_service import DocumentService
    
    with st.spinner("문서 생성 중..."):
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
        else:
            st.error("문서 생성에 실패했습니다.")


def render_ai_feedback_panel():
    """AI 피드백 패널"""
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border: 1px solid #fecaca;
            border-radius: 0.75rem;
            padding: 1.25rem;
        ">
            <h4 style="font-weight: 700; color: #dc2626; font-size: 0.9rem; margin: 0 0 0.75rem 0;">
                🧠 AI Validator 피드백
            </h4>
    """, unsafe_allow_html=True)
    
    feedbacks = st.session_state.get('ai_feedbacks', [])
    
    if feedbacks:
        for fb in feedbacks:
            fb_type = fb.get('type', 'info')
            if fb_type == 'warning':
                icon, bg, border, text_color = "⚠️", "#fef3c7", "#fcd34d", "#92400e"
            elif fb_type == 'error':
                icon, bg, border, text_color = "❌", "#fee2e2", "#fca5a5", "#991b1b"
            elif fb_type == 'success':
                icon, bg, border, text_color = "✅", "#dcfce7", "#86efac", "#166534"
            else:
                icon, bg, border, text_color = "💡", "#dbeafe", "#93c5fd", "#1e40af"
            
            st.markdown(f"""
                <div style="background: {bg}; border: 1px solid {border}; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 0.5rem;">
                    <div style="font-size: 0.8rem; color: {text_color}; font-weight: 600;">{icon} {fb.get('question', '')}</div>
                    <div style="font-size: 0.75rem; color: {text_color};">{fb.get('message', '')}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; color: #94a3b8; font-size: 0.8rem;">
                <p>아직 검토 결과가 없습니다.</p>
                <p>'AI 검토 요청' 버튼을 클릭하세요.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_scenario_specific_form(scenario):
    """시나리오별 폼 렌더링 (간소화)"""
    
    if scenario.id == "A":  # 구직 준비 D-10
        st.markdown("**🎓 학력 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("최종 학력", ["학사", "석사", "박사", "전문학사", "고졸"], key="education_level")
            st.text_input("전공", key="major")
        with col2:
            st.date_input("졸업(예정)일", key="graduation_date")
            st.text_input("목표 산업/직종", key="target_industry")
    
    elif scenario.id == "B":  # 아르바이트
        st.markdown("**📚 학교 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("학교명", key="school_name")
            st.selectbox("학적 상태", ["재학", "휴학", "수료"], key="student_status")
        with col2:
            st.number_input("현재 학기", min_value=1, max_value=12, key="semester")
            st.number_input("GPA", min_value=0.0, max_value=4.5, step=0.1, key="gpa")
        
        st.markdown("**💼 고용주 정보**")
        col3, col4 = st.columns(2)
        with col3:
            st.text_input("사업장명", key="employer_name")
            st.text_input("사업자등록번호", key="employer_business_no")
        with col4:
            st.number_input("시급 (원)", min_value=0, key="hourly_wage")
            st.number_input("주당 근무시간", min_value=0, max_value=20, key="weekly_hours")
    
    elif scenario.id == "C":  # 결혼 이민
        st.markdown("**💍 배우자 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("배우자 성명", key="spouse_name")
            st.text_input("배우자 연락처", key="spouse_phone")
        with col2:
            st.date_input("결혼일", key="marriage_date")
            st.text_input("배우자 직업", key="spouse_occupation")
    
    elif scenario.id == "D":  # 가족 초청
        st.markdown("**👨‍👩‍👧 피초청인 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("피초청인 성명", key="invitee_name")
            st.selectbox("관계", ["부", "모", "배우자", "자녀", "기타"], key="invitee_relation")
        with col2:
            st.date_input("생년월일", key="invitee_birth_date")
            st.text_input("여권번호", key="invitee_passport_no")
    
    elif scenario.id == "E":  # 전문 인력
        st.markdown("**🏢 회사 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("회사명", key="company_name")
            st.text_input("사업자등록번호", key="company_business_no")
        with col2:
            st.text_input("업종", key="company_industry")
            st.number_input("직원 수", min_value=1, key="company_employees")
    
    elif scenario.id == "F":  # 국적 귀화
        st.markdown("**🇰🇷 한국 체류 정보**")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("한국 거주 기간 (년)", min_value=0, key="korea_stay_years")
            st.text_input("현재 체류자격", key="current_visa_type")
        with col2:
            st.selectbox("한국어 능력", ["TOPIK 3급", "TOPIK 4급", "TOPIK 5급", "TOPIK 6급"], key="korean_language_level")


def save_form_data(scenario):
    """폼 데이터 저장"""
    form_data = {}
    form_keys = [
        'education_level', 'major', 'graduation_date', 'target_industry',
        'school_name', 'student_status', 'semester', 'gpa',
        'employer_name', 'employer_business_no', 'hourly_wage', 'weekly_hours',
        'spouse_name', 'spouse_phone', 'marriage_date', 'spouse_occupation',
        'invitee_name', 'invitee_relation', 'invitee_birth_date', 'invitee_passport_no',
        'company_name', 'company_business_no', 'company_industry', 'company_employees',
        'korea_stay_years', 'current_visa_type', 'korean_language_level'
    ]
    
    for key in form_keys:
        if key in st.session_state:
            value = st.session_state[key]
            if hasattr(value, 'strftime'):
                value = value.strftime('%Y-%m-%d')
            form_data[key] = value
    
    st.session_state.form_data = form_data


def get_narrative_questions(scenario_id):
    """시나리오별 사연 질문 목록"""
    questions = {
        "A": [
            {"id": "job_search_plan", "title": "구직 활동 계획", "hint": "월별 구체적인 구직 활동 계획을 작성해주세요.", "placeholder": "예: 1월 - IT 기업 5곳 지원, 2월 - 면접 준비...", "min_chars": 100, "required": True},
            {"id": "career_goal", "title": "경력 목표", "hint": "한국에서의 경력 목표를 설명해주세요.", "placeholder": "예: 한국 IT 기업에서 개발자로 성장하여...", "min_chars": 80, "required": True}
        ],
        "B": [
            {"id": "work_reason", "title": "아르바이트 사유", "hint": "아르바이트가 필요한 이유를 설명해주세요.", "placeholder": "예: 학비와 생활비 마련을 위해...", "min_chars": 80, "required": True},
            {"id": "work_schedule", "title": "근무 일정", "hint": "주당 근무 시간과 요일별 스케줄을 작성해주세요.", "placeholder": "예: 월, 수, 금 오후 2시~6시...", "min_chars": 80, "required": True}
        ],
        "C": [
            {"id": "first_meeting", "title": "첫 만남과 교제 과정", "hint": "배우자와의 만남과 교제 과정을 진솔하게 작성해주세요.", "placeholder": "예: 2022년 친구 소개로 처음 만났습니다...", "min_chars": 150, "required": True},
            {"id": "marriage_decision", "title": "결혼 결심 계기", "hint": "결혼을 결심하게 된 계기를 작성해주세요.", "placeholder": "예: 1년간의 교제 후...", "min_chars": 100, "required": True}
        ],
        "D": [
            {"id": "invitation_reason", "title": "초청 사유", "hint": "가족을 초청해야 하는 구체적인 사유를 작성해주세요.", "placeholder": "예: 어머니의 건강이 좋지 않아...", "min_chars": 100, "required": True},
            {"id": "stay_plan", "title": "체류 중 계획", "hint": "초청 기간 동안의 계획을 작성해주세요.", "placeholder": "예: 저의 집에서 함께 거주하며...", "min_chars": 80, "required": True}
        ],
        "E": [
            {"id": "hiring_reason", "title": "채용 필요성", "hint": "해당 외국인 인력을 채용해야 하는 이유를 작성해주세요.", "placeholder": "예: 베트남 시장 진출을 위해...", "min_chars": 120, "required": True},
            {"id": "job_duties", "title": "담당 업무 상세", "hint": "담당하게 될 업무를 구체적으로 작성해주세요.", "placeholder": "예: 베트남 고객사와의 기술 미팅...", "min_chars": 100, "required": True}
        ],
        "F": [
            {"id": "naturalization_reason", "title": "귀화 동기", "hint": "한국 국적을 취득하고자 하는 동기를 작성해주세요.", "placeholder": "예: 한국에서 15년간 생활하며...", "min_chars": 150, "required": True},
            {"id": "korea_adaptation", "title": "한국 사회 적응 과정", "hint": "한국 사회에 어떻게 적응해왔는지 작성해주세요.", "placeholder": "예: 처음 한국에 왔을 때...", "min_chars": 100, "required": True}
        ]
    }
    
    return questions.get(scenario_id, [{"id": "general", "title": "신청 사유", "hint": "신청 사유를 작성해주세요.", "placeholder": "신청 사유...", "min_chars": 100, "required": True}])


def run_ai_validation(scenario, questions):
    """AI 검토 실행"""
    feedbacks = []
    answers = st.session_state.get('narrative_answers', {})
    
    for q in questions:
        q_id = q['id']
        answer = answers.get(q_id, '')
        q_title = q['title']
        min_chars = q.get('min_chars', 100)
        
        if len(answer) == 0:
            feedbacks.append({'question': q_title, 'type': 'warning', 'message': '아직 작성되지 않았습니다.'})
        elif len(answer) < min_chars:
            feedbacks.append({'question': q_title, 'type': 'warning', 'message': f'내용이 부족합니다. ({len(answer)}/{min_chars}자)'})
        else:
            feedbacks.append({'question': q_title, 'type': 'success', 'message': '내용이 잘 작성되었습니다. ✓'})
    
    st.session_state.ai_feedbacks = feedbacks
