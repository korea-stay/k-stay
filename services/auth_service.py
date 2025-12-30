"""
K-Stay Authentication Service
Supabase 기반 인증 처리
"""

import streamlit as st
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import hashlib
import re

# Supabase 클라이언트
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class AuthService:
    """인증 서비스 클래스"""
    
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
                print(f"⚠️ Supabase 연결 실패, Mock 모드 사용: {e}")
                self.use_mock = True
    
    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "비밀번호는 8자 이상이어야 합니다."
        if not re.search(r'[A-Za-z]', password):
            return False, "비밀번호에 영문자가 포함되어야 합니다."
        if not re.search(r'\d', password):
            return False, "비밀번호에 숫자가 포함되어야 합니다."
        return True, "유효한 비밀번호입니다."
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _format_date(self, date_value) -> Optional[str]:
        if date_value is None:
            return None
        if isinstance(date_value, str):
            return date_value
        if hasattr(date_value, 'isoformat'):
            return date_value.isoformat()
        return str(date_value)
    
    def sign_up(self, user_data: Dict) -> Tuple[bool, str, Optional[str]]:
        """회원가입 처리"""
        try:
            if not self.validate_email(user_data.get('email', '')):
                return False, "유효한 이메일 주소를 입력해주세요.", None
            
            is_valid_pw, pw_msg = self.validate_password(user_data.get('password', ''))
            if not is_valid_pw:
                return False, pw_msg, None
            
            if not self.use_mock and self.supabase:
                try:
                    auth_response = self.supabase.auth.sign_up({
                        'email': user_data['email'],
                        'password': user_data['password']
                    })
                    
                    if auth_response.user is None:
                        return False, "회원가입에 실패했습니다. 이미 등록된 이메일일 수 있습니다.", None
                    
                    user_id = auth_response.user.id
                    
                    profile_data = {
                        'id': user_id,
                        'email': user_data['email'],
                        'surname': user_data.get('surname', ''),
                        'given_name': user_data.get('given_name', ''),
                        'birth_date': self._format_date(user_data.get('birth_date')),
                        'gender': user_data.get('gender', ''),
                        'nationality': user_data.get('nationality', ''),
                        'passport_no': user_data.get('passport_no', ''),
                        'passport_expiry_date': self._format_date(user_data.get('passport_expiry')),
                        'korea_phone': user_data.get('korea_phone', ''),
                        'korea_address': user_data.get('korea_address', ''),
                        'is_paid': False,
                        'is_admin': False
                    }
                    
                    self.supabase.table('users').insert(profile_data).execute()
                    
                    return True, "회원가입이 완료되었습니다! 🎉", user_id
                    
                except Exception as e:
                    error_msg = str(e)
                    if "User already registered" in error_msg:
                        return False, "이미 등록된 이메일입니다.", None
                    return False, f"회원가입 중 오류가 발생했습니다: {error_msg}", None
            
            else:
                mock_users = st.session_state.get('mock_users', {})
                
                if user_data['email'] in mock_users:
                    return False, "이미 등록된 이메일입니다.", None
                
                mock_user_id = f"mock-{len(mock_users) + 1}"
                
                mock_users[user_data['email']] = {
                    'id': mock_user_id,
                    'email': user_data['email'],
                    'password_hash': self.hash_password(user_data['password']),
                    'surname': user_data.get('surname', ''),
                    'given_name': user_data.get('given_name', ''),
                    'birth_date': self._format_date(user_data.get('birth_date')),
                    'gender': user_data.get('gender', ''),
                    'nationality': user_data.get('nationality', ''),
                    'passport_no': user_data.get('passport_no', ''),
                    'passport_expiry_date': self._format_date(user_data.get('passport_expiry')),
                    'korea_phone': user_data.get('korea_phone', ''),
                    'korea_address': user_data.get('korea_address', ''),
                    'is_paid': False,
                    'is_admin': False
                }
                
                st.session_state.mock_users = mock_users
                
                return True, "회원가입이 완료되었습니다! 🎉 (Mock 모드)", mock_user_id
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}", None
    
    def sign_in(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """로그인 처리"""
        try:
            if not self.use_mock and self.supabase:
                try:
                    auth_response = self.supabase.auth.sign_in_with_password({
                        'email': email,
                        'password': password
                    })
                    
                    if auth_response.user is None:
                        return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                    
                    user_id = auth_response.user.id
                    
                    # 세션 토큰 저장 (업데이트 시 필요)
                    if auth_response.session:
                        st.session_state._supabase_access_token = auth_response.session.access_token
                        st.session_state._supabase_refresh_token = auth_response.session.refresh_token
                    
                    # DB에서 최신 프로필 가져오기
                    profile_response = self.supabase.table('users').select('*').eq('id', user_id).single().execute()
                    
                    user_data = profile_response.data
                    
                    if user_data is None:
                        return False, "사용자 정보를 찾을 수 없습니다.", None
                    
                    return True, "로그인 성공! 🎉", user_data
                    
                except Exception as e:
                    error_msg = str(e)
                    if "Invalid login credentials" in error_msg:
                        return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                    return False, f"로그인 중 오류가 발생했습니다: {error_msg}", None
            
            else:
                mock_users = st.session_state.get('mock_users', {})
                
                if email not in mock_users:
                    return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                
                stored_user = mock_users[email]
                if stored_user['password_hash'] != self.hash_password(password):
                    return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                
                user_data = {k: v for k, v in stored_user.items() if k != 'password_hash'}
                
                return True, "로그인 성공! 🎉 (Mock 모드)", user_data
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}", None
    
    def sign_out(self) -> bool:
        """로그아웃 처리"""
        try:
            if not self.use_mock and self.supabase:
                self.supabase.auth.sign_out()
            
            keys_to_keep = ['mock_users']
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            
            return True
        except:
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """사용자 프로필 조회"""
        if self.use_mock:
            mock_users = st.session_state.get('mock_users', {})
            for user in mock_users.values():
                if user.get('id') == user_id:
                    return {k: v for k, v in user.items() if k != 'password_hash'}
            return None
        
        if not self.supabase:
            return None
        
        try:
            response = self.supabase.table('users').select('*').eq('id', user_id).single().execute()
            return response.data
        except:
            return None
    
    def update_user_profile(self, user_id: str, updates: Dict) -> Tuple[bool, str]:
        """사용자 프로필 업데이트"""
        if self.use_mock:
            mock_users = st.session_state.get('mock_users', {})
            for email, user in mock_users.items():
                if user.get('id') == user_id:
                    user.update(updates)
                    st.session_state.mock_users = mock_users
                    return True, "프로필이 업데이트되었습니다."
            return False, "사용자를 찾을 수 없습니다."
        
        if not self.supabase:
            return False, "데이터베이스에 연결되지 않았습니다."
        
        try:
            # 저장된 토큰으로 세션 복원 (RLS 우회를 위해)
            access_token = st.session_state.get('_supabase_access_token')
            refresh_token = st.session_state.get('_supabase_refresh_token')
            
            if access_token and refresh_token:
                try:
                    self.supabase.auth.set_session(access_token, refresh_token)
                except:
                    pass
            
            # updated_at 필드 추가
            updates['updated_at'] = datetime.now().isoformat()
            
            # 업데이트 실행
            response = self.supabase.table('users').update(updates).eq('id', user_id).execute()
            
            # 결과 확인
            if response.data and len(response.data) > 0:
                return True, "프로필이 업데이트되었습니다."
            else:
                # 데이터가 없으면 업데이트 실패
                return False, "업데이트된 데이터가 없습니다. RLS 정책을 확인해주세요."
                
        except Exception as e:
            return False, f"업데이트 실패: {str(e)}"
    
    def is_supabase_connected(self) -> bool:
        return not self.use_mock and self.supabase is not None


class SessionManager:
    """세션 관리 유틸리티"""
    
    @staticmethod
    def login_user(user_data: Dict):
        st.session_state.authenticated = True
        st.session_state.user_id = user_data.get('id')
        st.session_state.user_email = user_data.get('email')
        st.session_state.user_data = user_data
        st.session_state.is_paid = user_data.get('is_paid', False)
        st.session_state.is_admin = user_data.get('is_admin', False)
        st.session_state.current_page = 'dashboard'
    
    @staticmethod
    def logout_user():
        auth_service = AuthService()
        auth_service.sign_out()
    
    @staticmethod
    def is_authenticated() -> bool:
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_current_user() -> Optional[Dict]:
        if SessionManager.is_authenticated():
            return st.session_state.get('user_data')
        return None
    
    @staticmethod
    def require_auth():
        if not SessionManager.is_authenticated():
            st.warning("이 페이지에 접근하려면 로그인이 필요합니다.")
            st.stop()