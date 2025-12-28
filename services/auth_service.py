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
        self.use_mock = True  # 기본값: Mock 모드
        
        if SUPABASE_AVAILABLE:
            try:
                supabase_url = st.secrets.get("SUPABASE_URL", "")
                supabase_key = st.secrets.get("SUPABASE_KEY", "")
                
                if supabase_url and supabase_key and "your-project" not in supabase_url:
                    self.supabase = create_client(supabase_url, supabase_key)
                    self.use_mock = False
                    print("✅ Supabase 연결 성공")
            except Exception as e:
                print(f"⚠️ Supabase 연결 실패, Mock 모드 사용: {e}")
                self.use_mock = True
    
    def validate_email(self, email: str) -> bool:
        """이메일 형식 검증"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """비밀번호 강도 검증"""
        if len(password) < 8:
            return False, "비밀번호는 8자 이상이어야 합니다."
        if not re.search(r'[A-Za-z]', password):
            return False, "비밀번호에 영문자가 포함되어야 합니다."
        if not re.search(r'\d', password):
            return False, "비밀번호에 숫자가 포함되어야 합니다."
        return True, "유효한 비밀번호입니다."
    
    def hash_password(self, password: str) -> str:
        """비밀번호 해시 (Mock 모드용)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _format_date(self, date_value) -> Optional[str]:
        """날짜를 문자열로 변환"""
        if date_value is None:
            return None
        if hasattr(date_value, 'isoformat'):
            return date_value.isoformat()
        return str(date_value)
    
    def sign_up(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
        """
        회원가입 처리
        
        Args:
            user_data: 사용자 정보 딕셔너리
            
        Returns:
            (성공여부, 메시지, 사용자ID)
        """
        try:
            # 이메일 검증
            if not self.validate_email(user_data.get('email', '')):
                return False, "유효하지 않은 이메일 형식입니다.", None
            
            # 비밀번호 검증
            is_valid, msg = self.validate_password(user_data.get('password', ''))
            if not is_valid:
                return False, msg, None
            
            # =================================================================
            # Supabase 연동 모드
            # =================================================================
            if not self.use_mock and self.supabase:
                try:
                    # 1. Supabase Auth로 사용자 생성
                    auth_response = self.supabase.auth.sign_up({
                        'email': user_data['email'],
                        'password': user_data['password']
                    })
                    
                    if auth_response.user is None:
                        return False, "회원가입에 실패했습니다. 이미 등록된 이메일일 수 있습니다.", None
                    
                    user_id = auth_response.user.id
                    
                    # 2. users 테이블에 추가 정보 저장
                    profile_data = {
                        'id': user_id,
                        'email': user_data['email'],
                        'surname': user_data.get('surname', ''),
                        'given_name': user_data.get('given_name', ''),
                        'birth_date': self._format_date(user_data.get('birth_date')),
                        'gender': user_data.get('gender'),
                        'nationality': user_data.get('nationality'),
                        'alien_registration_no': user_data.get('alien_registration_no'),
                        'passport_no': user_data.get('passport_no'),
                        'passport_issue_date': self._format_date(user_data.get('passport_issue_date')),
                        'passport_expiry_date': self._format_date(user_data.get('passport_expiry_date')),
                        'korea_address': user_data.get('korea_address'),
                        'korea_phone': user_data.get('korea_phone'),
                        'home_country_address': user_data.get('home_country_address'),
                        'home_country_phone': user_data.get('home_country_phone'),
                        'is_paid': False,
                        'is_admin': False
                    }
                    
                    # None 값 제거
                    profile_data = {k: v for k, v in profile_data.items() if v is not None}
                    
                    self.supabase.table('users').insert(profile_data).execute()
                    
                    return True, "회원가입이 완료되었습니다! 이메일을 확인해주세요. 🎉", user_id
                    
                except Exception as e:
                    error_msg = str(e)
                    if "User already registered" in error_msg:
                        return False, "이미 등록된 이메일입니다.", None
                    return False, f"회원가입 중 오류가 발생했습니다: {error_msg}", None
            
            # =================================================================
            # Mock 모드 (개발/테스트용)
            # =================================================================
            else:
                import uuid
                mock_user_id = str(uuid.uuid4())
                
                # 세션에 사용자 정보 저장 (개발용)
                if 'mock_users' not in st.session_state:
                    st.session_state.mock_users = {}
                
                if user_data['email'] in st.session_state.mock_users:
                    return False, "이미 등록된 이메일입니다.", None
                
                st.session_state.mock_users[user_data['email']] = {
                    'id': mock_user_id,
                    'password_hash': self.hash_password(user_data['password']),
                    'is_paid': False,
                    'is_admin': False,
                    **{k: v for k, v in user_data.items() if k != 'password'}
                }
                
                return True, "회원가입이 완료되었습니다! 🎉 (Mock 모드)", mock_user_id
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}", None
    
    def sign_in(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        로그인 처리
        
        Args:
            email: 이메일
            password: 비밀번호
            
        Returns:
            (성공여부, 메시지, 사용자데이터)
        """
        try:
            # =================================================================
            # Supabase 연동 모드
            # =================================================================
            if not self.use_mock and self.supabase:
                try:
                    # 1. Supabase Auth로 로그인
                    auth_response = self.supabase.auth.sign_in_with_password({
                        'email': email,
                        'password': password
                    })
                    
                    if auth_response.user is None:
                        return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                    
                    user_id = auth_response.user.id
                    
                    # 2. users 테이블에서 프로필 정보 가져오기
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
            
            # =================================================================
            # Mock 모드 (개발/테스트용)
            # =================================================================
            else:
                mock_users = st.session_state.get('mock_users', {})
                
                if email not in mock_users:
                    return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                
                stored_user = mock_users[email]
                if stored_user['password_hash'] != self.hash_password(password):
                    return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
                
                # 비밀번호 해시 제외하고 반환
                user_data = {k: v for k, v in stored_user.items() if k != 'password_hash'}
                
                return True, "로그인 성공! 🎉 (Mock 모드)", user_data
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}", None
    
    def sign_out(self) -> bool:
        """로그아웃 처리"""
        try:
            if not self.use_mock and self.supabase:
                self.supabase.auth.sign_out()
            
            # 세션 초기화 (mock_users는 유지)
            keys_to_keep = ['mock_users']
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            
            return True
        except:
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """사용자 프로필 조회"""
        try:
            if not self.use_mock and self.supabase:
                response = self.supabase.table('users').select('*').eq('id', user_id).single().execute()
                return response.data
            else:
                return st.session_state.get('user_data', {})
        except:
            return None
    
    def update_user_profile(self, user_id: str, update_data: Dict) -> Tuple[bool, str]:
        """사용자 프로필 업데이트"""
        try:
            if not self.use_mock and self.supabase:
                # 날짜 필드 변환
                for key in ['birth_date', 'passport_issue_date', 'passport_expiry_date']:
                    if key in update_data:
                        update_data[key] = self._format_date(update_data[key])
                
                self.supabase.table('users').update(update_data).eq('id', user_id).execute()
                return True, "프로필이 업데이트되었습니다."
            else:
                if 'user_data' in st.session_state:
                    st.session_state.user_data.update(update_data)
                return True, "프로필이 업데이트되었습니다. (Mock 모드)"
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}"
    
    def check_payment_status(self, user_id: str) -> bool:
        """결제 상태 확인"""
        try:
            if not self.use_mock and self.supabase:
                response = self.supabase.table('users').select('is_paid').eq('id', user_id).single().execute()
                return response.data.get('is_paid', False) if response.data else False
            else:
                return st.session_state.get('is_paid', False)
        except:
            return False
    
    def check_admin_status(self, user_id: str) -> bool:
        """관리자 상태 확인"""
        try:
            if not self.use_mock and self.supabase:
                response = self.supabase.table('users').select('is_admin').eq('id', user_id).single().execute()
                return response.data.get('is_admin', False) if response.data else False
            else:
                return st.session_state.get('is_admin', False)
        except:
            return False
    
    def is_supabase_connected(self) -> bool:
        """Supabase 연결 상태 확인"""
        return not self.use_mock and self.supabase is not None


class SessionManager:
    """세션 관리 클래스"""
    
    @staticmethod
    def login_user(user_data: Dict):
        """사용자 로그인 세션 설정"""
        st.session_state.authenticated = True
        st.session_state.user_id = user_data.get('id')
        st.session_state.user_email = user_data.get('email')
        st.session_state.user_data = user_data
        st.session_state.is_paid = user_data.get('is_paid', False)
        st.session_state.is_admin = user_data.get('is_admin', False)
        st.session_state.current_page = 'dashboard'
    
    @staticmethod
    def logout_user():
        """사용자 로그아웃"""
        keys_to_keep = ['mock_users']  # 개발용 목업 데이터 유지
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """인증 상태 확인"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def require_auth():
        """인증 필요 페이지 가드"""
        if not SessionManager.is_authenticated():
            st.warning("로그인이 필요합니다.")
            st.stop()
    
    @staticmethod
    def require_payment():
        """결제 필요 페이지 가드"""
        if not st.session_state.get('is_paid', False) and not st.session_state.get('is_admin', False):
            st.warning("이 기능을 사용하려면 Premium 구매가 필요합니다.")
            st.stop()
