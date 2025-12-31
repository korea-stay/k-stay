"""
K-Stay AI Chat Page
RAG 기반 AI 상담사
Modern Chat UI Design
"""

import streamlit as st
from services.rag_service import RAGService


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
    st.markdown("""
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
                ">K-Stay AI 상담사</h2>
                <p style="
                    color: #64748b !important;
                    font-size: 0.9rem;
                    margin: 0.35rem 0 0 0;
                ">D-2 유학 · D-4 연수 · D-5 취재 · D-6 종교 · D-10 구직 · F-6 결혼 · C-4 단기취업</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 초기화
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # 빠른 질문 버튼
    st.markdown("""
        <p style="
            color: #64748b !important;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        ">💡 자주 묻는 질문</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    quick_questions = [
        ("🎓 D-2 유학", "D-2 유학비자 종류가 뭐가 있어요?"),
        ("📚 D-4 연수", "D-4 일반연수 비자는 뭐예요?"),
        ("💍 F-6 결혼", "F-6 결혼이민 비자 조건이 뭐예요?"),
        ("🔍 D-10 구직", "D-10 구직비자 점수제는 어떻게 되나요?")
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
            st.markdown("""
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
                            안녕하세요! 👋<br><br>
                            저는 <strong style="color: #3b82f6;">K-Stay AI 상담사</strong>입니다.<br>
                            비자 관련 궁금한 점을 물어보세요!
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
                            ">D-2 유학</span>
                            <span style="
                                background: #e0e7ff;
                                color: #3730a3;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">D-4 연수</span>
                            <span style="
                                background: #f3e8ff;
                                color: #6b21a8;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">D-5 취재</span>
                            <span style="
                                background: #fae8ff;
                                color: #86198f;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">D-6 종교</span>
                            <span style="
                                background: #dcfce7;
                                color: #166534;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">D-10 구직</span>
                            <span style="
                                background: #fce7f3;
                                color: #9d174d;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">F-6 결혼이민</span>
                            <span style="
                                background: #fef3c7;
                                color: #92400e;
                                padding: 4px 10px;
                                border-radius: 12px;
                                font-size: 0.75rem;
                                font-weight: 500;
                            ">C-4 단기취업</span>
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
        
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # 입력 폼
    with st.form("ai_chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        
        with col_input:
            user_input = st.text_input(
                "메시지 입력",
                placeholder="궁금한 점을 입력하세요...",
                label_visibility="collapsed"
            )
        
        with col_btn:
            submitted = st.form_submit_button("전송 ➤", type="primary", use_container_width=True)
        
        if submitted and user_input:
            add_message("user", user_input)
            generate_response(user_input)
    
    # 하단 버튼들
    col_clear, col_info, _ = st.columns([1, 1, 4])
    with col_clear:
        if st.button("🗑️ 초기화", use_container_width=True):
            st.session_state.ai_chat_history = []
            st.session_state.conversation_history = []
            st.rerun()
    
    # 안내 문구
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
            border: 1px solid #fde68a;
            border-radius: 12px;
            padding: 0.875rem 1.25rem;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span style="font-size: 1.25rem;">⚠️</span>
            <span style="color: #92400e; font-size: 0.85rem; line-height: 1.5;">
                AI 상담은 <strong>참고용</strong>입니다. 정확한 정보는 
                <strong>출입국관리사무소(☎ 1345)</strong> 또는 
                <strong>하이코리아(hikorea.go.kr)</strong>에서 확인하세요.
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.markdown("""
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
                ">📋 지원 비자</h3>
        """, unsafe_allow_html=True)
        
        visa_info = [
            ("🎓", "D-2 유학", "#3b82f6", ["D-2-1~4 학위과정", "D-2-5 연구", "D-2-6 교환학생"]),
            ("📚", "D-4 연수", "#6366f1", ["D-4-1 한국어연수", "D-4-6 사설교육기관"]),
            ("📰", "D-5 취재", "#8b5cf6", ["외신기자", "보도활동"]),
            ("⛪", "D-6 종교", "#a855f7", ["선교활동", "사회복지"]),
            ("🔍", "D-10 구직", "#10b981", ["D-10-1 일반구직", "D-10-2 기술창업"]),
            ("💍", "F-6 결혼이민", "#ec4899", ["F-6-1 배우자", "F-6-2 자녀양육", "F-6-3 혼인단절"]),
            ("✈️", "C-4 단기취업", "#f59e0b", ["C-4-1~4 계절근로", "C-4-5 흥행/모델"]),
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
                    ">{' · '.join(items)}</p>
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
    
    with st.spinner("💭 답변 생성 중..."):
        try:
            rag_service = st.session_state.rag_service
            
            if rag_service:
                response, updated_history = rag_service.chat(
                    query=user_message,
                    conversation_history=st.session_state.conversation_history
                )
                st.session_state.conversation_history = updated_history
                add_message("assistant", response)
            else:
                add_message("assistant", "죄송합니다. 현재 AI 서비스에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.")
            
        except Exception as e:
            add_message("assistant", f"응답 생성 중 오류가 발생했습니다: {str(e)}")
        
        st.rerun()