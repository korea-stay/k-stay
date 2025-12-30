"""
K-Stay Document Preview & Download Page
문서 생성 완료 후 결과 페이지
"""

import streamlit as st
from datetime import datetime
from config.settings import SCENARIOS
from services.document_storage_service import DocumentStorageService


def render():
    """문서 미리보기 및 다운로드 페이지"""
    
    scenario_id = st.session_state.get('selected_scenario')
    zip_bytes = st.session_state.get('generated_zip')
    
    if not scenario_id:
        st.warning("생성된 문서가 없습니다.")
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    user_id = st.session_state.get('user_id')
    
    # 문서 저장 (처음 한 번만)
    if zip_bytes and not st.session_state.get('document_saved'):
        save_document_to_db(user_id, scenario, zip_bytes)
    
    # 헤더
    st.markdown("## 🎉 문서 생성 완료!")
    st.markdown(f"**{scenario.name} ({scenario.visa_type})** 서류 패키지가 준비되었습니다.")
    
    st.markdown("---")
    
    # 2단 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        # 포함된 문서 목록
        st.markdown("### 📦 포함된 문서")
        
        for i, doc in enumerate(scenario.required_docs, 1):
            st.markdown(f"{i}. {doc}")
        
        st.markdown("---")
        
        # 저장 상태
        storage_service = DocumentStorageService()
        if storage_service.is_connected():
            st.success("✅ 문서가 클라우드에 저장되었습니다.")
        else:
            st.info("💾 문서가 로컬에 저장되었습니다. (테스트 모드)")
    
    with col2:
        st.markdown("### 📥 다운로드")
        
        if zip_bytes:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"KStay_{scenario.visa_type}_{timestamp}.zip"
            
            st.download_button(
                label="📥 서류 패키지 다운로드 (ZIP)",
                data=zip_bytes,
                file_name=filename,
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
            
            st.caption(f"파일명: {filename}")
        else:
            st.warning("다운로드 파일이 없습니다.")
        
        st.markdown("---")
        
        # 내 문서함으로 이동
        if st.button("📁 내 문서함에서 보기", use_container_width=True):
            st.session_state.current_page = 'my_documents'
            st.rerun()
        
        # 대시보드로 이동
        if st.button("🏠 대시보드로 돌아가기", use_container_width=True):
            reset_form_state()
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    # 안내사항
    st.markdown("---")
    
    st.info("""
**📋 다음 단계**

1. **다운로드**: 위 버튼을 클릭하여 ZIP 파일을 다운로드하세요.
2. **압축 해제**: 다운로드한 파일의 압축을 해제하세요.
3. **내용 확인**: 각 문서의 내용을 꼼꼼히 확인하고 수정하세요.
4. **출입국관리사무소 방문**: 하이코리아(www.hikorea.go.kr)에서 방문 예약 후 서류를 제출하세요.
    """)
    
    st.warning("⚠️ **주의**: 본 문서는 AI가 생성한 초안입니다. 제출 전 반드시 내용을 확인하시고, 필요시 전문가의 검토를 받으세요.")


def save_document_to_db(user_id: str, scenario, zip_bytes: bytes):
    """문서를 DB에 저장"""
    
    if not user_id or not zip_bytes:
        return
    
    storage_service = DocumentStorageService()
    
    success, msg, doc_id = storage_service.save_document(
        user_id=user_id,
        scenario_id=scenario.id,
        scenario_name=scenario.name,
        visa_type=scenario.visa_type,
        zip_bytes=zip_bytes,
        document_list=scenario.required_docs
    )
    
    if success:
        st.session_state.document_saved = True
        st.session_state.saved_document_id = doc_id
    else:
        st.error(f"문서 저장 실패: {msg}")


def reset_form_state():
    """폼 상태 초기화"""
    st.session_state.selected_scenario = None
    st.session_state.form_step = 1
    st.session_state.form_data = {}
    st.session_state.narrative_data = {}
    st.session_state.chat_history = []
    st.session_state.generated_zip = None
    st.session_state.document_saved = False
    st.session_state.saved_document_id = None
