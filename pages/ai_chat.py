"""
K-Stay AI Chat Page
RAG 기반 AI 상담사
Modern Chat UI Design with i18n
"""

import streamlit as st
from services.rag_service import RAGService
from utils.i18n import t, get_current_language


def render():
    """AI 채팅 페이지 렌더링"""
    
    # 커스텀 CSS
    st.markdown("""
        <style>
        /* 전체 채팅 컨테이너 */
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
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
        
        /* 입력창 스타일 - 빨간 테두리 제거 */
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
        
        /* Streamlit 기본 빨간 테두리 완전 제거 */
        .stTextInput > div {
            border: none !important;
        }
        .stTextInput > div > div {
            border: none !important;
            box-shadow: none !important;
        }
        .stTextInput input:focus {
            border-color: #3b82f6 !important;
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
        }
        div[data-baseweb="input"] {
            border-color: #e2e8f0 !important;
        }
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
                <h2 style="
                    font-size: 1.35rem;
                    font-weight: 700;
                    color: #1e293b !important;
                    margin: 0;
                    letter-spacing: -0.02em;
                ">{t('ai_chat.title')}</h2>
                <p style="
                    color: #64748b !important;
                    font-size: 0.9rem;
                    margin: 0.35rem 0 0 0;
                ">{t('ai_chat.subtitle')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 초기화
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # 빠른 질문 버튼
    st.markdown(f"""
        <p style="
            color: #64748b !important;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">💡 {t('ai_chat.faq')}</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    quick_questions = [
        (f"🎓 {t('ai_chat.quick_d2')}", t('ai_chat.quick_d2_q')),
        (f"📚 {t('ai_chat.quick_d4')}", t('ai_chat.quick_d4_q')),
        (f"💍 {t('ai_chat.quick_f6')}", t('ai_chat.quick_f6_q')),
        (f"🔍 {t('ai_chat.quick_d10')}", t('ai_chat.quick_d10_q'))
    ]
    
    for col, (label, question) in zip([col1, col2, col3, col4], quick_questions):
        with col:
            if st.button(label, use_container_width=True):
                add_message("user", question)
                generate_response(question)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # 채팅 영역
    chat_area = st.container()
    
    with chat_area:
        # 환영 메시지
        if not st.session_state.ai_chat_history:
            st.markdown(f"""
                <div style="
                    display: flex;
                    gap: 12px;
                    margin-bottom: 1rem;
                ">
                    <div style="
                        width: 36px;
                        height: 36px;
                        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1rem;
                        flex-shrink: 0;
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
                        <div style="
                            display: flex;
                            flex-wrap: wrap;
                            gap: 6px;
                            margin-top: 12px;
                        ">
                            <span style="
                                background: #dbeafe;
                                color: #1e40af;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_d2')}</span>
                            <span style="
                                background: #e0e7ff;
                                color: #3730a3;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_d4')}</span>
                            <span style="
                                background: #f3e8ff;
                                color: #6b21a8;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_d5')}</span>
                            <span style="
                                background: #fae8ff;
                                color: #86198f;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_d6')}</span>
                            <span style="
                                background: #dcfce7;
                                color: #166534;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_d10')}</span>
                            <span style="
                                background: #fce7f3;
                                color: #9d174d;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_f6')}</span>
                            <span style="
                                background: #fef3c7;
                                color: #92400e;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">{t('ai_chat.visa_c4')}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 채팅 기록 표시
        for msg in st.session_state.ai_chat_history:
            if msg['role'] == 'user':
                # 사용자 메시지 (연한 파랑, 오른쪽)
                st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        margin-bottom: 1rem;
                    ">
                        <div style="
                            background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
                            color: #1e40af !important;
                            padding: 0.875rem 1.25rem;
                            border-radius: 20px 20px 4px 20px;
                            max-width: 75%;
                            font-size: 0.95rem;
                            line-height: 1.6;
                            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
                        ">{msg['content']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # AI 메시지 (흰색, 왼쪽)
                # content 내 줄바꿈 처리
                content = msg['content'].replace('\n', '<br>')
                st.markdown(f"""
                    <div style="
                        display: flex;
                        gap: 12px;
                        margin-bottom: 1rem;
                    ">
                        <div style="
                            width: 36px;
                            height: 36px;
                            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1rem;
                            flex-shrink: 0;
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
                        ">{content}</div>
                    </div>
                """, unsafe_allow_html=True)
    
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
            add_message("user", user_input)
            generate_response(user_input)
    
    # 채팅 초기화 버튼
    st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        ">
    """, unsafe_allow_html=True)
    
    if st.session_state.ai_chat_history:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄", help="Clear chat", use_container_width=True):
                st.session_state.ai_chat_history = []
                st.session_state.conversation_history = []
                st.rerun()
    
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                border-radius: 12px;
                padding: 1.25rem;
                margin-bottom: 1rem;
            ">
                <h3 style="
                    color: #0369a1 !important;
                    font-size: 1rem;
                    margin: 0 0 1rem 0;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                ">📋 {t('sidebar.supported_visas')}</h3>
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
                    <p style="
                        color: {color} !important;
                        font-weight: 600;
                        font-size: 0.9rem;
                        margin: 0 0 4px 0;
                    ">{icon} {title}</p>
                    <p style="
                        color: #64748b !important;
                        font-size: 0.8rem;
                        margin: 0;
                        padding-left: 1.25rem;
                        line-height: 1.6;
                    ">{items}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def add_message(role: str, content: str):
    """메시지 추가"""
    st.session_state.ai_chat_history.append({
        "role": role,
        "content": content
    })


def generate_response(user_message: str):
    """RAG 기반 AI 응답 생성"""
    
    with st.spinner(f"💭 {t('ai_chat.generating')}"):
        try:
            rag_service = st.session_state.rag_service
            
            if rag_service:
                # 현재 언어 확인하여 영어면 영어로 응답하도록 설정
                current_lang = get_current_language()
                
                response, updated_history = rag_service.chat(
                    query=user_message,
                    conversation_history=st.session_state.conversation_history,
                    language=current_lang  # 언어 파라미터 전달
                )
                st.session_state.conversation_history = updated_history
                add_message("assistant", response)
            else:
                add_message("assistant", t('ai_chat.error_service'))
            
        except Exception as e:
            add_message("assistant", f"{t('ai_chat.error_response')}: {str(e)}")
        
        st.rerun()
