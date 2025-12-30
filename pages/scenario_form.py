"""
K-Stay Scenario Form Page
4-Phase Architecture (settings.py 기반 동적 생성)
- Phase 1: Universal Fact (Layer 1) - 회원가입 시 입력, DB에서 로드
- Phase 2: Variable Fact (Layer 2) - 시나리오별 Smart Form (target별 그룹화)
- Phase 3: Narrative (Layer 3) - AI 실시간 검토 & 코칭
- Phase 4: Payment & Document Generation - 결제 후 문서 생성
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
    TARGET_INFO,
    get_layer2_fields,
    get_layer2_field_groups,
    get_layer3_fields,
    get_danger_patterns,
    get_narrative_config,
)
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
    
    # 새로고침 경고 (Phase 2, 3에서만)
    if current_step in [2, 3]:
        st.warning("⚠️ 주의: 새로고침 또는 페이지 이탈 시 작성 중인 내용이 저장되지 않을 수 있습니다.")
    
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


def render_phase_indicator(current_step: int):
    """4-Phase 진행 상태 표시"""
    
    phases = [
        {"name": "Universal Fact", "desc": "불변 정보 확인", "color": "#22c55e"},
        {"name": "Variable Fact", "desc": "가변 정보 입력", "color": "#3b82f6"},
        {"name": "Narrative", "desc": "정성 사연", "color": "#a855f7"},
        {"name": "Payment", "desc": "결제 & 문서생성", "color": "#f59e0b"},
    ]
    
    cols = st.columns(4)
    
    for i, (col, phase) in enumerate(zip(cols, phases)):
        step_num = i + 1
        is_active = current_step == step_num
        is_done = current_step > step_num
        
        with col:
            # 변수로 미리 계산
            if is_active:
                bg_color = phase['color'] + "15"
                border_color = phase['color']
                badge_text = "● PHASE " + str(step_num)
                shadow = "box-shadow: 0 4px 12px " + phase['color'] + "40;"
                badge_bg = phase['color']
                title_color = "#1e293b"
                desc_color = "#64748b"
            elif is_done:
                bg_color = "#f0fdf4"
                border_color = "#86efac"
                badge_text = "✓ PHASE " + str(step_num)
                shadow = ""
                badge_bg = "#22c55e"
                title_color = "#1e293b"
                desc_color = "#64748b"
            else:
                bg_color = "#f1f5f9"
                border_color = "#cbd5e1"
                badge_text = "PHASE " + str(step_num)
                shadow = ""
                badge_bg = "#94a3b8"
                title_color = "#64748b"
                desc_color = "#94a3b8"
            
            html = f"""
                <div style="background: {bg_color}; border-radius: 0.75rem; padding: 1rem; border: 2px solid {border_color}; min-height: 100px; {shadow}">
                    <div style="background: {badge_bg}; color: white; font-size: 0.65rem; font-weight: 700; padding: 0.2rem 0.4rem; border-radius: 0.25rem; display: inline-block; margin-bottom: 0.5rem;">{badge_text}</div>
                    <h3 style="color: {title_color}; font-size: 0.9rem; font-weight: 700; margin: 0.25rem 0;">{phase['name']}</h3>
                    <p style="color: {desc_color}; font-size: 0.7rem; margin: 0;">{phase['desc']}</p>
                </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


# =============================================================================
# Phase 1: Universal Fact (Layer 1 - 불변 정보)
# =============================================================================

