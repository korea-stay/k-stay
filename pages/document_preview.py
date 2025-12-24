"""
K-Stay Document Preview Page
문서 미리보기 및 다운로드
"""

import streamlit as st
from datetime import datetime
from config.settings import SCENARIOS
from services.document_service import DocumentService, DocumentPreviewService


def render():
    """문서 미리보기 페이지 렌더링"""
    
    scenario_id = st.session_state.get('selected_scenario')
    zip_bytes = st.session_state.get('generated_zip')
    
    if not scenario_id or not zip_bytes:
        st.warning("생성된 문서가 없습니다.")
        if st.button("대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    
    # 성공 헤더
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(76,175,80,0.1) 0%, rgba(10,22,40,0.8) 100%);
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(76,175,80,0.3);
            text-align: center;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
            <h1 style="color: white; margin-bottom: 0.5rem;">문서 생성 완료!</h1>
            <p style="color: #a0aec0; font-size: 1.1rem;">
                {scenario.name} ({scenario.visa_type}) 패키지가 준비되었습니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 다운로드 버튼
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"KStay_{scenario.id}_{scenario.visa_type}_{timestamp}.zip"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 ZIP 패키지 다운로드",
            data=zip_bytes,
            file_name=filename,
            mime="application/zip",
            use_container_width=True,
            type="primary"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 문서 목록
    st.markdown("### 📄 포함된 문서")
    
    for i, doc_name in enumerate(scenario.required_docs, 1):
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1rem;
                background: rgba(255,255,255,0.02);
                border-radius: 8px;
                margin-bottom: 0.5rem;
            ">
                <span style="color: white;">{i}. {doc_name}</span>
                <span style="color: #4CAF50;">✓</span>
            </div>
        """, unsafe_allow_html=True)
    
    # 다음 단계
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 다음 단계")
    
    steps = [
        "다운로드한 ZIP 파일의 압축을 해제하세요.",
        "각 문서의 내용을 꼼꼼히 확인하세요.",
        "필요한 추가 서류(증명서 등)를 준비하세요.",
        "하이코리아(www.hikorea.go.kr)에서 온라인 예약하세요.",
        "출입국관리사무소를 방문하여 서류를 제출하세요."
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                padding: 0.8rem;
                margin-bottom: 0.5rem;
            ">
                <span style="
                    background: rgba(201,162,39,0.2);
                    color: #C9A227;
                    min-width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.85rem;
                ">{i}</span>
                <span style="color: #a0aec0;">{step}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # 경고
    st.markdown("<br>", unsafe_allow_html=True)
    st.warning("""
        ⚠️ **주의사항**
        - 본 문서는 AI가 생성한 초안입니다.
        - 제출 전 반드시 내용을 확인하고 필요시 수정하세요.
        - 최신 요건은 하이코리아에서 확인하세요.
        - 문의: 출입국외국인청 1345
    """)
    
    # 네비게이션
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 대시보드로 돌아가기", use_container_width=True):
            # 상태 초기화
            st.session_state.selected_scenario = None
            st.session_state.form_step = 1
            st.session_state.form_data = {}
            st.session_state.narrative_data = {}
            st.session_state.generated_zip = None
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button("💬 AI 상담사에게 질문하기", use_container_width=True):
            st.session_state.current_page = 'ai_chat'
            st.rerun()
