"""
K-Stay Payment Service
Stripe 기반 결제 처리
"""

import streamlit as st
from typing import Optional, Dict, Tuple
from datetime import datetime

# Stripe 클라이언트 (실제 배포 시 활성화)
# import stripe
# from config.settings import STRIPE_API_KEY, STRIPE_PRICE_ID, STRIPE_SUCCESS_URL, STRIPE_CANCEL_URL


class PaymentService:
    """결제 서비스 클래스"""
    
    def __init__(self):
        """Stripe 초기화"""
        # 실제 배포 시 아래 주석 해제
        # stripe.api_key = STRIPE_API_KEY
        pass
    
    def create_checkout_session(self, user_id: str, user_email: str) -> Optional[str]:
        """
        Stripe Checkout 세션 생성
        
        Args:
            user_id: 사용자 ID
            user_email: 사용자 이메일
            
        Returns:
            Checkout URL 또는 None
        """
        try:
            # =================================================================
            # 실제 Stripe 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': STRIPE_PRICE_ID,
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{STRIPE_SUCCESS_URL}&user_id={user_id}",
                cancel_url=STRIPE_CANCEL_URL,
                customer_email=user_email,
                metadata={
                    'user_id': user_id
                }
            )
            
            return checkout_session.url
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            # 개발 환경에서는 바로 결제 성공 처리
            st.session_state.is_paid = True
            st.success("🎉 개발 모드: 결제가 완료되었습니다!")
            return None
            
        except Exception as e:
            st.error(f"결제 세션 생성 실패: {str(e)}")
            return None
    
    def verify_payment(self, session_id: str) -> Tuple[bool, Dict]:
        """
        결제 완료 확인
        
        Args:
            session_id: Stripe 세션 ID
            
        Returns:
            (성공여부, 결제정보)
        """
        try:
            # =================================================================
            # 실제 Stripe 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                payment_info = {
                    'session_id': session_id,
                    'amount': session.amount_total / 100,
                    'currency': session.currency,
                    'customer_email': session.customer_email,
                    'payment_status': session.payment_status,
                    'created_at': datetime.utcnow().isoformat()
                }
                return True, payment_info
            
            return False, {}
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return True, {
                'session_id': 'mock_session',
                'amount': 9.99,
                'currency': 'usd',
                'payment_status': 'paid'
            }
            
        except Exception as e:
            return False, {'error': str(e)}
    
    def record_payment(self, user_id: str, payment_info: Dict) -> bool:
        """
        결제 기록 저장 (Supabase)
        
        Args:
            user_id: 사용자 ID
            payment_info: 결제 정보
            
        Returns:
            성공 여부
        """
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            from supabase import create_client
            from config.settings import SUPABASE_URL, SUPABASE_KEY
            
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # 1. payments 테이블에 기록
            supabase.table('payments').insert({
                'user_id': user_id,
                'stripe_session_id': payment_info.get('session_id'),
                'amount': payment_info.get('amount'),
                'currency': payment_info.get('currency'),
                'status': payment_info.get('payment_status'),
                'created_at': datetime.utcnow().isoformat()
            }).execute()
            
            # 2. users 테이블의 is_paid 업데이트
            supabase.table('users').update({
                'is_paid': True,
                'paid_at': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            
            return True
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            st.session_state.is_paid = True
            return True
            
        except Exception as e:
            st.error(f"결제 기록 저장 실패: {str(e)}")
            return False
    
    def check_payment_status(self, user_id: str) -> bool:
        """
        사용자 결제 상태 확인
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            결제 여부
        """
        try:
            # =================================================================
            # 실제 Supabase 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            from supabase import create_client
            from config.settings import SUPABASE_URL, SUPABASE_KEY
            
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            response = supabase.table('users').select('is_paid').eq('id', user_id).single().execute()
            return response.data.get('is_paid', False)
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return st.session_state.get('is_paid', False)
            
        except:
            return False


class PaymentGateway:
    """결제 게이트웨이 UI 컴포넌트"""
    
    @staticmethod
    def render_payment_modal():
        """결제 필요 모달 렌더링"""
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(201, 162, 39, 0.1) 0%, rgba(201, 162, 39, 0.05) 100%);
                border: 2px solid #C9A227;
                border-radius: 20px;
                padding: 3rem;
                text-align: center;
                margin: 2rem 0;
            ">
                <h2 style="color: #C9A227; margin-bottom: 1rem;">🔒 Premium 기능</h2>
                <p style="color: #a0aec0; margin-bottom: 2rem;">
                    이 기능을 사용하려면 Premium 구매가 필요합니다.
                </p>
                <div style="
                    background: rgba(255,255,255,0.05);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 2rem;
                ">
                    <h3 style="color: white; margin: 0;">$9.99</h3>
                    <p style="color: #6c757d; margin: 0.5rem 0 0 0;">일회성 결제 · 평생 이용</p>
                </div>
                <ul style="text-align: left; color: #a0aec0; margin-bottom: 2rem;">
                    <li>✅ 6가지 시나리오 무제한 이용</li>
                    <li>✅ AI 문서 자동 생성</li>
                    <li>✅ 전문가 수준의 사연서 작성</li>
                    <li>✅ ZIP 패키지 다운로드</li>
                    <li>✅ AI 상담사 무제한 이용</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_premium_badge():
        """프리미엄 배지 렌더링"""
        return """
            <span style="
                background: linear-gradient(135deg, #C9A227 0%, #E8D5A3 50%, #C9A227 100%);
                color: #0A1628;
                padding: 0.3rem 0.8rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
            ">PREMIUM</span>
        """
    
    @staticmethod
    def check_and_redirect(user_id: str) -> bool:
        """결제 확인 및 리다이렉트"""
        payment_service = PaymentService()
        
        # 관리자는 무료 통과
        if st.session_state.get('is_admin', False):
            return True
        
        # 결제 상태 확인
        if payment_service.check_payment_status(user_id):
            return True
        
        # 결제 필요
        PaymentGateway.render_payment_modal()
        
        if st.button("💳 Premium 구매하기", type="primary", use_container_width=True):
            checkout_url = payment_service.create_checkout_session(
                user_id,
                st.session_state.get('user_email', '')
            )
            if checkout_url:
                st.markdown(f"""
                    <script>
                        window.open('{checkout_url}', '_blank');
                    </script>
                """, unsafe_allow_html=True)
        
        return False