def render_phase1_universal_fact(scenario):
    """Phase 1: 회원가입 시 입력된 불변 정보 확인 (DB에서 로드)"""
    
    user_data = st.session_state.get('user_data', {})
    
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
    
    if st.button("← 다른 시나리오 선택"):
        st.session_state.selected_scenario = None
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.session_state.narrative_data = {}
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 카테고리별 표시
    categories = {
        "account": {"title": "1. 계정 정보", "icon": "👤"},
        "personal": {"title": "2. 인적사항", "icon": "📋"},
        "passport": {"title": "3. 여권 정보", "icon": "🛂"},
        "contact": {"title": "4. 연락처", "icon": "📞"},
    }
    
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
                <div style="background: #f8fafc; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem;">
                    <h4 style="color: #1e293b; font-size: 0.9rem; font-weight: 600; margin: 0 0 0.75rem 0;">
                        {cat_info['icon']} {cat_info['title']}
                    </h4>
            """, unsafe_allow_html=True)
            
            fields = fields_by_category.get(cat_key, [])
            for field in fields:
                data_key = field['data_key']
                label = field['label']
                value = user_data.get(data_key, '-')
                
                if data_key == 'password':
                    value = '••••••••'
                
                if field['type'] == 'date' and value and value != '-':
                    try:
                        if hasattr(value, 'strftime'):
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
    
    st.markdown("""
        <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 0.5rem; padding: 1rem; margin: 1.5rem 0;">
            <p style="color: #1e40af; font-size: 0.85rem; margin: 0;">
                ℹ️ 위 정보는 통합신청서의 기본 인적사항에 자동으로 채워집니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("정보 확인 완료 → Phase 2 시작", type="primary", use_container_width=True):
        st.session_state.form_step = 2
        st.rerun()


# =============================================================================
# Phase 2: Variable Fact (Layer 2 - 가변 정보)
# =============================================================================

def render_phase2_variable_fact(scenario):
    """Phase 2: 시나리오별 가변 정보 입력 (field_groups 기반 target별 그룹화)"""
    
    scenario_id = scenario.id
    
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
    
    # Layer 2 필드 그룹 가져오기 (target별 그룹화)
    field_groups = get_layer2_field_groups(scenario_id)
    
    if not field_groups:
        st.warning("이 시나리오에 대한 폼 설정이 없습니다.")
        if st.button("다음 단계로 →"):
            st.session_state.form_step = 3
            st.rerun()
        return
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # 폼 렌더링 (target별 그룹으로 구분)
    with st.form("phase2_form"):
        for group in field_groups:
            target = group.get('target', 'self')
            group_name = group.get('group_name', '기타')
            group_name_en = group.get('group_name_en', 'Other')
            fields = group.get('fields', [])
            
            # target에 따른 아이콘 선택
            target_icons = {
                "other_guarantor": "🤝",
                "other_spouse": "💑",
                "other_inviter": "📨",
                "other_employer": "🏢",
                "other_family": "👨‍👩‍👧",
                "other_introducer": "🔗",
                "other_reference": "📋",
                "self": "👤",
            }
            icon = target_icons.get(target, "📁")
            
            # 그룹 헤더
            st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    border-radius: 0.5rem;
                    padding: 0.75rem 1rem;
                    margin: 1rem 0 0.75rem 0;
                ">
                    <span style="font-size: 1rem; margin-right: 0.5rem;">{icon}</span>
                    <span style="color: white; font-weight: 600; font-size: 0.95rem;">
                        {group_name}
                    </span>
                    <span style="color: rgba(255,255,255,0.7); font-size: 0.8rem; margin-left: 0.5rem;">
                        {group_name_en}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # 2열 레이아웃으로 필드 표시
            col1, col2 = st.columns(2)
            
            for idx, field in enumerate(fields):
                col = col1 if idx % 2 == 0 else col2
                with col:
                    render_form_field(field)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        col_back, col_next = st.columns(2)
        
        with col_back:
            back_btn = st.form_submit_button("← Phase 1로", use_container_width=True)
        
        with col_next:
            next_btn = st.form_submit_button("다음: AI 코칭 (Phase 3) →", type="primary", use_container_width=True)
        
        if back_btn:
            st.session_state.form_step = 1
            st.rerun()
        
        if next_btn:
            # 폼 데이터 저장
            save_layer2_data(field_groups)
            st.session_state.form_step = 3
            st.rerun()


