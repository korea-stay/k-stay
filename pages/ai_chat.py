"""
K-Stay AI Chat Page
RAG 기반 AI 상담사
"""

import streamlit as st
from services.ai_service import AIService, RAGService


def render():
    """AI 채팅 페이지 렌더링"""
    
    # 헤더
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(10,22,40,0.8) 100%);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(102,126,234,0.2);
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.8rem;
                ">🤖</div>
                <div>
                    <h1 style="
                        color: white;
                        font-family: 'Noto Sans KR', sans-serif;
                        margin: 0;
                        font-size: 1.8rem;
                    ">K-Stay AI 상담사</h1>
                    <p style="
                        color: #a0aec0;
                        margin: 0.3rem 0 0 0;
                    ">출입국 · 비자 · 체류 관련 무엇이든 물어보세요!</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 채팅 기록 초기화
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 빠른 질문 버튼
    render_quick_questions()
    
    # 채팅 영역
    render_chat_area()
    
    # 입력 영역
    render_input_area()


def render_quick_questions():
    """빠른 질문 버튼"""
    
    quick_questions = [
        ("D-10 비자란?", "D-10 구직비자에 대해 알려주세요."),
        ("시간제 취업", "유학생 아르바이트 허가 조건이 뭔가요?"),
        ("F-6 결혼이민", "F-6 비자 신청 조건과 필요 서류는?"),
        ("체류 연장", "체류기간 연장 신청은 어떻게 하나요?")
    ]
    
    st.markdown("#### 💡 자주 묻는 질문")
    
    cols = st.columns(4)
    
    for i, (label, question) in enumerate(quick_questions):
        with cols[i]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                # 질문 추가 및 응답 생성
                add_message("user", question)
                generate_response(question)


def render_chat_area():
    """채팅 메시지 영역"""
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 채팅 컨테이너
    chat_container = st.container()
    
    with chat_container:
        # 환영 메시지 (첫 방문 시)
        if not st.session_state.chat_history:
            st.markdown("""
                <div style="
                    background: rgba(102,126,234,0.1);
                    border: 1px solid rgba(102,126,234,0.2);
                    border-radius: 16px;
                    padding: 1.5rem;
                    margin: 1rem 2rem 1rem 0;
                ">
                    <p style="color: white; margin: 0;">
                        안녕하세요! 저는 K-Stay AI 상담사입니다. 🤖<br><br>
                        한국 체류, 비자, 출입국 관련 질문에 답변해드립니다.<br>
                        무엇이든 편하게 물어보세요!
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # 채팅 기록 표시
        for msg in st.session_state.chat_history:
            render_message(msg['role'], msg['content'])


def render_message(role: str, content: str):
    """개별 메시지 렌더링"""
    
    if role == "user":
        st.markdown(f"""
            <div style="
                background: rgba(201,162,39,0.1);
                border: 1px solid rgba(201,162,39,0.3);
                border-radius: 16px;
                padding: 1rem 1.5rem;
                margin: 1rem 0 1rem 3rem;
            ">
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 0.8rem;
                ">
                    <span style="font-size: 1.2rem;">👤</span>
                    <p style="color: white; margin: 0; line-height: 1.6;">{content}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="
                background: rgba(102,126,234,0.1);
                border: 1px solid rgba(102,126,234,0.2);
                border-radius: 16px;
                padding: 1rem 1.5rem;
                margin: 1rem 3rem 1rem 0;
            ">
                <div style="
                    display: flex;
                    align-items: flex-start;
                    gap: 0.8rem;
                ">
                    <span style="font-size: 1.2rem;">🤖</span>
                    <div style="color: white; margin: 0; line-height: 1.6;">{content}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_input_area():
    """입력 영역"""
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 입력 폼
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input(
                "메시지 입력",
                placeholder="질문을 입력하세요...",
                label_visibility="collapsed",
                key="chat_input"
            )
        
        with col2:
            submitted = st.form_submit_button("전송", type="primary", use_container_width=True)
        
        if submitted and user_input:
            add_message("user", user_input)
            generate_response(user_input)


def add_message(role: str, content: str):
    """메시지 추가"""
    st.session_state.chat_history.append({
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
            st.session_state.chat_history,
            context
        )
        
        add_message("assistant", response)
        st.rerun()


def render_info_panel():
    """정보 패널 (사이드바용)"""
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(201,162,39,0.15);
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <h4 style="color: #C9A227; margin-bottom: 1rem;">📚 참고 자료</h4>
            <ul style="color: #a0aec0; font-size: 0.9rem; padding-left: 1.2rem;">
                <li>하이코리아 공식 가이드</li>
                <li>출입국관리법</li>
                <li>비자 종류별 요건</li>
                <li>최근 정책 변경사항</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: rgba(255,107,107,0.1);
            border: 1px solid rgba(255,107,107,0.2);
            border-radius: 12px;
            padding: 1rem;
        ">
            <p style="color: #FF6B6B; font-size: 0.85rem; margin: 0;">
                ⚠️ AI 상담은 참고용입니다.<br>
                정확한 정보는 출입국관리사무소에 문의하세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
