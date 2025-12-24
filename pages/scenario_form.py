"""
K-Stay Scenario Form Page
Phase 1-2: Variable Fact + AI Chat Interview
Clean White/Blue Theme
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
    
    if current_step == 1:
        render_phase1_form(scenario)
    elif current_step == 2:
        render_phase2_chat(scenario)


def render_phase1_form(scenario):
    """Phase 1: 기본 정보 입력 (Smart Form)"""
    
    # 진행 단계 표시
    st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
        ">
            <span style="color: #2563eb !important;">Step 1. 기본 정보</span>
            <span style="color: #cbd5e1 !important;">›</span>
            <span style="color: #64748b !important;">Step 2. AI 인터뷰</span>
        </div>
        <h2 style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b !important;
            margin: 0 0 0.5rem 0;
        ">{scenario.visa_type} 비자 - 기본 정보 입력</h2>
        <p style="color: #475569 !important; margin-bottom: 1.5rem;">
            여권 정보와 기본적인 인적 사항을 입력해주세요.
        </p>
    """, unsafe_allow_html=True)
    
    # 뒤로가기
    if st.button("← 다른 시나리오 선택"):
        st.session_state.selected_scenario = None
        st.session_state.form_step = 1
        st.session_state.form_data = {}
        st.session_state.current_page = 'dashboard'
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    user_data = st.session_state.get('user_data', {})
    
    # 폼 컨테이너
    with st.container():
        st.markdown("""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.5rem;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            "></div>
        """, unsafe_allow_html=True)
        
        with st.form("phase1_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "성명 (Full Name)",
                    value=f"{user_data.get('surname', '')} {user_data.get('given_name', '')}".strip(),
                    placeholder="HONG GIL DONG"
                )
            
            with col2:
                passport = st.text_input(
                    "여권번호",
                    value=user_data.get('passport_no', ''),
                    placeholder="M12345678"
                )
            
            col3, col4 = st.columns(2)
            
            with col3:
                nationality = st.selectbox(
                    "국적",
                    options=["USA", "Vietnam", "China", "Uzbekistan", "기타"],
                    index=0
                )
            
            with col4:
                job_category = st.selectbox(
                    "희망 직무",
                    options=["IT/SW 개발", "마케팅/영업", "무역/유통", "디자인", "기타"]
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button(
                "다음: AI 인터뷰 시작 →",
                type="primary",
                use_container_width=True
            )
            
            if submitted:
                if not name or not passport:
                    st.error("필수 정보(성명, 여권번호)를 입력해주세요.")
                else:
                    st.session_state.form_data = {
                        'name': name,
                        'passport': passport,
                        'nationality': nationality,
                        'job_category': job_category
                    }
                    
                    initial_greeting = {
                        'role': 'assistant',
                        'content': f"안녕하세요! {job_category} 분야 구직을 희망하시는군요. 구직활동계획서 작성을 도와드리겠습니다. 구체적으로 어떤 회사나 직무를 목표로 하고 계신가요?"
                    }
                    st.session_state.chat_history = [initial_greeting]
                    st.session_state.form_step = 2
                    st.rerun()


def render_phase2_chat(scenario):
    """Phase 2: AI 인터뷰 (Chat Interface)"""
    
    # 진행 단계 표시
    st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 1rem;
        ">
            <span style="color: #22c55e !important;">✓ Step 1. 기본 정보</span>
            <span style="color: #cbd5e1 !important;">›</span>
            <span style="color: #2563eb !important;">Step 2. AI 인터뷰</span>
        </div>
    """, unsafe_allow_html=True)
    
    # 2단 레이아웃
    chat_col, info_col = st.columns([2, 1])
    
    with chat_col:
        # 채팅 헤더
        st.markdown("""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem 0.75rem 0 0;
                padding: 1rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: none;
            ">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="
                        width: 8px;
                        height: 8px;
                        background: #22c55e;
                        border-radius: 50%;
                    "></div>
                    <span style="font-weight: 600; color: #1e293b !important;">AI 행정사 인터뷰</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 채팅 메시지 영역
        chat_area = st.container()
        
        with chat_area:
            for msg in st.session_state.get('chat_history', []):
                if msg['role'] == 'user':
                    st.markdown(f"""
                        <div style="
                            display: flex;
                            justify-content: flex-end;
                            margin-bottom: 0.75rem;
                            padding: 0 1rem;
                        ">
                            <div style="
                                background: #2563eb;
                                color: white !important;
                                padding: 0.75rem 1rem;
                                border-radius: 1rem;
                                border-top-right-radius: 0.25rem;
                                max-width: 80%;
                                font-size: 0.9rem;
                                line-height: 1.5;
                            ">{msg['content']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="
                            display: flex;
                            justify-content: flex-start;
                            margin-bottom: 0.75rem;
                            padding: 0 1rem;
                        ">
                            <div style="
                                background: white;
                                border: 1px solid #e2e8f0;
                                color: #1e293b !important;
                                padding: 0.75rem 1rem;
                                border-radius: 1rem;
                                border-top-left-radius: 0.25rem;
                                max-width: 80%;
                                font-size: 0.9rem;
                                line-height: 1.5;
                                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                            ">{msg['content']}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # 입력 영역
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_btn = st.columns([5, 1])
            
            with col_input:
                user_message = st.text_input(
                    "메시지",
                    placeholder="계획을 편하게 이야기해주세요...",
                    label_visibility="collapsed"
                )
            
            with col_btn:
                send_btn = st.form_submit_button("전송", type="primary", use_container_width=True)
            
            if send_btn and user_message:
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message
                })
                
                ai_service = AIService()
                response = ai_service.chat_response(
                    user_message,
                    st.session_state.chat_history,
                    ""
                )
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✓ 인터뷰 종료 및 문서 생성", use_container_width=True, type="primary"):
            # 문서 생성 및 미리보기 페이지로 이동
            from services.document_service import DocumentService
            
            doc_service = DocumentService()
            zip_bytes = doc_service.generate_full_package(
                scenario.id,
                st.session_state.get('user_data', {}),
                st.session_state.get('form_data', {}),
                {'chat_history': st.session_state.get('chat_history', [])}
            )
            
            if zip_bytes:
                st.session_state.generated_zip = zip_bytes
                st.session_state.current_page = 'document_preview'
                st.rerun()
    
    with info_col:
        form_data = st.session_state.get('form_data', {})
        
        # 정보 요약 패널
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.25rem;
                margin-bottom: 1rem;
            ">
                <h4 style="
                    font-weight: 700;
                    color: #1e293b !important;
                    font-size: 0.9rem;
                    margin: 0 0 0.75rem 0;
                ">📄 실시간 정보 요약</h4>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.5rem 0;
                    border-bottom: 1px solid #f1f5f9;
                    font-size: 0.85rem;
                ">
                    <span style="color: #64748b !important;">신청자</span>
                    <span style="font-weight: 500; color: #1e293b !important;">{form_data.get('name', 'N/A')}</span>
                </div>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.5rem 0;
                    border-bottom: 1px solid #f1f5f9;
                    font-size: 0.85rem;
                ">
                    <span style="color: #64748b !important;">비자 타입</span>
                    <span style="
                        font-weight: 500;
                        color: #2563eb !important;
                        background: #dbeafe;
                        padding: 0.125rem 0.5rem;
                        border-radius: 0.25rem;
                        font-size: 0.75rem;
                    ">{scenario.visa_type}</span>
                </div>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.5rem 0;
                    font-size: 0.85rem;
                ">
                    <span style="color: #64748b !important;">목표</span>
                    <span style="font-weight: 500; color: #1e293b !important;">{form_data.get('job_category', 'N/A')}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # RAG 가이드 패널
        st.markdown(f"""
            <div style="
                background: #dbeafe;
                border: 1px solid rgba(37, 99, 235, 0.2);
                border-radius: 0.75rem;
                padding: 1.25rem;
            ">
                <h4 style="
                    font-weight: 700;
                    color: #1e40af !important;
                    font-size: 0.9rem;
                    margin: 0 0 0.75rem 0;
                ">📚 하이코리아 심사 기준</h4>
                
                <ul style="
                    font-size: 0.8rem;
                    color: #1e40af !important;
                    padding-left: 1rem;
                    margin: 0;
                    line-height: 1.8;
                ">
                    <li style="color: #1e40af !important;">구직활동계획서 작성 시 월별 계획이 구체적이어야 함</li>
                    <li style="color: #1e40af !important;">단순 어학연수는 불허될 가능성 높음</li>
                    <li style="color: #1e40af !important;">지난 6개월간 구직 활동 증빙 필수</li>
                    <li style="color: #1e40af !important;">예금 잔고 증명 480만원 이상 필요</li>
                </ul>
                
                <div style="
                    margin-top: 1rem;
                    padding: 0.75rem;
                    background: rgba(255,255,255,0.6);
                    border-radius: 0.5rem;
                    font-size: 0.75rem;
                    color: #1e40af !important;
                ">
                    ℹ️ AI가 위 규정을 바탕으로 사용자 답변을 분석하고 있습니다.
                </div>
            </div>
        """, unsafe_allow_html=True)
