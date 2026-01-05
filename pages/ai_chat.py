"""
K-Stay AI Chat Page
RAG 기반 AI 상담사
Modern Chat UI Design with Real-time Response UX
"""

import streamlit as st
from services.rag_service import RAGService
from utils.i18n import t, get_current_language
from utils.scroll import scroll_to_top


def render():
    """AI 채팅 페이지 렌더링"""
    
    # 페이지 진입 시 스크롤 맨 위로
    scroll_to_top()
    
    # 커스텀 CSS (타이핑 애니메이션 포함)
    st.markdown("""
        <style>
        /* 전체 채팅 컨테이너 */
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* ★★★ 사용자 메시지 텍스트 색상 강제 (최우선) ★★★ */
        .user-message-bubble,
        .user-message-bubble * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        .user-message-bubble p {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            margin: 0 !important;
        }
        
        /* 빠른 질문 버튼 스타일 */
        .stButton > button {
            border-radius: 20px !important;
            font-size: 0.85rem !important;
            padding: 0.5rem 1rem !important;
            border: 1px solid #e2e8f0 !important;
            background: white !important;
            color: #475569 !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: #f1f5f9 !important;
            border-color: #94a3b8 !important;
        }
        
        /* 입력창 스타일 */
        .stTextInput > div > div > input {
            border-radius: 24px !important;
            padding: 0.75rem 1.25rem !important;
            border: 2px solid #e2e8f0 !important;
            font-size: 0.95rem !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            outline: none !important;
        }
        
        /* Streamlit 기본 빨간 테두리 제거 */
        .stTextInput > div { border: none !important; }
        .stTextInput > div > div { border: none !important; box-shadow: none !important; }
        div[data-baseweb="input"] { border-color: #e2e8f0 !important; }
        div[data-baseweb="input"]:focus-within {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }
        
        /* 전송 버튼 */
        .stFormSubmitButton > button {
            border-radius: 24px !important;
            background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
        }
        .stFormSubmitButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
            transform: translateY(-1px);
        }
        
        /* ★★★ 타이핑 애니메이션 ★★★ */
        @keyframes typingBounce {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-4px); opacity: 1; }
        }
        .typing-indicator {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 0;
        }
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #6366f1;
        }
        .typing-dot:nth-child(1) { animation: typingBounce 1.4s ease-in-out infinite 0s; }
        .typing-dot:nth-child(2) { animation: typingBounce 1.4s ease-in-out infinite 0.2s; }
        .typing-dot:nth-child(3) { animation: typingBounce 1.4s ease-in-out infinite 0.4s; }
        </style>
    """, unsafe_allow_html=True)
    
    # RAG 서비스 초기화
    if 'rag_service' not in st.session_state:
        try:
            st.session_state.rag_service = RAGService()
        except Exception as e:
            st.error(f"RAG 서비스 초기화 실패: {e}")
            st.session_state.rag_service = None
    
    # 헤더
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="
                width: 56px;
                height: 56px;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            ">🤖</div>
            <div>
                <h2 style="font-size: 1.35rem; font-weight: 700; color: #1e293b !important; margin: 0; letter-spacing: -0.02em;">{t('ai_chat.title')}</h2>
                <p style="color: #64748b !important; font-size: 0.9rem; margin: 0.35rem 0 0 0;">{t('ai_chat.subtitle')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 초기화
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'pending_response' not in st.session_state:
        st.session_state.pending_response = None
    
    # K-ETA 프리셋 질문 처리 (대시보드에서 넘어온 경우)
    if 'ai_chat_preset' in st.session_state and st.session_state.ai_chat_preset:
        preset_question = st.session_state.ai_chat_preset
        st.session_state.ai_chat_preset = None
        # 사용자 메시지 즉시 추가
        st.session_state.ai_chat_history.append({"role": "user", "content": preset_question})
        st.session_state.pending_response = preset_question
        st.rerun()
    
    # 빠른 질문 버튼
    st.markdown(f"""
        <p style="color: #64748b !important; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">💡 {t('ai_chat.faq')}</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    quick_questions = [
        (f"🎓 {t('ai_chat.quick_d2')}", t('ai_chat.quick_d2_q')),
        (f"📚 {t('ai_chat.quick_d4')}", t('ai_chat.quick_d4_q')),
        (f"💍 {t('ai_chat.quick_f6')}", t('ai_chat.quick_f6_q')),
        (f"🔍 {t('ai_chat.quick_d10')}", t('ai_chat.quick_d10_q')),
        (f"🛫 {t('ai_chat.quick_keta')}", t('ai_chat.quick_keta_q'))
    ]
    
    for col, (label, question) in zip([col1, col2, col3, col4, col5], quick_questions):
        with col:
            if st.button(label, use_container_width=True):
                # 사용자 메시지 즉시 추가 후 pending 상태로
                st.session_state.ai_chat_history.append({"role": "user", "content": question})
                st.session_state.pending_response = question
                st.rerun()
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # 채팅 영역
    chat_area = st.container()
    
    with chat_area:
        # 환영 메시지 (채팅 기록이 없을 때만)
        if not st.session_state.ai_chat_history:
            render_welcome_message()
        
        # ★★★ 채팅 기록 표시 (사용자 메시지 즉시 표시) ★★★
        for idx, msg in enumerate(st.session_state.ai_chat_history):
            if msg['role'] == 'user':
                render_user_message(msg['content'])
            else:
                render_ai_message(msg['content'], msg.get('scenario'), idx)
        
        # ★★★ 응답 생성 중 표시 ★★★
        if st.session_state.pending_response:
            render_typing_indicator()
    
    # 입력 영역
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        
        with col_input:
            user_input = st.text_input(
                "message",
                placeholder=t('ai_chat.input_placeholder'),
                key="chat_input",
                label_visibility="collapsed"
            )
        
        with col_btn:
            submitted = st.form_submit_button(
                t('ai_chat.send'),
                use_container_width=True,
                type="primary"
            )
        
        if submitted and user_input:
            # ★★★ 사용자 메시지 즉시 추가 (화면에 바로 표시됨) ★★★
            st.session_state.ai_chat_history.append({"role": "user", "content": user_input})
            st.session_state.pending_response = user_input
            st.rerun()
    
    # ★★★ 응답 생성 로직 (pending 상태일 때 실행) ★★★
    if st.session_state.pending_response:
        generate_response_async(st.session_state.pending_response)
    
    # 채팅 초기화 버튼
    if st.session_state.ai_chat_history:
        st.markdown("<div style='display: flex; justify-content: center; margin-top: 1rem;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄", help="Clear chat", use_container_width=True):
                st.session_state.ai_chat_history = []
                st.session_state.conversation_history = []
                st.session_state.pending_response = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 사이드바
    render_sidebar()


def render_welcome_message():
    """환영 메시지 렌더링"""
    st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 1rem;">
            <div style="
                width: 36px; height: 36px;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 1rem; flex-shrink: 0;
            ">🤖</div>
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0 16px 16px 16px;
                padding: 1rem 1.25rem;
                max-width: 85%;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            ">
                <p style="color: #334155 !important; margin: 0; line-height: 1.7; font-size: 0.95rem;">
                    {t('ai_chat.welcome')} 👋<br><br>
                    {t('ai_chat.welcome_intro')}<br>
                    {t('ai_chat.welcome_ask')}
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #f1f5f9;">
                    <span style="background: #dbeafe; color: #1e40af; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">🎓 {t('ai_chat.visa_d2')}</span>
                    <span style="background: #ede9fe; color: #5b21b6; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">📚 {t('ai_chat.visa_d4')}</span>
                    <span style="background: #fce7f3; color: #9d174d; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">💍 {t('ai_chat.visa_f6')}</span>
                    <span style="background: #d1fae5; color: #065f46; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">🔍 {t('ai_chat.visa_d10')}</span>
                    <span style="background: #fef3c7; color: #92400e; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 500;">🛫 {t('ai_chat.visa_keta')}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_user_message(content: str):
    """사용자 메시지 렌더링 (오른쪽, 파란색 배경 + 흰색 텍스트)"""
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
            <div class="user-message-bubble" style="
                background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
                padding: 0.875rem 1.25rem;
                border-radius: 20px 20px 4px 20px;
                max-width: 75%;
                font-size: 0.95rem;
                line-height: 1.6;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
            ">
                <p style="color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; margin: 0 !important; font-weight: 400;">{content}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_ai_message(content: str, scenario: dict = None, idx: int = 0):
    """AI 메시지 렌더링 (왼쪽, 흰색)"""
    content_html = content.replace('\n', '<br>')
    
    st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 0.5rem;">
            <div style="
                width: 36px; height: 36px;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 1rem; flex-shrink: 0;
            ">🤖</div>
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                color: #334155 !important;
                padding: 1rem 1.25rem;
                border-radius: 0 20px 20px 20px;
                max-width: 85%;
                font-size: 0.95rem;
                line-height: 1.7;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">{content_html}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 시나리오 버튼 표시
    if scenario:
        current_lang = get_current_language()
        scenario_name = scenario.get('name_en' if current_lang == 'en' else 'name_ko', '')
        scenario_icon = scenario.get('icon', '📄')
        scenario_visa = scenario.get('visa', '')
        
        btn_text = f"{scenario_icon} Start {scenario_name} ({scenario_visa})" if current_lang == 'en' else f"{scenario_icon} {scenario_name} 시작하기 ({scenario_visa})"
        
        col_spacer, col_btn, col_spacer2 = st.columns([0.5, 3, 4])
        with col_btn:
            if st.button(btn_text, key=f"scenario_btn_{idx}", type="primary"):
                st.session_state.selected_scenario = scenario.get('id')
                st.session_state.current_page = 'scenario_form'
                st.session_state.form_step = 1
                st.rerun()
        
        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)


def render_typing_indicator():
    """★★★ 타이핑 중 표시 (생성 중 애니메이션) ★★★"""
    st.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 1rem;">
            <div style="
                width: 36px; height: 36px;
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 1rem; flex-shrink: 0;
            ">🤖</div>
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                color: #64748b !important;
                padding: 1rem 1.5rem;
                border-radius: 0 20px 20px 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <span style="font-size: 0.9rem; color: #64748b;">{t('ai_chat.generating')}</span>
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def generate_response_async(user_message: str):
    """RAG 기반 AI 응답 생성 (비동기 스타일)"""
    
    try:
        rag_service = st.session_state.rag_service
        
        if rag_service:
            current_lang = get_current_language()
            
            response, updated_history, related_scenario = rag_service.chat(
                query=user_message,
                conversation_history=st.session_state.conversation_history,
                language=current_lang
            )
            st.session_state.conversation_history = updated_history
            
            # 응답 메시지 추가
            st.session_state.ai_chat_history.append({
                "role": "assistant",
                "content": response,
                "scenario": related_scenario
            })
        else:
            st.session_state.ai_chat_history.append({
                "role": "assistant",
                "content": t('ai_chat.error_service')
            })
        
    except Exception as e:
        st.session_state.ai_chat_history.append({
            "role": "assistant",
            "content": f"{t('ai_chat.error_response')}: {str(e)}"
        })
    
    # pending 상태 해제 및 화면 갱신
    st.session_state.pending_response = None
    st.rerun()


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                border-radius: 12px;
                padding: 1.25rem;
                margin-bottom: 1rem;
            ">
                <h3 style="color: #0369a1 !important; font-size: 1rem; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 8px;">📋 {t('sidebar.supported_visas')}</h3>
        """, unsafe_allow_html=True)
        
        visa_info = [
            ("🎓", t("visa_info.d2_name"), "#3b82f6", t("visa_info.d2_types")),
            ("📚", t("visa_info.d4_name"), "#6366f1", t("visa_info.d4_types")),
            ("📰", t("visa_info.d5_name"), "#8b5cf6", t("visa_info.d5_types")),
            ("⛪", t("visa_info.d6_name"), "#a855f7", t("visa_info.d6_types")),
            ("🔍", t("visa_info.d10_name"), "#10b981", t("visa_info.d10_types")),
            ("💍", t("visa_info.f6_name"), "#ec4899", t("visa_info.f6_types")),
            ("✈️", t("visa_info.c4_name"), "#f59e0b", t("visa_info.c4_types")),
        ]
        
        for icon, title, color, items in visa_info:
            st.markdown(f"""
                <div style="margin-bottom: 0.75rem;">
                    <p style="color: {color} !important; font-weight: 600; font-size: 0.9rem; margin: 0 0 4px 0;">{icon} {title}</p>
                    <p style="color: #64748b !important; font-size: 0.8rem; margin: 0; padding-left: 1.25rem; line-height: 1.6;">{items}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)