def render_form_field(field: Dict):
    """개별 폼 필드 렌더링"""
    
    data_key = field['data_key']
    label = field.get('label', data_key)
    label_en = field.get('label_en', '')
    field_type = field.get('type', 'text')
    placeholder = field.get('placeholder', '')
    required = field.get('required', False)
    options = field.get('options', [])
    
    current_value = st.session_state.form_data.get(data_key, '')
    
    # 라벨 표시 (한글 + 영문)
    if label_en:
        label_display = f"{label} ({label_en})"
    else:
        label_display = label
    
    if required:
        label_display += " *"
    
    if field_type == 'text':
        st.text_input(label_display, key=data_key, value=current_value, placeholder=placeholder)
    
    elif field_type == 'textarea':
        st.text_area(label_display, key=data_key, value=current_value, placeholder=placeholder)
    
    elif field_type == 'number':
        min_val = field.get('min_value', 0)
        max_val = field.get('max_value', None)
        step = field.get('step', 1)
        
        kwargs = {'label': label_display, 'key': data_key, 'min_value': min_val, 'step': step}
        if max_val:
            kwargs['max_value'] = max_val
        if current_value:
            try:
                kwargs['value'] = int(current_value) if isinstance(current_value, (int, float, str)) else min_val
            except:
                kwargs['value'] = min_val
        
        st.number_input(**kwargs)
    
    elif field_type == 'select':
        if not options:
            options = ['']
        
        default_idx = 0
        if current_value and current_value in options:
            default_idx = options.index(current_value)
        st.selectbox(label_display, options=options, key=data_key, index=default_idx)
    
    elif field_type == 'date':
        default_date = date.today()
        if current_value:
            try:
                if isinstance(current_value, str):
                    default_date = datetime.strptime(current_value, '%Y-%m-%d').date()
                elif isinstance(current_value, date):
                    default_date = current_value
            except:
                pass
        st.date_input(label_display, key=data_key, value=default_date)


