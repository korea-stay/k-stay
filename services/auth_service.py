"""
K-Stay Authentication Service
Supabase 기반 인증 처리
"""

import streamlit as st
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import hashlib
import re

# Supabase 클라이언트 (실제 배포 시 활성화)
# from supabase import create_client, Client
# from config.settings import SUPABASE_URL, SUPABASE_KEY


class AuthService:
    """인증 서비스 클래스"""
    
    def __init__(self):
        """Supabase 클라이언트 초기화"""
        # 실제 배포 시 아래 주석 해제
        # self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        pass
    
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
        """비밀번호 해시 (실제로는 Supabase Auth 사용)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
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
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            # 1. Supabase Auth로 사용자 생성
            auth_response = self.supabase.auth.sign_up({
                'email': user_data['email'],
                'password': user_data['password']
            })
            
            if auth_response.user is None:
                return False, "회원가입에 실패했습니다.", None
            
            user_id = auth_response.user.id
            
            # 2. users 테이블에 추가 정보 저장
            profile_data = {
                'id': user_id,
                'email': user_data['email'],
                'surname': user_data.get('surname', ''),
                'given_name': user_data.get('given_name', ''),
                'birth_date': user_data.get('birth_date'),
                'gender': user_data.get('gender'),
                'nationality': user_data.get('nationality'),
                'alien_registration_no': user_data.get('alien_registration_no'),
                'passport_no': user_data.get('passport_no'),
                'passport_issue_date': user_data.get('passport_issue_date'),
                'passport_expiry_date': user_data.get('passport_expiry_date'),
                'korea_address': user_data.get('korea_address'),
                'korea_phone': user_data.get('korea_phone'),
                'home_country_address': user_data.get('home_country_address'),
                'home_country_phone': user_data.get('home_country_phone'),
                'created_at': datetime.utcnow().isoformat(),
                'is_paid': False,
                'is_admin': False
            }
            
            self.supabase.table('users').insert(profile_data).execute()
            
            return True, "회원가입이 완료되었습니다!", user_id
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            import uuid
            mock_user_id = str(uuid.uuid4())
            
            # 세션에 사용자 정보 저장 (개발용)
            st.session_state.mock_users = st.session_state.get('mock_users', {})
            st.session_state.mock_users[user_data['email']] = {
                'id': mock_user_id,
                'password_hash': self.hash_password(user_data['password']),
                **user_data
            }
            
            return True, "회원가입이 완료되었습니다! 🎉", mock_user_id
            
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
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
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
            
            return True, "로그인 성공!", user_data
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            mock_users = st.session_state.get('mock_users', {})
            
            if email not in mock_users:
                return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
            
            stored_user = mock_users[email]
            if stored_user['password_hash'] != self.hash_password(password):
                return False, "이메일 또는 비밀번호가 일치하지 않습니다.", None
            
            # 비밀번호 해시 제외하고 반환
            user_data = {k: v for k, v in stored_user.items() if k != 'password_hash'}
            
            return True, "로그인 성공! 🎉", user_data
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}", None
    
    def sign_out(self) -> bool:
        """로그아웃 처리"""
        try:
            # 실제 배포 시: self.supabase.auth.sign_out()
            
            # 세션 초기화
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            return True
        except:
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """사용자 프로필 조회"""
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            response = self.supabase.table('users').select('*').eq('id', user_id).single().execute()
            return response.data
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return st.session_state.get('user_data', {})
            
        except:
            return None
    
    def update_user_profile(self, user_id: str, update_data: Dict) -> Tuple[bool, str]:
        """사용자 프로필 업데이트"""
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            self.supabase.table('users').update(update_data).eq('id', user_id).execute()
            return True, "프로필이 업데이트되었습니다."
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            st.session_state.user_data.update(update_data)
            return True, "프로필이 업데이트되었습니다."
            
        except Exception as e:
            return False, f"오류가 발생했습니다: {str(e)}"
    
    def check_payment_status(self, user_id: str) -> bool:
        """결제 상태 확인"""
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            response = self.supabase.table('users').select('is_paid').eq('id', user_id).single().execute()
            return response.data.get('is_paid', False)
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return st.session_state.get('is_paid', False)
            
        except:
            return False
    
    def check_admin_status(self, user_id: str) -> bool:
        """관리자 상태 확인"""
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            response = self.supabase.table('users').select('is_admin').eq('id', user_id).single().execute()
            return response.data.get('is_admin', False)
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return st.session_state.get('is_admin', False)
            
        except:
            return False


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
