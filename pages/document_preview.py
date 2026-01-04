"""
K-Stay Document Preview & Download Page
문서 생성 완료 후 결과 페이지
with i18n support
"""

import streamlit as st
from datetime import datetime
from config.settings import SCENARIOS
from services.document_storage_service import DocumentStorageService
from utils.i18n import t


def render():
    """문서 미리보기 및 다운로드 페이지"""
    
    scenario_id = st.session_state.get('selected_scenario')
    zip_bytes = st.session_state.get('generated_zip')
    
    if not scenario_id:
        st.warning(t('document_preview.no_document'))
        if st.button(t('document_preview.back_to_dashboard')):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    user_id = st.session_state.get('user_id')
    
    # 문서 저장 (처음 한 번만)
    if zip_bytes and not st.session_state.get('document_saved'):
        save_document_to_db(user_id, scenario, zip_bytes)
    
    # 헤더
    st.markdown(f"## {t('document_preview.title')}")
    
    # subtitle with scenario name and visa type
    subtitle = t('document_preview.subtitle').replace('{scenario}', scenario.name).replace('{visa_type}', scenario.visa_type)
    st.markdown(f"**{subtitle}**")
    
    st.markdown("---")
    
    # 2단 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        # 포함된 문서 목록
        st.markdown(f"### {t('document_preview.included_docs')}")
        
        for i, doc in enumerate(scenario.required_docs, 1):
            st.markdown(f"{i}. {doc}")
        
        st.markdown("---")
        
        # 저장 상태
        storage_service = DocumentStorageService()
        if storage_service.is_connected():
            st.success(t('document_preview.cloud_saved'))
        else:
            st.info(t('document_preview.local_saved'))
    
    with col2:
        st.markdown(f"### {t('document_preview.download_title')}")
        
        if zip_bytes:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"KStay_{scenario.visa_type}_{timestamp}.zip"
            
            st.download_button(
                label=t('document_preview.download_btn'),
                data=zip_bytes,
                file_name=filename,
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
            
            st.caption(f"{t('document_preview.filename')}: {filename}")
        else:
            st.warning(t('document_preview.no_file'))
        
        st.markdown("---")
        
        # 내 문서함으로 이동
        if st.button(t('document_preview.view_my_documents'), use_container_width=True):
            st.session_state.current_page = 'my_documents'
            st.rerun()
        
        # 대시보드로 이동
        if st.button(t('document_preview.go_to_dashboard'), use_container_width=True):
            reset_form_state()
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    # 안내사항
    st.markdown("---")
    
    next_steps = f"""
**{t('document_preview.next_steps_title')}**

1. {t('document_preview.next_step_1')}
2. {t('document_preview.next_step_2')}
3. {t('document_preview.next_step_3')}
4. {t('document_preview.next_step_4')}
    """
    st.info(next_steps)
    
    st.warning(t('document_preview.warning'))


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
        st.error(f"{t('document_preview.save_error')}: {msg}")


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