"""
K-Stay My Documents Page
내 문서함 - 생성된 문서 목록 조회 및 다운로드
비밀번호 확인 + 다국어 지원
"""

import streamlit as st
from datetime import datetime
from services.document_storage_service import DocumentStorageService
from services.auth_service import AuthService
from utils.i18n import t, get_current_language


def render():
    """내 문서함 페이지 렌더링"""
    
    user_id = st.session_state.get('user_id')
    user_email = st.session_state.get('user_email', '')
    
    if not user_id:
        st.warning(t('my_documents.login_required'))
        return
    
    st.markdown(f"## 📁 {t('my_documents.title')}")
    st.markdown(t('my_documents.subtitle'))
    
    st.markdown("---")
    
    # 비밀번호 확인 상태 (my_documents 전용)
    docs_password_verified = st.session_state.get('docs_password_verified', False)
    
    if not docs_password_verified:
        render_password_verification(user_email)
    else:
        render_documents_list(user_id)


def render_password_verification(user_email: str):
    """비밀번호 확인 단계"""
    
    st.markdown(f"""
        <div style="
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <p style="margin: 0; color: #92400e;">
                🔐 {t('my_documents.password_verify_msg')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("docs_password_verify_form"):
            st.markdown(f"**{t('my_page.email')}**: {user_email}")
            
            password = st.text_input(
                t('auth.password'),
                type="password",
                placeholder=t('my_documents.current_password_placeholder')
            )
            
            submitted = st.form_submit_button(t('common.confirm'), use_container_width=True, type="primary")
            
            if submitted:
                if not password:
                    st.error(t('my_documents.enter_password'))
                else:
                    auth_service = AuthService()
                    success, message, user_data = auth_service.sign_in(user_email, password)
                    
                    if success:
                        st.session_state.docs_password_verified = True
                        st.success(t('my_documents.password_verified'))
                        st.rerun()
                    else:
                        st.error(t('my_documents.password_mismatch'))


def render_documents_list(user_id: str):
    """문서 목록 렌더링"""
    
    st.markdown(f"""
        <div style="
            background: #dcfce7;
            border: 1px solid #22c55e;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <p style="margin: 0; color: #166534;">
                ✅ {t('my_documents.password_verified_msg')}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    storage_service = DocumentStorageService()
    documents = storage_service.get_user_documents(user_id)
    
    if not documents:
        st.info(f"📭 {t('my_documents.no_documents')}")
        
        if st.button(f"🚀 {t('my_documents.go_to_scenario')}", type="primary"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    else:
        # 총 문서 수
        current_lang = get_current_language()
        if current_lang == "en":
            st.markdown(f"### Total {len(documents)} document packages")
        else:
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
    
    # 비밀번호 확인 취소 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"🔒 {t('my_documents.cancel_verify')}", use_container_width=False):
        st.session_state.docs_password_verified = False
        st.rerun()


def render_document_card(doc: dict, storage_service: DocumentStorageService, user_id: str):
    """개별 문서 카드 렌더링"""
    
    doc_id = doc.get('id', '')
    scenario_name = doc.get('scenario_name', 'Unknown')
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
    date_str = format_datetime(created_at)
    
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
                    <div style="font-size: 0.8rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;">{t('my_documents.included_docs')}</div>
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
                label=f"📥 {t('my_documents.download')}",
                data=file_data,
                file_name=filename,
                mime="application/zip",
                key=f"dl_{doc_id}",
                use_container_width=True
            )
        else:
            st.button(f"📥 {t('my_documents.download')}", key=f"dl_{doc_id}", disabled=True, use_container_width=True)
            st.caption(t('my_documents.file_loading'))
    
    with col3:
        if st.button(f"🗑️ {t('my_documents.delete')}", key=f"del_{doc_id}", use_container_width=True):
            st.session_state[f'confirm_delete_{doc_id}'] = True
            st.rerun()
    
    # 삭제 확인
    if st.session_state.get(f'confirm_delete_{doc_id}'):
        st.warning(f"⚠️ {t('my_documents.delete_confirm')}")
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button(t('my_documents.delete_yes'), key=f"yes_{doc_id}", type="primary"):
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
            if st.button(t('my_documents.delete_no'), key=f"no_{doc_id}"):
                del st.session_state[f'confirm_delete_{doc_id}']
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)


def format_datetime(datetime_value):
    """날짜/시간을 언어에 맞게 포맷팅"""
    if not datetime_value:
        return "-"
    
    try:
        if 'T' in str(datetime_value):
            dt = datetime.fromisoformat(str(datetime_value).replace('Z', '+00:00').split('+')[0])
        else:
            dt = datetime.strptime(str(datetime_value)[:19], '%Y-%m-%d %H:%M:%S')
        
        current_lang = get_current_language()
        if current_lang == "en":
            return dt.strftime('%B %d, %Y %H:%M')
        else:
            return dt.strftime('%Y년 %m월 %d일 %H:%M')
    except:
        return str(datetime_value)[:16] if datetime_value else '-'