def save_layer2_data(field_groups: List[Dict]):
    """Layer 2 폼 데이터 저장 (field_groups 구조에서)"""
    form_data = {}
    
    for group in field_groups:
        fields = group.get('fields', [])
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
    """Phase 3: 서술형 데이터 입력 + AI 실시간 검토"""
    
    scenario_id = scenario.id
    narrative_config = get_narrative_config(scenario_id)
    layer3_fields = get_layer3_fields(scenario_id)
    danger_patterns = get_danger_patterns(scenario_id)
    
    if 'narrative_data' not in st.session_state:
        st.session_state.narrative_data = {}
    
    if 'ai_feedbacks' not in st.session_state:
        st.session_state.ai_feedbacks = []
    
    narrative_label = narrative_config.get('narrative_label', '상세 내용')
    narrative_label_en = narrative_config.get('narrative_label_en', 'Details')
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">📝</span>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">
                    {scenario.name} - {narrative_label}
                </h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                각 항목에 대해 상세히 작성해주세요. AI가 실시간으로 내용을 검토합니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    form_col, feedback_col = st.columns([2, 1])
    
    with form_col:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
                border-radius: 0.75rem;
                padding: 1rem 1.25rem;
                margin-bottom: 1.5rem;
            ">
                <span style="font-size: 1.25rem;">✍️</span>
                <span style="font-weight: 600; color: white; font-size: 0.95rem; margin-left: 0.5rem;">
                    {narrative_label}
                </span>
                <span style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-left: 0.25rem;">
                    ({narrative_label_en})
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
        
        for i, field in enumerate(layer3_fields):
            data_key = field['data_key']
            label = field.get('label', data_key)
            label_en = field.get('label_en', '')
            hint = field.get('hint', '')
            hint_en = field.get('hint_en', '')
            placeholder = field.get('placeholder', '')
            min_chars = field.get('min_chars', 50)
            required = field.get('required', False)
            
            if i > 0:
                st.divider()
            
            required_text = " *필수" if required else ""
            label_full = f"{label} ({label_en})" if label_en else label
            st.markdown(f"**Q{i+1}. {label_full}**{required_text}")
            
            hint_full = f"{hint}" if hint else ""
            if hint_en:
                hint_full += f" / {hint_en}"
            st.caption(hint_full)
            
            current_value = st.session_state.narrative_data.get(data_key, '')
            
            answer = st.text_area(
                f"답변 {i+1}",
                value=current_value,
                height=120,
                key=f"narrative_{data_key}",
                placeholder=placeholder,
                label_visibility="collapsed"
            )
            
            st.session_state.narrative_data[data_key] = answer
            
            char_count = len(answer)
            color = "#22c55e" if char_count >= min_chars else "#ef4444"
            st.markdown(f'<div style="text-align: right; font-size: 0.75rem; color: {color};">{char_count}/{min_chars}자</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_validate, col_empty = st.columns([1, 1])
        with col_validate:
            if st.button("🤖 AI 검토 요청", use_container_width=True):
                run_ai_validation(scenario_id, layer3_fields, danger_patterns)
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_back, col_next = st.columns(2)
        
        with col_back:
            if st.button("← Phase 2로 돌아가기", use_container_width=True):
                st.session_state.form_step = 2
                st.rerun()
        
        with col_next:
            if st.button("✓ 작성 완료 → 결제하기", use_container_width=True, type="primary"):
                missing_required = validate_required_fields(layer3_fields)
                
                if missing_required:
                    st.error(f"필수 항목을 작성해주세요: {', '.join(missing_required)}")
                else:
                    st.session_state.form_step = 4
                    st.rerun()
    
    with feedback_col:
        render_feedback_panel(layer3_fields)


def run_ai_validation(scenario_id: str, fields: List[Dict], danger_patterns: List[str]):
    """AI 검토 실행"""
    import re
    
    feedbacks = []
    answers = st.session_state.get('narrative_data', {})
    
    for field in fields:
        data_key = field['data_key']
        answer = answers.get(data_key, '')
        label = field.get('label', data_key)
        min_chars = field.get('min_chars', 50)
        
        if len(answer) == 0:
            feedbacks.append({'field': label, 'type': 'warning', 'message': '아직 작성되지 않았습니다.'})
            continue
        elif len(answer) < min_chars:
            feedbacks.append({'field': label, 'type': 'warning', 'message': f'내용이 부족합니다. ({len(answer)}/{min_chars}자)'})
            continue
        
        found_dangers = [p for p in danger_patterns if p in answer]
        if found_dangers:
            feedbacks.append({'field': label, 'type': 'error', 'message': f'위험 표현 감지: "{", ".join(found_dangers)}"'})
            continue
        
        has_date = bool(re.search(r'\d{4}년|\d{1,2}월|\d{1,2}일', answer))
        has_number = bool(re.search(r'\d+', answer))
        
        if not has_date and not has_number and len(answer) > 50:
            feedbacks.append({'field': label, 'type': 'info', 'message': '구체적인 날짜나 수치를 추가하면 더 설득력이 있습니다.'})
            continue
        
        feedbacks.append({'field': label, 'type': 'success', 'message': '내용이 잘 작성되었습니다. ✓'})
    
    st.session_state.ai_feedbacks = feedbacks
    
    errors = sum(1 for f in feedbacks if f['type'] == 'error')
    warnings = sum(1 for f in feedbacks if f['type'] == 'warning')
    
    if errors > 0:
        st.error(f"⚠️ {errors}개 항목에서 문제가 발견되었습니다.")
    elif warnings > 0:
        st.warning(f"💡 {warnings}개 항목에서 보완이 필요합니다.")
    else:
        st.success("✅ 모든 항목이 잘 작성되었습니다!")


def render_feedback_panel(fields: List[Dict]):
    """AI 피드백 패널 (Fixed)"""
    
    # 진행률 계산
    total = len(fields)
    completed = sum(1 for f in fields if len(st.session_state.narrative_data.get(f['data_key'], '')) >= f.get('min_chars', 50))
    progress = int((completed / total) * 100) if total > 0 else 0
    
    # 피드백 데이터
    feedbacks = st.session_state.get('ai_feedbacks', [])
    
    # 피드백 HTML 생성
    feedback_html = ""
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
            feedback_html += f"""
                <div style="background: {s['bg']}; border: 1px solid {s['border']}; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 0.5rem;">
                    <div style="font-size: 0.8rem; color: {s['color']}; font-weight: 600;">{s['icon']} {fb.get('field', '')}</div>
                    <div style="font-size: 0.75rem; color: {s['color']};">{fb.get('message', '')}</div>
                </div>
            """
    else:
        feedback_html = '<div style="text-align: center; padding: 1rem; color: #94a3b8; font-size: 0.8rem;">아직 검토 결과가 없습니다.<br>\'AI 검토 요청\' 버튼을 클릭하세요.</div>'
    
    progress_color = '#22c55e' if progress == 100 else '#64748b'
    
    # Fixed 스타일 CSS 주입
    st.markdown("""
        <style>
        .fixed-feedback-panel {
            position: fixed;
            top: 380px;
            right: 2rem;
            width: 280px;
            max-height: calc(100vh - 420px);
            z-index: 999;
            overflow-y: auto;
        }
        @media (max-width: 1200px) {
            .fixed-feedback-panel {
                position: relative;
                top: 0;
                right: 0;
                width: 100%;
                max-height: none;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Fixed 컨테이너로 전체 패널 렌더링
    st.markdown(f"""
        <div class="fixed-feedback-panel">
            <div style="background: linear-gradient(135deg, #fef2f2, #fee2e2); border: 1px solid #fecaca; border-radius: 0.75rem; padding: 1.25rem; margin-bottom: 1rem;">
                <h4 style="font-weight: 700; color: #dc2626; font-size: 0.9rem; margin: 0 0 0.75rem 0;">🧠 AI Validator 피드백</h4>
                {feedback_html}
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 0.75rem; padding: 1.25rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <h4 style="font-weight: 700; color: #1e293b; font-size: 0.9rem; margin: 0 0 0.75rem 0;">📊 작성 진행률</h4>
                <div style="background: #e2e8f0; border-radius: 0.5rem; height: 8px; margin-bottom: 0.5rem; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #22c55e, #16a34a); height: 100%; width: {progress}%; border-radius: 0.5rem;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b;">
                    <span>{completed}/{total} 항목 완료</span>
                    <span style="font-weight: 600; color: {progress_color};">{progress}%</span>
                </div>
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
                missing.append(field.get('label', data_key))
    
    return missing


# =============================================================================
# Phase 4: Payment & Document Generation (결제 후 문서 생성)
# =============================================================================

def render_phase4_payment(scenario):
    """Phase 4: 결제 후 문서 생성"""
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">💳</span>
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">
                    {scenario.name} - 결제 & 문서 생성
                </h2>
            </div>
            <p style="color: #64748b; font-size: 0.95rem;">
                결제 완료 후 문서가 자동으로 생성됩니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    is_paid = st.session_state.get('is_paid', False)
    is_admin = st.session_state.get('is_admin', False)
    
    if is_paid or is_admin:
        st.success("✅ Premium 활성화 상태입니다!")
        
        st.markdown(f"""
            <div style="background: #f0fdf4; border: 2px solid #22c55e; border-radius: 1rem; padding: 1.5rem; text-align: center; margin: 1rem 0;">
                <h3 style="color: #166534; margin: 0 0 0.5rem 0;">📄 생성될 문서 ({len(scenario.required_docs)}개)</h3>
                <p style="color: #15803d; font-size: 0.9rem; margin: 0;">
                    {', '.join(scenario.required_docs)}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 문서 생성하기", type="primary", use_container_width=True):
            generate_documents(scenario)
    else:
        render_payment_section(scenario)
    
    st.markdown("---")
    
    if st.button("← Phase 3로 돌아가기", use_container_width=True):
        st.session_state.form_step = 3
        st.rerun()


def render_payment_section(scenario):
    """결제 섹션"""
    
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
        
        # 결제 세션이 없으면 생성 버튼 표시
        if 'checkout_url' not in st.session_state or not st.session_state.checkout_url:
            if st.button("💳 카드 결제하기", type="primary", use_container_width=True):
                user_id = st.session_state.get('user_id', '')
                user_email = st.session_state.get('user_email', '')
                
                with st.spinner("결제 페이지 생성 중..."):
                    checkout_url, session_id = payment_service.create_checkout_session(user_id, user_email)
                
                if checkout_url and session_id:
                    st.session_state.checkout_url = checkout_url
                    st.session_state.checkout_session_id = session_id
                    st.rerun()
        
        # 결제 링크가 있으면 표시
        if st.session_state.get('checkout_url'):
            url = st.session_state.checkout_url
            session_id = st.session_state.get('checkout_session_id', '')
            
            st.markdown("### 🔗 결제 링크")
            st.markdown(f"[**👉 여기를 클릭하여 결제 페이지로 이동**]({url})")
            st.text_input("또는 URL 복사:", value=url, key="payment_url")
            
            st.markdown("---")
            
            # 결제 상태 확인 버튼
            st.info("💡 결제 완료 후 아래 버튼을 눌러 결제를 확인해주세요.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 결제 상태 확인", use_container_width=True):
                    with st.spinner("결제 상태 확인 중..."):
                        is_paid, payment_info = payment_service.verify_payment(session_id)
                    
                    if is_paid:
                        # 결제 확인됨 - DB 업데이트
                        user_id = st.session_state.get('user_id', '')
                        payment_service.record_payment_to_db(user_id, payment_info)
                        
                        st.session_state.is_paid = True
                        st.session_state.checkout_url = None
                        st.session_state.checkout_session_id = None
                        st.session_state.payment_verified = True
                        
                        st.success("🎉 결제가 확인되었습니다! Premium이 활성화되었습니다!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ 결제가 아직 완료되지 않았습니다. 결제를 완료한 후 다시 확인해주세요.")
            
            with col2:
                if st.button("❌ 결제 취소", use_container_width=True):
                    st.session_state.checkout_url = None
                    st.session_state.checkout_session_id = None
                    st.rerun()
            
            # 안내 메시지
            st.markdown("""
            <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 0.5rem; padding: 1rem; margin-top: 1rem;">
                <p style="color: #92400e; margin: 0; font-size: 0.85rem;">
                    ⚠️ <strong>참고:</strong> 결제 페이지에서 카드 정보 입력 후 결제를 완료해야 합니다.<br>
                    결제 완료 후 이 페이지로 돌아와서 "결제 상태 확인" 버튼을 클릭해주세요.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.warning("⚠️ Stripe 미연결 - 테스트 모드")
        
        if st.button("🧪 테스트 결제 (무료)", type="primary", use_container_width=True):
            st.session_state.is_paid = True
            st.success("🎉 테스트 결제 완료!")
            st.rerun()


def generate_documents(scenario):
    """문서 생성 및 페이지 이동"""
    from services.document_service import DocumentService
    
    user_data = st.session_state.get('user_data', {})
    form_data = st.session_state.get('form_data', {})
    narrative_data = st.session_state.get('narrative_data', {})
    
    required_docs = scenario.required_docs
    total_docs = len(required_docs)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(168, 85, 247, 0.1)); border: 2px solid #a855f7; border-radius: 1rem; padding: 2rem; text-align: center; margin: 1rem 0;">
            <h3 style="color: #7c3aed; margin: 0 0 1rem 0;">📄 문서 생성 중...</h3>
        </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    doc_service = DocumentService()
    
    import io
    import zipfile
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, doc_name in enumerate(required_docs):
            progress = int(((idx + 1) / (total_docs + 1)) * 100)
            progress_bar.progress(progress)
            status_text.markdown(f'<div style="text-align: center; color: #64748b;">📝 <strong>{doc_name}</strong> 생성 중... ({idx + 1}/{total_docs})</div>', unsafe_allow_html=True)
            
            try:
                doc_bytes = doc_service.generate_document(doc_name, user_data, form_data, narrative_data)
                safe_name = doc_name.replace(' ', '_').replace('/', '_')
                
                if len(doc_bytes) >= 4 and doc_bytes[:4] == b'PK\x03\x04':
                    filename = f"{safe_name}.docx"
                else:
                    filename = f"{safe_name}.txt"
                
                zip_file.writestr(filename, doc_bytes)
            except Exception as e:
                error_content = f"문서 생성 오류: {str(e)}"
                zip_file.writestr(f"ERROR_{doc_name}.txt", error_content.encode('utf-8'))
        
        readme_content = f"""
K-Stay 문서 패키지
==================
시나리오: {scenario.name} ({scenario.visa_type})
생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

포함 문서:
{chr(10).join(f'- {doc}' for doc in required_docs)}

문의: support@k-stay.com
"""
        zip_file.writestr("README.txt", readme_content.encode('utf-8'))
    
    progress_bar.progress(100)
    status_text.markdown('<div style="text-align: center; color: #22c55e; font-weight: 600;">✅ 모든 문서 생성 완료!</div>', unsafe_allow_html=True)
    
    zip_buffer.seek(0)
    st.session_state.generated_zip = zip_buffer.getvalue()
    st.session_state.current_page = 'document_preview'
    
    import time
    time.sleep(0.5)
    st.rerun()