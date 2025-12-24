"""
K-Stay Scenario Form Page
Phase 2-3: Variable Fact + Narrative Collection
"""

import streamlit as st
from datetime import date
from config.settings import SCENARIOS
from services.ai_service import AIService, NarrativeValidator
from services.document_service import DocumentService


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
    
    # 헤더
    render_header(scenario)
    
    # 진행 단계
    current_step = st.session_state.get('form_step', 1)
    render_progress(current_step)
    
    # 단계별 렌더링
    if current_step == 1:
        render_variable_fact_form(scenario)
    elif current_step == 2:
        render_narrative_form(scenario)
    elif current_step == 3:
        render_review_and_generate(scenario)


def render_header(scenario):
    """헤더 렌더링"""
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(201,162,39,0.1) 0%, rgba(10,22,40,0.8) 100%);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(201,162,39,0.2);
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 3rem;">{scenario.icon}</div>
                <div>
                    <h1 style="
                        color: white;
                        font-family: 'Noto Sans KR', sans-serif;
                        margin: 0;
                    ">{scenario.name}</h1>
                    <p style="
                        color: #C9A227;
                        margin: 0.3rem 0 0 0;
                    ">{scenario.visa_type}</p>
                </div>
            </div>
            <p style="color: #a0aec0; margin-top: 1rem;">
                {scenario.description}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 뒤로가기 버튼
    if st.button("← 다른 시나리오 선택"):
        st.session_state.selected_scenario = None
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.session_state.narrative_data = {}
        st.session_state.current_page = 'dashboard'
        st.rerun()


def render_progress(current_step):
    """진행 단계 표시"""
    
    steps = [
        ("1", "상황 정보", "variable"),
        ("2", "사연 작성", "narrative"),
        ("3", "검토 및 생성", "generate")
    ]
    
    cols = st.columns(len(steps))
    
    for i, (num, label, key) in enumerate(steps):
        with cols[i]:
            is_active = (i + 1) == current_step
            is_completed = (i + 1) < current_step
            
            if is_completed:
                color = "#4CAF50"
                icon = "✓"
            elif is_active:
                color = "#C9A227"
                icon = num
            else:
                color = "#6c757d"
                icon = num
            
            st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="
                        width: 36px;
                        height: 36px;
                        border-radius: 50%;
                        background: {'rgba(201,162,39,0.2)' if is_active else 'rgba(255,255,255,0.05)'};
                        border: 2px solid {color};
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        color: {color};
                        font-weight: 700;
                    ">{icon}</div>
                    <p style="color: {color}; font-size: 0.85rem; margin: 0.5rem 0 0 0;">{label}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


