"""
K-Stay AI Chat Page
RAG 기반 AI 상담사
Clean White/Blue Theme
"""

import streamlit as st
from services.ai_service import AIService, RAGService


def render():
    """AI 채팅 페이지 렌더링"""
    
    # 헤더
    st.markdown("""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
            <div style="
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
            ">🤖</div>
            <div>
                <h2 style="
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: #1e293b !important;
                    margin: 0;
                ">K-Stay AI 상담사</h2>
                <p style="
                    color: #475569 !important;
                    font-size: 0.9rem;
                    margin: 0.25rem 0 0 0;
                ">출입국 · 비자 · 체류 관련 무엇이든 물어보세요!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 초기화
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # 빠른 질문 버튼
    st.markdown("""
        <p style="
            color: #475569 !important;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
        ">💡 자주 묻는 질문</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = [
        ("D-10 비자란?", "D-10 구직비자에 대해 알려주세요."),
        ("시간제 취업", "유학생 아르바이트 허가 조건이 뭔가요?"),
        ("F-6 결혼이민", "F-6 비자 신청 조건과 필요 서류는?"),
        ("체류 연장", "체류기간 연장 신청은 어떻게 하나요?")
    ]
    
    for col, (label, question) in zip([col1, col2, col3, col4], quick_questions):
        with col:
            if st.button(label, use_container_width=True):
                add_message("user", question)
                generate_response(question)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 채팅 영역
    chat_container = st.container()
    
    with chat_container:
        # 환영 메시지 (첫 방문 시)
        if not st.session_state.ai_chat_history:
            st.markdown("""
                <div style="
                    background: #dbeafe;
                    border: 1px solid rgba(37, 99, 235, 0.2);
                    border-radius: 1rem;
                    border-top-left-radius: 0.25rem;
                    padding: 1rem;
                    margin-right: 20%;
                    margin-bottom: 1rem;
                ">
                    <p style="color: #1e40af !important; margin: 0; line-height: 1.6;">
                        안녕하세요! 저는 K-Stay AI 상담사입니다. 🤖<br><br>
                        한국 체류, 비자, 출입국 관련 질문에 답변해드립니다.<br>
                        무엇이든 편하게 물어보세요!
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # 채팅 기록 표시
        for msg in st.session_state.ai_chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        margin-bottom: 0.75rem;
                    ">
                        <div style="
                            background: #2563eb;
                            color: white !important;
                            padding: 0.75rem 1rem;
                            border-radius: 1rem;
                            border-top-right-radius: 0.25rem;
                            max-width: 70%;
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
                    ">
                        <div style="
                            background: white;
                            border: 1px solid #e2e8f0;
                            color: #1e293b !important;
                            padding: 0.75rem 1rem;
                            border-radius: 1rem;
                            border-top-left-radius: 0.25rem;
                            max-width: 70%;
                            font-size: 0.9rem;
                            line-height: 1.6;
                            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                        ">{msg['content']}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 입력 폼
    with st.form("ai_chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([6, 1])
        
        with col_input:
            user_input = st.text_input(
                "메시지 입력",
                placeholder="질문을 입력하세요...",
                label_visibility="collapsed"
            )
        
        with col_btn:
            submitted = st.form_submit_button("전송", type="primary", use_container_width=True)
        
        if submitted and user_input:
            add_message("user", user_input)
            generate_response(user_input)
    
    # 주의사항
    st.markdown("""
        <div style="
            background: #fef3c7;
            border: 1px solid #fde68a;
            border-radius: 0.5rem;
            padding: 0.75rem 1rem;
            margin-top: 1rem;
            font-size: 0.8rem;
            color: #92400e;
        ">
            ⚠️ AI 상담은 참고용입니다. 정확한 정보는 출입국관리사무소(1345)에 문의하세요.
        </div>
    """, unsafe_allow_html=True)


def add_message(role: str, content: str):
    """메시지 추가"""
    st.session_state.ai_chat_history.append({
        "role": role,
        "content": content
    })


def generate_response(user_message: str):
    """AI 응답 생성"""
    
    with st.spinner("AI가 답변을 준비 중입니다..."):
        # RAG 컨텍스트 검색
        rag_service = RAGService()
        context = rag_service.retrieve_context(user_message)
        
        # AI 응답 생성
        ai_service = AIService()
        response = ai_service.chat_response(
            user_message,
            st.session_state.ai_chat_history,
            context
        )
        
        add_message("assistant", response)
        st.rerun()
