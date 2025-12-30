"""
K-Stay My Documents Page
내 문서함 - 생성된 문서 목록 조회 및 다운로드
"""

import streamlit as st
from datetime import datetime
from services.document_storage_service import DocumentStorageService


def render():
    """내 문서함 페이지 렌더링"""
    
    user_id = st.session_state.get('user_id')
    
    if not user_id:
        st.warning("로그인이 필요합니다.")
        return
    
    st.markdown("## 📁 내 문서함")
    st.markdown("생성하신 비자 서류 패키지를 확인하고 다운로드할 수 있습니다.")
    
    st.markdown("---")
    
    storage_service = DocumentStorageService()
    
    documents = storage_service.get_user_documents(user_id)
    
    if not documents:
        st.info("📭 아직 생성된 문서가 없습니다. 시나리오를 선택하고 서류를 생성해보세요!")
        
        if st.button("🚀 시나리오 선택하러 가기", type="primary"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    st.markdown(f"### 총 {len(documents)}개의 문서 패키지")
    st.markdown("")
    
    # 각 문서에 대해 파일 데이터 미리 로드 (다운로드 버튼용)
    for doc in documents:
        doc_id = doc.get('id', '')
        # 파일 데이터 캐싱
        cache_key = f'doc_file_{doc_id}'
        if cache_key not in st.session_state:
            file_data = storage_service.get_document_file(user_id, doc_id)
            if file_data:
                st.session_state[cache_key] = file_data
        
        render_document_card(doc, storage_service, user_id)


def render_document_card(doc: dict, storage_service: DocumentStorageService, user_id: str):
    """개별 문서 카드 렌더링"""
    
    doc_id = doc.get('id', '')
    scenario_name = doc.get('scenario_name', '알 수 없음')
    visa_type = doc.get('visa_type', '-')
    document_list = doc.get('document_list', [])
    file_size = doc.get('file_size', 0)
    created_at = doc.get('created_at', '')
    
    # document_list 처리
    if isinstance(document_list, str):
        try:
            import json
            document_list = json.loads(document_list)
        except:
            document_list = []
    
    # 날짜 포맷팅
    try:
        if created_at:
            if 'T' in str(created_at):
                dt = datetime.fromisoformat(str(created_at).replace('Z', '+00:00').split('+')[0])
            else:
                dt = datetime.strptime(str(created_at)[:19], '%Y-%m-%d %H:%M:%S')
            date_str = dt.strftime('%Y년 %m월 %d일 %H:%M')
        else:
            date_str = '-'
    except:
        date_str = str(created_at)[:16] if created_at else '-'
    
    # 파일 크기 포맷팅
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.1f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    # 문서 목록 HTML 생성 (세로 나열)
    docs_html = ""
    for i, doc_name in enumerate(document_list, 1):
        docs_html += f'<div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.25rem;">{i}. {doc_name}</div>'
    
    # 카드 HTML
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        ">
            <div style="display: flex; justify-content: space-between; gap: 2rem;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem;">📄</span>
                        <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">{scenario_name}</h3>
                    </div>
                    <div style="
                        display: inline-block;
                        background: #dbeafe;
                        color: #1d4ed8;
                        padding: 0.25rem 0.75rem;
                        border-radius: 1rem;
                        font-size: 0.85rem;
                        font-weight: 600;
                        margin-bottom: 0.75rem;
                    ">{visa_type}</div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        📅 {date_str} &nbsp;|&nbsp; 💾 {size_str}
                    </div>
                </div>
                <div style="flex: 1; border-left: 1px solid #e2e8f0; padding-left: 1.5rem;">
                    <div style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">포함된 문서</div>
                    {docs_html}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 버튼 영역
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        # 캐시된 파일 데이터 사용
        cache_key = f'doc_file_{doc_id}'
        file_data = st.session_state.get(cache_key)
        
        if file_data:
            filename = f"KStay_{visa_type}_{doc_id[:8]}.zip"
            st.download_button(
                label="📥 다운로드",
                data=file_data,
                file_name=filename,
                mime="application/zip",
                key=f"dl_{doc_id}",
                use_container_width=True
            )
        else:
            st.button("📥 다운로드", key=f"dl_{doc_id}", disabled=True, use_container_width=True)
            st.caption("파일 로드 중...")
    
    with col3:
        if st.button("🗑️ 삭제", key=f"del_{doc_id}", use_container_width=True):
            st.session_state[f'confirm_delete_{doc_id}'] = True
            st.rerun()
    
    # 삭제 확인
    if st.session_state.get(f'confirm_delete_{doc_id}'):
        st.warning("⚠️ 정말 삭제하시겠습니까?")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("예, 삭제", key=f"yes_{doc_id}", type="primary"):
                success, msg = storage_service.delete_document(user_id, doc_id)
                if success:
                    # 캐시도 삭제
                    cache_key = f'doc_file_{doc_id}'
                    if cache_key in st.session_state:
                        del st.session_state[cache_key]
                    if f'confirm_delete_{doc_id}' in st.session_state:
                        del st.session_state[f'confirm_delete_{doc_id}']
                    st.rerun()
                else:
                    st.error(msg)
        with col_no:
            if st.button("아니오", key=f"no_{doc_id}"):
                del st.session_state[f'confirm_delete_{doc_id}']
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)