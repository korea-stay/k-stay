"""
K-Stay AI 챗봇 페이지
RAG 기반 비자 상담 챗봇
"""

import os
from dotenv import load_dotenv

# ✅ .env 파일 로드 (반드시 다른 import 전에!)
load_dotenv()

import streamlit as st
from datetime import datetime

# 상위 디렉토리 import를 위한 경로 설정
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rag_service import RAGService


def init_session_state():
    """세션 상태 초기화"""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "rag_service" not in st.session_state:
        try:
            st.session_state.rag_service = RAGService()
            st.session_state.rag_available = True
        except Exception as e:
            st.session_state.rag_available = False
            st.session_state.rag_error = str(e)


def render_chat_message(role: str, content: str, timestamp: str = None):
    """채팅 메시지 렌더링"""
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
            if timestamp:
                st.caption(timestamp)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)
            if timestamp:
                st.caption(timestamp)


def render_suggested_questions():
    """추천 질문 버튼"""
    st.markdown("#### 💡 자주 묻는 질문")
    
    questions = [
        "D-2 유학비자 종류가 뭐가 있어요?",
        "유학생 아르바이트 몇시간까지 가능해요?",
        "F-6-1이랑 F-6-2 차이가 뭐야?",
        "C-4 단기취업 비자가 뭐예요?",
        "D-10 구직비자 점수제는 어떻게 되나요?"
    ]
    
    cols = st.columns(2)
    for i, q in enumerate(questions):
        col = cols[i % 2]
        if col.button(q, key=f"suggested_{i}", use_container_width=True):
            return q
    
    return None


def main():
    """메인 페이지"""
    st.set_page_config(
        page_title="K-Stay AI 상담",
        page_icon="🤖",
        layout="wide"
    )
    
    # 세션 초기화
    init_session_state()
    
    # 헤더
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>🤖 K-Stay AI 비자 상담</h1>
        <p style="color: #666;">한국 비자 및 체류자격에 대해 무엇이든 물어보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # RAG 서비스 상태 확인
    if not st.session_state.get("rag_available", False):
        st.error(f"""
        ⚠️ AI 서비스를 시작할 수 없습니다.
        
        환경변수를 확인해주세요:
        - OPENAI_API_KEY
        - SUPABASE_URL  
        - SUPABASE_KEY
        
        오류: {st.session_state.get('rag_error', 'Unknown')}
        """)
        return
    
    # 사이드바
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        
        # 대화 초기화
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.conversation_history = []
            st.rerun()
        
        st.divider()
        
        # 안내
        st.markdown("""
        ### 📌 이용 안내
        
        이 AI는 **D-2 유학비자**, 
        **D-10 구직비자**, **F-6 결혼이민비자**,
        **C-4 단기취업비자**에 대한 
        정보를 제공합니다.
        
        **D-2 유학비자**
        - 학위과정 (전문학사~박사)
        - 시간제취업 / 체류기간
        
        **D-10 구직비자**
        - 자격요건 / 점수제
        - 제출서류 / 체류기간
        
        **F-6 결혼이민비자**
        - 국민의 배우자 (F-6-1)
        - 자녀 양육자 (F-6-2)
        - 혼인단절자 (F-6-3)
        
        **C-4 단기취업비자**
        - 계절근로 (C-4-1~4)
        - 일시흥행/모델/강연 (C-4-5)
        
        ---
        
        ⚠️ **주의사항**
        
        AI의 답변은 참고용입니다.
        정확한 정보는 **하이코리아** 또는 
        **출입국관리사무소**에서 확인하세요.
        """)
        
        st.divider()
        
        # 통계
        st.markdown("### 📊 대화 통계")
        msg_count = len(st.session_state.chat_messages)
        st.metric("메시지 수", msg_count)
    
    # 메인 영역
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 채팅 컨테이너
        chat_container = st.container()
        
        with chat_container:
            # 기존 메시지 표시
            if not st.session_state.chat_messages:
                # 웰컴 메시지
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 2rem;
                    border-radius: 1rem;
                    margin-bottom: 1rem;
                ">
                    <h3>👋 안녕하세요!</h3>
                    <p>저는 K-Stay AI 상담원입니다.</p>
                    <p>한국 비자, 특히 <strong>D-2 유학</strong>, <strong>D-10 구직</strong>, <strong>F-6 결혼이민</strong>, <strong>C-4 단기취업</strong> 비자에 대해 도움을 드릴 수 있어요.</p>
                    <p>궁금한 점이 있으시면 아래에 질문해 주세요! 😊</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                for msg in st.session_state.chat_messages:
                    render_chat_message(
                        msg["role"],
                        msg["content"],
                        msg.get("timestamp")
                    )
        
        # 입력 영역
        st.divider()
        
        # 추천 질문 (메시지가 없을 때만)
        if not st.session_state.chat_messages:
            suggested = render_suggested_questions()
            if suggested:
                # 추천 질문 클릭 시 처리
                process_user_input(suggested)
                st.rerun()
        
        # 채팅 입력
        user_input = st.chat_input("질문을 입력하세요...")
        
        if user_input:
            process_user_input(user_input)
            st.rerun()
    
    with col2:
        # 빠른 링크
        st.markdown("### 🔗 유용한 링크")
        
        st.markdown("""
        - [하이코리아](https://www.hikorea.go.kr)
        - [출입국외국인정책본부](https://www.immigration.go.kr)
        - [비자포털](https://www.visa.go.kr)
        """)
        
        st.divider()
        
        # 비자 종류 안내
        st.markdown("### 📋 비자 종류")
        
        st.markdown("**D-2 유학**")
        d2_types = {
            "D-2-1~4": "학위과정",
            "D-2-5": "연구과정",
            "D-2-6": "교환학생",
            "D-2-7": "일-학습연계"
        }
        for code, name in d2_types.items():
            st.markdown(f"- {code}: {name}")
        
        st.markdown("**D-10 구직비자**")
        d10_types = {
            "D-10-1": "일반구직",
            "D-10-2": "기술창업준비",
            "D-10-3": "첨단기술인턴"
        }
        for code, name in d10_types.items():
            st.markdown(f"- {code}: {name}")
        
        st.markdown("**F-6 결혼이민**")
        f6_types = {
            "F-6-1": "국민의 배우자",
            "F-6-2": "자녀 양육자",
            "F-6-3": "혼인단절자"
        }
        for code, name in f6_types.items():
            st.markdown(f"- {code}: {name}")
        
        st.markdown("**C-4 단기취업**")
        c4_types = {
            "C-4-1~4": "계절근로",
            "C-4-5": "흥행/모델/강연"
        }
        for code, name in c4_types.items():
            st.markdown(f"- {code}: {name}")


def process_user_input(user_input: str):
    """사용자 입력 처리"""
    timestamp = datetime.now().strftime("%H:%M")
    
    # 사용자 메시지 추가
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    # RAG 응답 생성
    try:
        with st.spinner("🤔 답변을 생성하고 있습니다..."):
            answer, updated_history = st.session_state.rag_service.chat(
                query=user_input,
                conversation_history=st.session_state.conversation_history
            )
            
            st.session_state.conversation_history = updated_history
            
            # AI 응답 추가
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
    except Exception as e:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"죄송합니다. 오류가 발생했습니다: {str(e)}",
            "timestamp": datetime.now().strftime("%H:%M")
        })


if __name__ == "__main__":
    main()