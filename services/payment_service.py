"""
K-Stay Payment Service
Stripe 기반 결제 처리
"""

import streamlit as st
from typing import Optional, Dict, Tuple
from datetime import datetime

# Stripe
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


class PaymentService:
    """결제 서비스 클래스"""
    
    def __init__(self):
        """Stripe 초기화"""
        self.use_mock = True
        
        if STRIPE_AVAILABLE:
            try:
                secret_key = st.secrets.get("STRIPE_SECRET_KEY", "")
                if secret_key and secret_key.startswith("sk_"):
                    stripe.api_key = secret_key
                    self.use_mock = False
            except Exception as e:
                self.use_mock = True
    
    def is_stripe_connected(self) -> bool:
        return not self.use_mock
    
    def create_checkout_session(self, user_id: str, user_email: str) -> Optional[str]:
        """Stripe Checkout 세션 생성"""
        try:
            if not self.use_mock:
                price_id = st.secrets.get("STRIPE_PRICE_ID", "")
                success_url = st.secrets.get("STRIPE_SUCCESS_URL", "http://localhost:8501/?payment=success")
                cancel_url = st.secrets.get("STRIPE_CANCEL_URL", "http://localhost:8501/?payment=cancel")
                
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{'price': price_id, 'quantity': 1}],
                    mode='payment',
                    success_url=f"{success_url}&session_id={{CHECKOUT_SESSION_ID}}",
                    cancel_url=cancel_url,
                    customer_email=user_email if user_email else None,
                    metadata={'user_id': user_id}
                )
                return checkout_session.url
            return None
        except Exception as e:
            st.error(f"결제 세션 생성 실패: {str(e)}")
            return None
    
    def verify_payment(self, session_id: str) -> Tuple[bool, Dict]:
        """결제 완료 확인"""
        try:
            if not self.use_mock and session_id:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status == 'paid':
                    return True, {
                        'session_id': session_id,
                        'payment_intent': session.payment_intent,
                        'amount': session.amount_total / 100,
                        'currency': session.currency,
                        'customer_email': session.customer_email,
                        'payment_status': session.payment_status,
                        'user_id': session.metadata.get('user_id'),
                    }
                return False, {}
            return True, {'session_id': 'mock', 'amount': 9.99, 'payment_status': 'paid'}
        except Exception as e:
            return False, {'error': str(e)}
    
    def record_payment_to_db(self, user_id: str, payment_info: Dict) -> bool:
        """결제 기록을 Supabase에 저장"""
        try:
            from supabase import create_client
            supabase_url = st.secrets.get("SUPABASE_URL", "")
            supabase_key = st.secrets.get("SUPABASE_KEY", "")
            
            if supabase_url and supabase_key and "your-project" not in supabase_url:
                supabase = create_client(supabase_url, supabase_key)
                
                # users 테이블 업데이트
                supabase.table('users').update({
                    'is_paid': True,
                    'paid_at': datetime.utcnow().isoformat()
                }).eq('id', user_id).execute()
                
            st.session_state.is_paid = True
            return True
        except Exception as e:
            st.error(f"DB 저장 실패: {str(e)}")
            return False
    
    def check_payment_status(self, user_id: str) -> bool:
        """결제 상태 확인"""
        # 먼저 세션 확인
        if st.session_state.get('is_paid', False):
            return True
        
        # DB에서 확인
        try:
            from supabase import create_client
            supabase_url = st.secrets.get("SUPABASE_URL", "")
            supabase_key = st.secrets.get("SUPABASE_KEY", "")
            
            if supabase_url and supabase_key and "your-project" not in supabase_url:
                supabase = create_client(supabase_url, supabase_key)
                response = supabase.table('users').select('is_paid').eq('id', user_id).single().execute()
                if response.data and response.data.get('is_paid'):
                    st.session_state.is_paid = True
                    return True
        except:
            pass
        
        return False
