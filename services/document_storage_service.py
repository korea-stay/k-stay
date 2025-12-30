"""
K-Stay Document Storage Service
Supabase를 이용한 문서 저장 및 관리
"""

import streamlit as st
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import base64
import uuid

# Supabase 클라이언트
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class DocumentStorageService:
    """문서 저장 서비스 클래스"""
    
    def __init__(self):
        """Supabase 클라이언트 초기화"""
        self.supabase = None
        self.use_mock = True
        
        if SUPABASE_AVAILABLE:
            try:
                supabase_url = st.secrets.get("SUPABASE_URL", "")
                supabase_key = st.secrets.get("SUPABASE_KEY", "")
                
                if supabase_url and supabase_key and "your-project" not in supabase_url:
                    self.supabase = create_client(supabase_url, supabase_key)
                    self.use_mock = False
            except Exception as e:
                print(f"⚠️ Supabase 연결 실패: {e}")
                self.use_mock = True
    
    def save_document(
        self,
        user_id: str,
        scenario_id: str,
        scenario_name: str,
        visa_type: str,
        zip_bytes: bytes,
        document_list: List[str]
    ) -> Tuple[bool, str, Optional[str]]:
        """
        생성된 문서 패키지를 저장
        """
        
        if self.use_mock:
            return self._save_document_mock(
                user_id, scenario_id, scenario_name, visa_type, zip_bytes, document_list
            )
        
        try:
            document_id = str(uuid.uuid4())
            
            # ZIP 파일을 Base64로 인코딩
            zip_base64 = base64.b64encode(zip_bytes).decode('utf-8')
            
            # document_list를 JSON 문자열이 아닌 리스트로 저장
            document_data = {
                'id': document_id,
                'user_id': str(user_id),  # 문자열로 변환
                'scenario_id': scenario_id,
                'scenario_name': scenario_name,
                'visa_type': visa_type,
                'document_list': document_list,  # Supabase가 자동으로 JSONB 처리
                'file_data': zip_base64,
                'file_size': len(zip_bytes),
                'status': 'completed'
            }
            
            result = self.supabase.table('user_documents').insert(document_data).execute()
            
            if result.data:
                return True, "문서가 저장되었습니다.", document_id
            else:
                return False, "문서 저장 실패", None
            
        except Exception as e:
            error_msg = str(e)
            print(f"문서 저장 오류: {error_msg}")
            return False, f"문서 저장 실패: {error_msg}", None
    
    def _save_document_mock(
        self,
        user_id: str,
        scenario_id: str,
        scenario_name: str,
        visa_type: str,
        zip_bytes: bytes,
        document_list: List[str]
    ) -> Tuple[bool, str, Optional[str]]:
        """Mock 모드에서 문서 저장 (세션에 저장)"""
        
        if 'mock_documents' not in st.session_state:
            st.session_state.mock_documents = {}
        
        user_key = str(user_id)
        if user_key not in st.session_state.mock_documents:
            st.session_state.mock_documents[user_key] = []
        
        document_id = str(uuid.uuid4())
        
        document_data = {
            'id': document_id,
            'user_id': user_key,
            'scenario_id': scenario_id,
            'scenario_name': scenario_name,
            'visa_type': visa_type,
            'document_list': document_list,
            'file_data': zip_bytes,
            'file_size': len(zip_bytes),
            'created_at': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        st.session_state.mock_documents[user_key].append(document_data)
        
        return True, "문서가 저장되었습니다. (Mock 모드)", document_id
    
    def get_user_documents(self, user_id: str) -> List[Dict]:
        """
        사용자의 모든 문서 목록 조회 (user_id로 필터링)
        """
        
        if self.use_mock:
            return self._get_user_documents_mock(user_id)
        
        try:
            user_id_str = str(user_id)
            
            response = self.supabase.table('user_documents')\
                .select('id, user_id, scenario_id, scenario_name, visa_type, document_list, file_size, created_at, status')\
                .eq('user_id', user_id_str)\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data or []
            
        except Exception as e:
            print(f"문서 조회 실패: {e}")
            return []
    
    def _get_user_documents_mock(self, user_id: str) -> List[Dict]:
        """Mock 모드에서 문서 목록 조회"""
        
        if 'mock_documents' not in st.session_state:
            return []
        
        user_key = str(user_id)
        user_docs = st.session_state.mock_documents.get(user_key, [])
        
        # file_data 제외하고 반환
        return [
            {k: v for k, v in doc.items() if k != 'file_data'}
            for doc in sorted(user_docs, key=lambda x: x['created_at'], reverse=True)
        ]
    
    def get_document_file(self, user_id: str, document_id: str) -> Optional[bytes]:
        """
        특정 문서의 파일 데이터 조회 (user_id로 권한 확인)
        """
        
        if self.use_mock:
            return self._get_document_file_mock(user_id, document_id)
        
        try:
            user_id_str = str(user_id)
            
            response = self.supabase.table('user_documents')\
                .select('file_data, user_id')\
                .eq('id', document_id)\
                .single()\
                .execute()
            
            if response.data:
                # 권한 확인: 자신의 문서인지 체크
                if response.data.get('user_id') != user_id_str:
                    print("권한 없음: 다른 사용자의 문서")
                    return None
                
                file_data = response.data.get('file_data')
                if file_data:
                    return base64.b64decode(file_data)
            
            return None
            
        except Exception as e:
            print(f"파일 조회 실패: {e}")
            return None
    
    def _get_document_file_mock(self, user_id: str, document_id: str) -> Optional[bytes]:
        """Mock 모드에서 파일 데이터 조회"""
        
        if 'mock_documents' not in st.session_state:
            return None
        
        user_key = str(user_id)
        user_docs = st.session_state.mock_documents.get(user_key, [])
        
        for doc in user_docs:
            if doc['id'] == document_id:
                return doc.get('file_data')
        
        return None
    
    def delete_document(self, user_id: str, document_id: str) -> Tuple[bool, str]:
        """
        문서 삭제 (user_id로 권한 확인)
        """
        
        if self.use_mock:
            return self._delete_document_mock(user_id, document_id)
        
        try:
            user_id_str = str(user_id)
            
            # 먼저 문서 소유권 확인
            check = self.supabase.table('user_documents')\
                .select('user_id')\
                .eq('id', document_id)\
                .single()\
                .execute()
            
            if not check.data or check.data.get('user_id') != user_id_str:
                return False, "권한이 없거나 문서를 찾을 수 없습니다."
            
            # 삭제 실행
            self.supabase.table('user_documents')\
                .delete()\
                .eq('id', document_id)\
                .execute()
            
            return True, "문서가 삭제되었습니다."
            
        except Exception as e:
            return False, f"삭제 실패: {str(e)}"
    
    def _delete_document_mock(self, user_id: str, document_id: str) -> Tuple[bool, str]:
        """Mock 모드에서 문서 삭제"""
        
        if 'mock_documents' not in st.session_state:
            return False, "문서를 찾을 수 없습니다."
        
        user_key = str(user_id)
        user_docs = st.session_state.mock_documents.get(user_key, [])
        
        for i, doc in enumerate(user_docs):
            if doc['id'] == document_id:
                del st.session_state.mock_documents[user_key][i]
                return True, "문서가 삭제되었습니다. (Mock 모드)"
        
        return False, "문서를 찾을 수 없습니다."
    
    def is_connected(self) -> bool:
        """Supabase 연결 상태 확인"""
        return not self.use_mock