def render_variable_fact_form(scenario):
    """Phase 2: Variable Fact 폼"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
        ">
            <h3 style="color: #C9A227; margin-bottom: 0.5rem;">
                📝 상황별 정보 입력
            </h3>
            <p style="color: #a0aec0; font-size: 0.9rem;">
                이 시나리오에 필요한 구체적인 정보를 입력해주세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # 동적 폼 필드 생성
    with st.form("variable_fact_form"):
        form_data = {}
        
        # 2열 레이아웃
        fields = scenario.smart_form_fields
        
        for i in range(0, len(fields), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(fields):
                    field = fields[i + j]
                    with col:
                        form_data[field['name']] = render_form_field(field)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("← 이전", use_container_width=True):
                st.session_state.form_step = 1
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.form_submit_button("다음 →", type="primary", use_container_width=True):
                # 필수 필드 검증
                required_fields = [f for f in fields if f.get('required', True)]
                missing = [f['label'] for f in required_fields if not form_data.get(f['name'])]
                
                if missing:
                    st.error(f"다음 항목을 입력해주세요: {', '.join(missing)}")
                else:
                    st.session_state.form_data = form_data
                    st.session_state.form_step = 2
                    st.rerun()


def render_form_field(field):
    """개별 폼 필드 렌더링"""
    
    field_type = field.get('type', 'text')
    label = field.get('label', field['name'])
    key = f"field_{field['name']}"
    default = st.session_state.get('form_data', {}).get(field['name'], '')
    
    if field_type == 'text':
        return st.text_input(label, value=default, key=key)
    
    elif field_type == 'textarea':
        return st.text_area(label, value=default, key=key, height=100)
    
    elif field_type == 'number':
        return st.number_input(label, value=int(default) if default else 0, key=key)
    
    elif field_type == 'select':
        options = field.get('options', [])
        index = options.index(default) if default in options else 0
        return st.selectbox(label, options=[''] + options, key=key)
    
    elif field_type == 'date':
        return st.date_input(label, key=key)
    
    elif field_type == 'checkbox':
        return st.checkbox(label, value=bool(default), key=key)
    
    return st.text_input(label, value=default, key=key)


def render_narrative_form(scenario):
    """Phase 3: Narrative 폼 (AI 검토 포함)"""
    
    ai_prompts = scenario.ai_prompts
    
    st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
        ">
            <h3 style="color: #C9A227; margin-bottom: 0.5rem;">
                ✍️ {ai_prompts.get('narrative_label', '사연 작성')}
            </h3>
            <p style="color: #a0aec0; font-size: 0.9rem;">
                AI가 실시간으로 내용을 검토하여 피드백을 제공합니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 사연 입력
    narrative_field = ai_prompts.get('narrative_field', 'narrative')
    placeholder = ai_prompts.get('narrative_placeholder', '내용을 입력해주세요...')
    
    narrative = st.text_area(
        "내용 입력",
        placeholder=placeholder,
        height=300,
        key="narrative_input",
        value=st.session_state.get('narrative_data', {}).get(narrative_field, '')
    )
    
    # AI 검토 버튼
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🤖 AI 검토", use_container_width=True):
            if len(narrative) < 50:
                st.warning("내용이 너무 짧습니다. 최소 50자 이상 작성해주세요.")
            else:
                with st.spinner("AI가 검토 중입니다..."):
                    ai_service = AIService()
                    result = ai_service.validate_narrative(
                        narrative,
                        ai_prompts.get('validation_prompt', ''),
                        st.session_state.get('form_data', {})
                    )
                    
                    st.session_state.ai_feedback = result
    
    # AI 피드백 표시
    if 'ai_feedback' in st.session_state and st.session_state.ai_feedback:
        st.markdown("<br>", unsafe_allow_html=True)
        NarrativeValidator.render_validation_result(st.session_state.ai_feedback)
    
    # AI 자동 생성 옵션
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🤖 AI가 대신 작성해주기"):
        st.markdown("""
            <p style="color: #a0aec0; font-size: 0.9rem;">
                입력한 정보를 바탕으로 AI가 초안을 작성합니다.
            </p>
        """, unsafe_allow_html=True)
        
        if st.button("AI 초안 생성", use_container_width=True):
            with st.spinner("AI가 초안을 작성 중입니다..."):
                ai_service = AIService()
                
                generation_prompt = ai_prompts.get('generation_prompt', '')
                combined_data = {
                    **st.session_state.get('user_data', {}),
                    **st.session_state.get('form_data', {}),
                    'narrative_content': narrative
                }
                
                generated = ai_service.generate_narrative(generation_prompt, combined_data)
                st.session_state.generated_narrative = generated
                st.text_area("생성된 초안", value=generated, height=200, key="generated_preview")
                
                if st.button("이 초안 사용하기"):
                    st.session_state.narrative_data = {narrative_field: generated}
                    st.rerun()
    
    # 네비게이션
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← 이전", use_container_width=True):
            st.session_state.form_step = 1
            st.rerun()
    
    with col2:
        if st.button("다음 →", type="primary", use_container_width=True):
            if len(narrative) < 50:
                st.error("내용을 충분히 작성해주세요. (최소 50자)")
            else:
                st.session_state.narrative_data = {narrative_field: narrative}
                st.session_state.form_step = 3
                st.rerun()


def render_review_and_generate(scenario):
    """Phase 4: 검토 및 문서 생성"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 16px;
            padding: 2rem;
        ">
            <h3 style="color: #C9A227; margin-bottom: 0.5rem;">
                ✅ 최종 검토
            </h3>
            <p style="color: #a0aec0; font-size: 0.9rem;">
                입력한 정보를 확인하고 문서를 생성합니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 데이터 요약
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 기본 정보")
        user_data = st.session_state.get('user_data', {})
        st.write(f"성명: {user_data.get('surname', '')} {user_data.get('given_name', '')}")
        st.write(f"국적: {user_data.get('nationality', '')}")
        st.write(f"여권번호: {user_data.get('passport_no', '')}")
    
    with col2:
        st.markdown("#### 📝 상황 정보")
        form_data = st.session_state.get('form_data', {})
        for key, value in list(form_data.items())[:5]:
            if value:
                label = key.replace('_', ' ').title()
                st.write(f"{label}: {value}")
    
    st.markdown("---")
    
    # 생성될 문서 목록
    st.markdown("#### 📦 생성될 문서 패키지")
    
    for i, doc in enumerate(scenario.required_docs, 1):
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                padding: 0.8rem;
                background: rgba(255,255,255,0.02);
                border-radius: 8px;
                margin-bottom: 0.5rem;
            ">
                <span style="
                    background: rgba(201,162,39,0.2);
                    color: #C9A227;
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 1rem;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">{i}</span>
                <span style="color: white;">{doc}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 네비게이션 및 생성
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("← 이전", use_container_width=True):
            st.session_state.form_step = 2
            st.rerun()
    
    with col3:
        if st.button("📄 문서 패키지 생성", type="primary", use_container_width=True):
            with st.spinner("문서를 생성하는 중입니다..."):
                doc_service = DocumentService()
                
                zip_bytes = doc_service.generate_full_package(
                    scenario.id,
                    st.session_state.get('user_data', {}),
                    st.session_state.get('form_data', {}),
                    st.session_state.get('narrative_data', {})
                )
                
                if zip_bytes:
                    st.session_state.generated_zip = zip_bytes
                    st.session_state.current_page = 'document_preview'
                    st.rerun()
                else:
                    st.error("문서 생성에 실패했습니다.")
