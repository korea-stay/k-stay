"""
K-Stay Document Preview & Payment Page
Clean White/Blue Theme
"""

import streamlit as st
from datetime import datetime
from config.settings import SCENARIOS
from services.document_service import DocumentService


def render():
    """문서 미리보기 및 결제 페이지 렌더링"""
    
    scenario_id = st.session_state.get('selected_scenario')
    zip_bytes = st.session_state.get('generated_zip')
    
    if not scenario_id:
        st.warning("생성된 문서가 없습니다.")
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    
    st.markdown("""
        <h2 style="
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b !important;
            margin-bottom: 1.5rem;
        ">결제 및 문서 확인</h2>
    """, unsafe_allow_html=True)
    
    # 2단 레이아웃
    order_col, payment_col = st.columns(2)
    
    with order_col:
        # 주문 내역
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <h3 style="
                    font-weight: 700;
                    font-size: 1.1rem;
                    color: #1e293b !important;
                    margin: 0 0 1rem 0;
                ">주문 내역</h3>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 1rem 0;
                    border-bottom: 1px solid #f1f5f9;
                ">
                    <div>
                        <div style="font-weight: 500; color: #1e293b !important;">
                            {scenario.visa_type} 비자 서류 패키지
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b !important; margin-top: 0.25rem;">
                            통합신청서 + AI 작성 계획서
                        </div>
                    </div>
                    <div style="font-weight: 700; color: #1e293b !important;">$9.90</div>
                </div>
                
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding-top: 1rem;
                ">
                    <div style="font-weight: 700; font-size: 1.1rem; color: #1e293b !important;">Total</div>
                    <div style="font-weight: 700; font-size: 1.25rem; color: #2563eb !important;">$9.90</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 포함된 문서 목록
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 0.75rem;
                padding: 1.5rem;
            ">
                <h4 style="
                    font-weight: 600;
                    color: #1e293b !important;
                    margin: 0 0 1rem 0;
                ">📦 포함된 문서</h4>
        """, unsafe_allow_html=True)
        
        for i, doc in enumerate(scenario.required_docs[:5], 1):
            st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    padding: 0.5rem 0;
                    border-bottom: 1px solid #f8fafc;
                ">
                    <span style="
                        width: 24px;
                        height: 24px;
                        background: #dbeafe;
                        color: #2563eb !important;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 0.75rem;
                        font-weight: 600;
                    ">{i}</span>
                    <span style="font-size: 0.9rem; color: #1e293b !important;">{doc}</span>
                </div>
            """, unsafe_allow_html=True)
        
        if len(scenario.required_docs) > 5:
            st.markdown(f"""
                <p style="
                    font-size: 0.85rem;
                    color: #64748b !important;
                    margin-top: 0.5rem;
                ">외 {len(scenario.required_docs) - 5}개 문서</p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with payment_col:
        # 결제 상태에 따른 UI
        payment_complete = st.session_state.get('payment_complete', False)
        
        if not payment_complete:
            # 결제 대기 UI
            st.markdown("""
                <div style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 0.75rem;
                    padding: 2rem;
                    text-align: center;
                ">
                    <div style="
                        width: 64px;
                        height: 64px;
                        background: white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 1rem;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        font-size: 2rem;
                    ">💳</div>
                    <h3 style="
                        font-weight: 700;
                        font-size: 1.1rem;
                        color: #1e293b !important;
                        margin: 0 0 0.5rem 0;
                    ">결제 대기중</h3>
                    <p style="
                        color: #64748b !important;
                        font-size: 0.9rem;
                        margin-bottom: 1.5rem;
                    ">Stripe 안전 결제 시스템을 이용합니다.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("💳 결제하기 ($9.90)", use_container_width=True, type="primary"):
                # 결제 시뮬레이션
                with st.spinner("결제 처리 중..."):
                    import time
                    time.sleep(1.5)
                
                st.session_state.payment_complete = True
                st.session_state.is_paid = True
                st.rerun()
        
        else:
            # 결제 완료 UI
            st.markdown("""
                <div style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 0.75rem;
                    padding: 2rem;
                    text-align: center;
                ">
                    <div style="
                        width: 64px;
                        height: 64px;
                        background: #dcfce7;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 1rem;
                        font-size: 2rem;
                    ">✓</div>
                    <h3 style="
                        font-weight: 700;
                        font-size: 1.1rem;
                        color: #1e293b !important;
                        margin: 0 0 0.5rem 0;
                    ">결제 완료!</h3>
                    <p style="
                        color: #64748b !important;
                        font-size: 0.9rem;
                        margin-bottom: 1.5rem;
                    ">서류 생성이 완료되었습니다.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 다운로드 버튼
            if zip_bytes:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"KStay_{scenario.visa_type}_{timestamp}.zip"
                
                st.download_button(
                    label="📥 구직활동계획서 다운로드",
                    data=zip_bytes,
                    file_name=filename,
                    mime="application/zip",
                    use_container_width=True,
                    type="primary"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🏠 처음으로 돌아가기", use_container_width=True):
                # 상태 초기화
                st.session_state.selected_scenario = None
                st.session_state.form_step = 1
                st.session_state.form_data = {}
                st.session_state.chat_history = []
                st.session_state.generated_zip = None
                st.session_state.payment_complete = False
                st.session_state.current_page = 'dashboard'
                st.rerun()
    
    # 주의사항
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("""
        **📋 다음 단계**
        1. 다운로드한 ZIP 파일의 압축을 해제하세요.
        2. 각 문서의 내용을 꼼꼼히 확인하세요.
        3. 하이코리아(www.hikorea.go.kr)에서 온라인 예약 후 방문하세요.
        
        ⚠️ 본 문서는 AI가 생성한 초안입니다. 제출 전 반드시 확인하세요.
    """)
