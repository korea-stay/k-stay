"""
K-Stay Scenario Form Page
3-Phase Architecture (settings.py 기반 동적 생성)
- Phase 1: Universal Fact (Layer 1) - 회원가입 시 입력, DB에서 로드
- Phase 2: Variable Fact (Layer 2) - 시나리오별 Smart Form
- Phase 3: Narrative (Layer 3) - AI 실시간 검토 & 코칭
"""

import streamlit as st
from datetime import date, datetime
from typing import Dict, List, Any

# 설정 파일에서 Layer 정의 임포트
from config.settings import (
    SCENARIOS,
    LAYER1_UNIVERSAL_FIELDS,
    LAYER2_VARIABLE_FIELDS,
    LAYER3_NARRATIVE_FIELDS,
    get_layer2_fields,
    get_layer3_fields,
    get_danger_patterns,
    get_narrative_config,
)


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


def render_phase_indicator(current_step: int):
    """3-Phase 진행 상태 표시"""
    
    phases = [
        {"name": "Universal Fact", "desc": "불변 정보 확인", "color": "#22c55e"},
        {"name": "Variable Fact", "desc": "가변 정보 입력", "color": "#3b82f6"},
        {"name": "Narrative", "desc": "정성 사연", "color": "#a855f7"},
    ]
    
    cols = st.columns(3)
    
    for i, (col, phase) in enumerate(zip(cols, phases)):
        step_num = i + 1
        is_active = current_step == step_num
        is_done = current_step > step_num
        
        with col:
            if is_active:
                bg_color = f"{phase['color']}15"
                border_color = phase['color']
                badge_text = f"● PHASE {step_num}"
                shadow = f"box-shadow: 0 4px 12px {phase['color']}40;"
            elif is_done:
                bg_color = "#f0fdf4"
                border_color = "#86efac"
                badge_text = f"✓ PHASE {step_num}"
                shadow = ""
            else:
                bg_color = "#f1f5f9"
                border_color = "#cbd5e1"
                badge_text = f"PHASE {step_num}"
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
                        background: {phase['color'] if is_active else ('#22c55e' if is_done else '#94a3b8')};
                        color: white;
                        font-size: 0.7rem;
                        font-weight: 700;
                        padding: 0.25rem 0.5rem;
                        border-radius: 0.25rem;
                        display: inline-block;
                        margin-bottom: 0.5rem;
                    ">{badge_text}</div>
                    <h3 style="
                        color: {'#1e293b' if is_active or is_done else '#64748b'};
                        font-size: 1.1rem;
                        font-weight: 700;
                        margin: 0.5rem 0 0.25rem 0;
                    ">{phase['name']}</h3>
                    <p style="color: {'#64748b' if is_active or is_done else '#94a3b8'}; font-size: 0.8rem; margin: 0;">
                        {phase['desc']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


# =============================================================================
# Phase 1: Universal Fact (Layer 1 - 불변 정보)
# =============================================================================

def render_phase1_universal_fact(scenario):
    """Phase 1: 회원가입 시 입력된 불변 정보 확인 (DB에서 로드)"""
    
    # DB에서 로드된 사용자 데이터 (Layer 1)
    user_data = st.session_state.get('user_data', {})
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{scenario.icon}</span>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">
                    {scenario.name} ({scenario.visa_type})
                </h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                회원가입 시 입력한 기본 정보를 확인해주세요. (Layer 1: Universal Fact)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 뒤로가기
    if st.button("← 다른 시나리오 선택"):
        st.session_state.selected_scenario = None
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.session_state.narrative_data = {}
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 카테고리별로 Layer 1 필드 표시
    categories = {
        "account": {"title": "1. 계정 정보", "icon": "👤"},
        "personal": {"title": "2. 인적사항", "icon": "📋"},
        "passport": {"title": "3. 여권 정보", "icon": "🛂"},
        "contact": {"title": "4. 연락처", "icon": "📞"},
    }
    
    # 카테고리별 필드 그룹화
    fields_by_category = {}
    for field in LAYER1_UNIVERSAL_FIELDS:
        cat = field.get('category', 'other')
        if cat not in fields_by_category:
            fields_by_category[cat] = []
        fields_by_category[cat].append(field)
    
    col1, col2 = st.columns(2)
    
    for idx, (cat_key, cat_info) in enumerate(categories.items()):
        col = col1 if idx % 2 == 0 else col2
        
        with col:
            st.markdown(f"""
                <div style="
                    background: #f8fafc;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin-bottom: 1rem;
                ">
                    <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                        {cat_info['icon']} {cat_info['title']}
                    </h4>
            """, unsafe_allow_html=True)
            
            fields = fields_by_category.get(cat_key, [])
            for field in fields:
                data_key = field['data_key']
                label = field['label']
                value = user_data.get(data_key, '-')
                
                # 비밀번호는 마스킹
                if data_key == 'password':
                    value = '••••••••'
                
                # 날짜 포맷팅
                if field['type'] == 'date' and value and value != '-':
                    try:
                        if isinstance(value, str):
                            value = value
                        else:
                            value = value.strftime('%Y-%m-%d')
                    except:
                        pass
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: #64748b; font-size: 0.85rem;">{label}</span>
                        <span style="color: #1e293b; font-weight: 500; font-size: 0.85rem;">{value or '-'}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
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
                        위 정보는 통합신청서의 기본 인적사항에 자동으로 채워집니다.
                    </p>
                    <p style="color: #3b82f6; font-size: 0.8rem; margin: 0.25rem 0 0 0;">
                        정보 수정이 필요하면 마이페이지에서 변경해주세요.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 다음 단계 버튼
    if st.button("정보 확인 완료 → Phase 2 시작", type="primary", use_container_width=True):
        st.session_state.form_step = 2
        st.rerun()


# =============================================================================
# Phase 2: Variable Fact (Layer 2 - 가변 정보)
# =============================================================================

def render_phase2_variable_fact(scenario):
    """Phase 2: 시나리오별 가변 정보 입력 (settings.py 기반 동적 생성)"""
    
    scenario_id = scenario.id
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{scenario.icon}</span>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">
                    {scenario.name} ({scenario.visa_type})
                </h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                시나리오별로 달라지는 정보를 입력해주세요. (Layer 2: Variable Fact)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 뒤로가기
    if st.button("← Phase 1로 돌아가기"):
        st.session_state.form_step = 1
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Layer 2 필드 가져오기
    layer2_fields = get_layer2_fields(scenario_id)
    
    if not layer2_fields:
        st.warning("이 시나리오에 대한 폼 설정이 없습니다.")
        return
    
    # 섹션별로 필드 그룹화
    sections = {}
    for field in layer2_fields:
        section = field.get('section', '기타')
        if section not in sections:
            sections[section] = []
        sections[section].append(field)
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # 폼 렌더링
    with st.form("phase2_form"):
        for section_name, fields in sections.items():
            st.markdown(f"**📁 {section_name}**")
            
            # 2열 레이아웃
            col1, col2 = st.columns(2)
            
            for idx, field in enumerate(fields):
                col = col1 if idx % 2 == 0 else col2
                
                with col:
                    render_form_field(field)
            
            st.markdown("---")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "다음: AI 코칭 시작 (Phase 3) →",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # 폼 데이터 저장
            save_layer2_data(layer2_fields)
            st.session_state.form_step = 3
            st.rerun()


def render_form_field(field: Dict):
    """개별 폼 필드 렌더링 (Layer 2 필드 정의 기반)"""
    
    data_key = field['data_key']
    label = field['label']
    field_type = field.get('type', 'text')
    placeholder = field.get('placeholder', '')
    required = field.get('required', False)
    options = field.get('options', [])
    
    # 현재 저장된 값
    current_value = st.session_state.form_data.get(data_key, '')
    
    label_display = f"{label} *" if required else label
    
    if field_type == 'text':
        st.text_input(
            label_display,
            key=data_key,
            value=current_value,
            placeholder=placeholder
        )
    
    elif field_type == 'textarea':
        st.text_area(
            label_display,
            key=data_key,
            value=current_value,
            placeholder=placeholder
        )
    
    elif field_type == 'number':
        min_val = field.get('min_value', 0)
        max_val = field.get('max_value', None)
        step = field.get('step', 1)
        
        kwargs = {
            'label': label_display,
            'key': data_key,
            'min_value': min_val,
            'step': step,
        }
        if max_val:
            kwargs['max_value'] = max_val
        if current_value:
            kwargs['value'] = int(current_value) if isinstance(current_value, (int, float)) else min_val
        
        st.number_input(**kwargs)
    
    elif field_type == 'select':
        default_idx = 0
        if current_value and current_value in options:
            default_idx = options.index(current_value)
        
        st.selectbox(
            label_display,
            options=options,
            key=data_key,
            index=default_idx
        )
    
    elif field_type == 'date':
        default_date = date.today()
        if current_value:
            try:
                if isinstance(current_value, str):
                    default_date = datetime.strptime(current_value, '%Y-%m-%d').date()
                else:
                    default_date = current_value
            except:
                pass
        
        st.date_input(
            label_display,
            key=data_key,
            value=default_date
        )


def save_layer2_data(fields: List[Dict]):
    """Layer 2 폼 데이터 저장"""
    form_data = {}
    
    for field in fields:
        data_key = field['data_key']
        if data_key in st.session_state:
            value = st.session_state[data_key]
            
            # 날짜 문자열 변환
            if hasattr(value, 'strftime'):
                value = value.strftime('%Y-%m-%d')
            
            form_data[data_key] = value
    
    st.session_state.form_data = form_data


# =============================================================================
# Phase 3: Narrative (Layer 3 - 서술형)
# =============================================================================

def render_phase3_narrative(scenario):
    """Phase 3: 서술형 데이터 입력 + AI 실시간 검토 (settings.py 기반)"""
    
    scenario_id = scenario.id
    
    # Layer 3 설정 가져오기
    narrative_config = get_narrative_config(scenario_id)
    layer3_fields = get_layer3_fields(scenario_id)
    danger_patterns = get_danger_patterns(scenario_id)
    
    # narrative_data 초기화
    if 'narrative_data' not in st.session_state:
        st.session_state.narrative_data = {}
    
    # AI 피드백 저장소 초기화
    if 'ai_feedbacks' not in st.session_state:
        st.session_state.ai_feedbacks = []
    
    narrative_label = narrative_config.get('narrative_label', '상세 내용')
    
    # 헤더
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">📝</span>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">
                    {scenario.name} - {narrative_label}
                </h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                각 항목에 대해 상세히 작성해주세요. AI가 실시간으로 내용을 검토합니다. (Layer 3: Narrative)
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2단 레이아웃
    form_col, feedback_col = st.columns([2, 1])
    
    with form_col:
        # 헤더 배지
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
                    {narrative_label}
                </span>
                <span style="
                    background: rgba(255,255,255,0.2);
                    color: white;
                    font-size: 0.7rem;
                    padding: 0.125rem 0.5rem;
                    border-radius: 1rem;
                    margin-left: auto;
                ">{len(layer3_fields)}개 항목</span>
            </div>
        """, unsafe_allow_html=True)
        
        # 각 Layer 3 필드에 대한 입력 영역
        for i, field in enumerate(layer3_fields):
            data_key = field['data_key']
            label = field['label']
            hint = field.get('hint', '')
            placeholder = field.get('placeholder', '')
            min_chars = field.get('min_chars', 50)
            required = field.get('required', False)
            
            if i > 0:
                st.divider()
            
            required_text = " *필수" if required else ""
            st.markdown(f"**Q{i+1}. {label}**{required_text}")
            st.caption(hint)
            
            # 현재 값
            current_value = st.session_state.narrative_data.get(data_key, '')
            
            # 텍스트 입력
            answer = st.text_area(
                f"답변 {i+1}",
                value=current_value,
                height=120,
                key=f"narrative_{data_key}",
                placeholder=placeholder,
                label_visibility="collapsed"
            )
            
            # 저장
            st.session_state.narrative_data[data_key] = answer
            
            # 글자 수 표시
            char_count = len(answer)
            color = "#22c55e" if char_count >= min_chars else "#ef4444"
            st.markdown(f"""
                <div style="text-align: right; font-size: 0.75rem; color: {color};">
                    {char_count}/{min_chars}자
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI 검토 요청 버튼
        col_validate, col_empty = st.columns([1, 1])
        with col_validate:
            if st.button("🤖 AI 검토 요청", use_container_width=True):
                run_ai_validation(scenario_id, layer3_fields, danger_patterns)
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
                missing_required = validate_required_fields(layer3_fields)
                
                if missing_required:
                    st.error(f"필수 항목을 작성해주세요: {', '.join(missing_required)}")
                else:
                    generate_documents(scenario)
    
    with feedback_col:
        render_feedback_panel(layer3_fields)


def run_ai_validation(scenario_id: str, fields: List[Dict], danger_patterns: List[str]):
    """AI 검토 실행"""
    
    feedbacks = []
    answers = st.session_state.get('narrative_data', {})
    
    for field in fields:
        data_key = field['data_key']
        answer = answers.get(data_key, '')
        label = field['label']
        min_chars = field.get('min_chars', 50)
        
        # 1. 글자 수 검증
        if len(answer) == 0:
            feedbacks.append({
                'field': label,
                'type': 'warning',
                'message': '아직 작성되지 않았습니다. 내용을 입력해주세요.'
            })
            continue
        elif len(answer) < min_chars:
            feedbacks.append({
                'field': label,
                'type': 'warning',
                'message': f'내용이 부족합니다. ({len(answer)}/{min_chars}자) 더 구체적으로 작성해주세요.'
            })
            continue
        
        # 2. 위험 표현 검사
        found_dangers = [p for p in danger_patterns if p in answer]
        if found_dangers:
            feedbacks.append({
                'field': label,
                'type': 'error',
                'message': f'위험 표현 감지: "{", ".join(found_dangers)}". 심사에서 불리할 수 있습니다.'
            })
            continue
        
        # 3. 구체성 검사
        import re
        has_date = bool(re.search(r'\d{4}년|\d{1,2}월|\d{1,2}일', answer))
        has_number = bool(re.search(r'\d+', answer))
        
        if not has_date and not has_number and len(answer) > 50:
            feedbacks.append({
                'field': label,
                'type': 'info',
                'message': '구체적인 날짜나 수치를 추가하면 더 설득력이 있습니다.'
            })
            continue
        
        # 4. 통과
        feedbacks.append({
            'field': label,
            'type': 'success',
            'message': '내용이 잘 작성되었습니다. ✓'
        })
    
    st.session_state.ai_feedbacks = feedbacks
    
    # 결과 요약
    errors = sum(1 for f in feedbacks if f['type'] == 'error')
    warnings = sum(1 for f in feedbacks if f['type'] == 'warning')
    
    if errors > 0:
        st.error(f"⚠️ {errors}개 항목에서 문제가 발견되었습니다.")
    elif warnings > 0:
        st.warning(f"💡 {warnings}개 항목에서 보완이 필요합니다.")
    else:
        st.success("✅ 모든 항목이 잘 작성되었습니다!")


def render_feedback_panel(fields: List[Dict]):
    """AI 피드백 패널 렌더링"""
    
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
            ">🧠 AI Validator 피드백</h4>
    """, unsafe_allow_html=True)
    
    feedbacks = st.session_state.get('ai_feedbacks', [])
    
    if feedbacks:
        for fb in feedbacks:
            fb_type = fb.get('type', 'info')
            
            styles = {
                'warning': {"icon": "⚠️", "bg": "#fef3c7", "border": "#fcd34d", "color": "#92400e"},
                'error': {"icon": "❌", "bg": "#fee2e2", "border": "#fca5a5", "color": "#991b1b"},
                'success': {"icon": "✅", "bg": "#dcfce7", "border": "#86efac", "color": "#166534"},
                'info': {"icon": "💡", "bg": "#dbeafe", "border": "#93c5fd", "color": "#1e40af"},
            }
            
            s = styles.get(fb_type, styles['info'])
            
            st.markdown(f"""
                <div style="
                    background: {s['bg']};
                    border: 1px solid {s['border']};
                    border-radius: 0.5rem;
                    padding: 0.75rem;
                    margin-bottom: 0.5rem;
                ">
                    <div style="font-size: 0.8rem; color: {s['color']}; font-weight: 600; margin-bottom: 0.25rem;">
                        {s['icon']} {fb.get('field', '전체')}
                    </div>
                    <div style="font-size: 0.75rem; color: {s['color']}; line-height: 1.5;">
                        {fb.get('message', '')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 1rem; color: #94a3b8; font-size: 0.8rem;">
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
            <h4 style="font-weight: 700; color: #1e293b; font-size: 0.9rem; margin: 0 0 0.75rem 0;">
                📋 검토 기준
            </h4>
            <ul style="font-size: 0.8rem; color: #64748b; padding-left: 1rem; margin: 0; line-height: 1.8;">
                <li><strong>구체성:</strong> 날짜, 장소, 이름 등 구체적 정보</li>
                <li><strong>진정성:</strong> 실제 경험과 감정 표현</li>
                <li><strong>적합성:</strong> 비자 목적에 맞는 내용</li>
                <li><strong>금지표현:</strong> 법적 문제 표현 감지</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # 작성 진행률
    total = len(fields)
    completed = 0
    
    for field in fields:
        data_key = field['data_key']
        min_chars = field.get('min_chars', 50)
        answer = st.session_state.narrative_data.get(data_key, '')
        if len(answer) >= min_chars:
            completed += 1
    
    progress = int((completed / total) * 100) if total > 0 else 0
    
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
        ">
            <h4 style="font-weight: 700; color: #1e293b; font-size: 0.9rem; margin: 0 0 0.75rem 0;">
                📊 작성 진행률
            </h4>
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
                "></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b;">
                <span>{completed}/{total} 항목 완료</span>
                <span style="font-weight: 600; color: {'#22c55e' if progress == 100 else '#64748b'};">{progress}%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def validate_required_fields(fields: List[Dict]) -> List[str]:
    """필수 항목 검증"""
    missing = []
    
    for field in fields:
        if field.get('required', False):
            data_key = field['data_key']
            min_chars = field.get('min_chars', 50)
            answer = st.session_state.narrative_data.get(data_key, '')
            
            if len(answer) < min_chars:
                missing.append(field['label'])
    
    return missing


def generate_documents(scenario):
    """문서 생성 및 페이지 이동 (프로그레스 바 포함)"""
    from services.document_service import DocumentService
    from templates.mapping_guide import get_scenario_documents
    
    # 모든 레이어 데이터 수집
    user_data = st.session_state.get('user_data', {})
    form_data = st.session_state.get('form_data', {})
    narrative_data = st.session_state.get('narrative_data', {})
    
    # 시나리오별 필요 문서 목록
    required_docs = get_scenario_documents(scenario.id)
    if not required_docs:
        required_docs = scenario.required_docs
    
    total_docs = len(required_docs)
    
    # 프로그레스 바 컨테이너
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
            border: 2px solid #a855f7;
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
        ">
            <h3 style="color: #7c3aed; margin: 0 0 1rem 0;">📄 문서 생성 중...</h3>
        </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    doc_service = DocumentService()
    
    # ZIP 패키지 생성 (진행률 표시)
    import io
    import zipfile
    from datetime import datetime
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, doc_name in enumerate(required_docs):
            # 진행률 업데이트
            progress = int(((idx + 1) / (total_docs + 1)) * 100)
            progress_bar.progress(progress)
            status_text.markdown(f"""
                <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
                    📝 <strong>{doc_name}</strong> 생성 중... ({idx + 1}/{total_docs})
                </div>
            """, unsafe_allow_html=True)
            
            try:
                doc_bytes = doc_service.generate_document(
                    doc_name, user_data, form_data, narrative_data
                )
                
                safe_name = doc_name.replace(' ', '_').replace('/', '_')
                
                # 확장자 결정
                if len(doc_bytes) >= 4 and doc_bytes[:4] == b'PK\x03\x04':
                    filename = f"{safe_name}.docx"
                else:
                    filename = f"{safe_name}.txt"
                
                zip_file.writestr(filename, doc_bytes)
                
            except Exception as e:
                error_content = f"문서 생성 오류: {str(e)}"
                zip_file.writestr(f"ERROR_{doc_name}.txt", error_content.encode('utf-8'))
        
        # README 추가
        status_text.markdown("""
            <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
                📋 <strong>README</strong> 생성 중...
            </div>
        """, unsafe_allow_html=True)
        
        readme_content = doc_service._create_readme(scenario, required_docs, datetime.now())
        zip_file.writestr("README.txt", readme_content.encode('utf-8'))
    
    # 완료
    progress_bar.progress(100)
    status_text.markdown("""
        <div style="text-align: center; color: #22c55e; font-size: 0.9rem; font-weight: 600;">
            ✅ 모든 문서 생성 완료!
        </div>
    """, unsafe_allow_html=True)
    
    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()
    
    if zip_bytes:
        st.session_state.generated_zip = zip_bytes
        st.session_state.current_page = 'document_preview'
        import time
        time.sleep(0.5)  # 완료 메시지 잠깐 보여주기
        st.rerun()