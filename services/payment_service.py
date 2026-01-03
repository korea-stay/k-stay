"""
K-Stay Payment Service
Stripe Embedded Checkout 지원
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Dict, Tuple
from datetime import datetime

# Stripe
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


class PaymentService:
    """결제 서비스 클래스 - Embedded Checkout 지원"""
    
    def __init__(self):
        """Stripe 초기화"""
        self.use_mock = True
        self.publishable_key = ""
        
        if STRIPE_AVAILABLE:
            try:
                secret_key = st.secrets.get("STRIPE_SECRET_KEY", "")
                self.publishable_key = st.secrets.get("STRIPE_PUBLISHABLE_KEY", "")
                
                if secret_key and secret_key.startswith("sk_"):
                    stripe.api_key = secret_key
                    self.use_mock = False
            except Exception as e:
                self.use_mock = True
    
    def is_stripe_connected(self) -> bool:
        return not self.use_mock
    
    # =========================================================================
    # Embedded Checkout (추천 방식)
    # =========================================================================
    
    def create_embedded_checkout_session(self, user_id: str, user_email: str) -> Optional[str]:
        """
        Embedded Checkout용 세션 생성
        Returns: client_secret (Embedded Checkout에 필요)
        """
        try:
            if self.use_mock:
                return None
            
            price_id = st.secrets.get("STRIPE_PRICE_ID", "")
            return_url = st.secrets.get("STRIPE_RETURN_URL", "")
            
            if not return_url:
                return_url = "https://your-app.streamlit.app/?payment=complete&session_id={CHECKOUT_SESSION_ID}"
            
            checkout_session = stripe.checkout.Session.create(
                ui_mode="embedded",  # Embedded 모드
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='payment',
                return_url=return_url,
                customer_email=user_email if user_email else None,
                metadata={'user_id': user_id}
            )
            
            st.session_state.pending_checkout_session_id = checkout_session.id
            return checkout_session.client_secret
            
        except Exception as e:
            st.error(f"Embedded 세션 생성 실패: {str(e)}")
            return None
    
    def render_embedded_checkout(self, client_secret: str, height: int = 700):
        """Streamlit에 Embedded Checkout 렌더링"""
        if not client_secret or not self.publishable_key:
            st.error("결제 설정이 올바르지 않습니다.")
            return
        
        checkout_html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://js.stripe.com/v3/"></script>
            <style>
                body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: transparent; }}
                #checkout {{ min-height: {height - 100}px; }}
                .loading {{ display: flex; justify-content: center; align-items: center; height: 200px; color: #64748b; font-size: 14px; }}
                .loading::after {{ content: ''; width: 20px; height: 20px; border: 2px solid #e2e8f0; border-top-color: #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; margin-left: 10px; }}
                @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
                .error {{ background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; color: #dc2626; text-align: center; }}
            </style>
        </head>
        <body>
            <div id="checkout"><div class="loading">결제 폼 로딩 중...</div></div>
            <script>
                const stripe = Stripe('{self.publishable_key}');
                async function initialize() {{
                    try {{
                        const checkout = await stripe.initEmbeddedCheckout({{ clientSecret: '{client_secret}' }});
                        document.getElementById('checkout').innerHTML = '';
                        checkout.mount('#checkout');
                    }} catch (error) {{
                        document.getElementById('checkout').innerHTML = '<div class="error">결제 폼 로드 실패: ' + error.message + '</div>';
                    }}
                }}
                initialize();
            </script>
        </body>
        </html>
        '''
        
        components.html(checkout_html, height=height, scrolling=True)
    
    # =========================================================================
    # 기존 Redirect 방식 (대체 옵션)
    # =========================================================================
    
    def create_checkout_session(self, user_id: str, user_email: str) -> Tuple[Optional[str], Optional[str]]:
        """Stripe Checkout 세션 생성 (Redirect 방식)"""
        try:
            if self.use_mock:
                return None, None
            
            price_id = st.secrets.get("STRIPE_PRICE_ID", "")
            success_url = st.secrets.get("STRIPE_SUCCESS_URL", "")
            cancel_url = st.secrets.get("STRIPE_CANCEL_URL", "")
            
            if "?" in success_url:
                success_url_with_session = f"{success_url}&session_id={{CHECKOUT_SESSION_ID}}"
            else:
                success_url_with_session = f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}"
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': price_id, 'quantity': 1}],
                mode='payment',
                success_url=success_url_with_session,
                cancel_url=cancel_url,
                customer_email=user_email if user_email else None,
                metadata={'user_id': user_id}
            )
            
            st.session_state.pending_checkout_session_id = checkout_session.id
            return checkout_session.url, checkout_session.id
            
        except Exception as e:
            st.error(f"결제 세션 생성 실패: {str(e)}")
            return None, None
    
    # =========================================================================
    # 결제 확인 및 처리
    # =========================================================================
    
    def verify_payment(self, session_id: str) -> Tuple[bool, Dict]:
        """결제 완료 확인"""
        try:
            if self.use_mock:
                return True, {'session_id': 'mock', 'amount': 9.99, 'payment_status': 'paid'}
            
            if not session_id:
                return False, {'error': 'No session ID'}
            
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                return True, {
                    'session_id': session_id,
                    'payment_intent': session.payment_intent,
                    'amount': session.amount_total / 100 if session.amount_total else 0,
                    'currency': session.currency,
                    'customer_email': session.customer_email,
                    'payment_status': session.payment_status,
                    'user_id': session.metadata.get('user_id'),
                }
            
            return False, {'payment_status': session.payment_status}
            
        except Exception as e:
            return False, {'error': str(e)}
    
    def check_session_status(self, session_id: str) -> str:
        """세션 상태 확인 (폴링용)"""
        try:
            if self.use_mock:
                return 'complete'
            if not session_id:
                return 'error'
            session = stripe.checkout.Session.retrieve(session_id)
            return session.status
        except Exception as e:
            return 'error'
    
    def record_payment_to_db(self, user_id: str, payment_info: Dict) -> bool:
        """결제 기록을 Supabase에 저장"""
        try:
            from supabase import create_client
            supabase_url = st.secrets.get("SUPABASE_URL", "")
            supabase_key = st.secrets.get("SUPABASE_KEY", "")
            
            if supabase_url and supabase_key and "your-project" not in supabase_url:
                supabase = create_client(supabase_url, supabase_key)
                supabase.table('users').update({
                    'is_paid': True,
                    'paid_at': datetime.utcnow().isoformat(),
                    'stripe_session_id': payment_info.get('session_id', ''),
                }).eq('id', user_id).execute()
            
            st.session_state.is_paid = True
            return True
        except Exception as e:
            st.session_state.is_paid = True
            return False
    
    def check_payment_status(self, user_id: str) -> bool:
        """사용자의 결제 상태 확인"""
        if st.session_state.get('is_paid', False):
            return True
        
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
    
    def handle_return_from_checkout(self) -> bool:
        """결제 페이지에서 돌아왔을 때 처리"""
        try:
            params = st.query_params
            payment_status = params.get("payment", "")
            session_id = params.get("session_id", "")
            
            if payment_status in ["complete", "success"] and session_id:
                is_paid, payment_info = self.verify_payment(session_id)
                if is_paid:
                    user_id = st.session_state.get('user_id', '')
                    self.record_payment_to_db(user_id, payment_info)
                    st.query_params.clear()
                    return True
            elif payment_status == "cancel":
                st.query_params.clear()
                st.warning("결제가 취소되었습니다.")
            return False
        except Exception as e:
            return False


def render_payment_section(scenario, payment_service: PaymentService):
    """결제 섹션 렌더링"""
    user_id = st.session_state.get('user_id', '')
    user_email = st.session_state.get('user_email', '')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'''
            <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 16px; padding: 2rem; text-align: center; color: white;">
                <div style="font-size: 1rem; opacity: 0.9;">Premium Plan</div>
                <div style="font-size: 3rem; font-weight: 700; margin: 0.5rem 0;">${scenario.price}</div>
                <div style="opacity: 0.8;">일회성 결제 · 평생 이용</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            ### ✨ Premium 혜택
            - ✅ **AI 문서 자동 생성**
            - ✅ **전문가 수준 서류 작성**
            - ✅ **ZIP 패키지 다운로드**
            - ✅ **무제한 수정 & 재생성**
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not payment_service.is_stripe_connected():
        st.warning("⚠️ 테스트 모드")
        if st.button("🧪 테스트 결제 (무료)", type="primary", use_container_width=True):
            st.session_state.is_paid = True
            st.success("🎉 테스트 결제 완료!")
            st.rerun()
        return
    
    # 결제 방식 탭
    tab_embedded, tab_redirect = st.tabs(["💳 이 페이지에서 결제", "🔗 새 페이지에서 결제"])
    
    with tab_embedded:
        st.markdown("##### Embedded Checkout")
        st.caption("페이지 이동 없이 바로 결제할 수 있습니다.")
        
        if 'checkout_client_secret' not in st.session_state:
            if st.button("결제 폼 불러오기", key="load_embedded", use_container_width=True):
                with st.spinner("결제 폼 준비 중..."):
                    client_secret = payment_service.create_embedded_checkout_session(user_id, user_email)
                    if client_secret:
                        st.session_state.checkout_client_secret = client_secret
                        st.rerun()
                    else:
                        st.error("결제 세션 생성 실패. '새 페이지에서 결제'를 이용해주세요.")
        else:
            st.markdown('<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; text-align: center;"><span style="font-size: 0.85rem; color: #64748b;">🔒 Stripe 보안 결제</span></div>', unsafe_allow_html=True)
            
            payment_service.render_embedded_checkout(st.session_state.checkout_client_secret)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ 결제 완료 확인", use_container_width=True, type="primary"):
                    session_id = st.session_state.get('pending_checkout_session_id', '')
                    if session_id:
                        status = payment_service.check_session_status(session_id)
                        if status == 'complete':
                            is_paid, payment_info = payment_service.verify_payment(session_id)
                            if is_paid:
                                payment_service.record_payment_to_db(user_id, payment_info)
                                st.success("🎉 결제 완료!")
                                if 'checkout_client_secret' in st.session_state:
                                    del st.session_state.checkout_client_secret
                                st.rerun()
                        elif status == 'open':
                            st.warning("결제가 아직 완료되지 않았습니다.")
                        else:
                            st.error(f"세션 상태: {status}")
            with col2:
                if st.button("🔄 새로고침", use_container_width=True):
                    if 'checkout_client_secret' in st.session_state:
                        del st.session_state.checkout_client_secret
                    st.rerun()
    
    with tab_redirect:
        st.markdown("##### Redirect Checkout")
        st.caption("Stripe 결제 페이지로 이동합니다. 결제 완료 후 돌아옵니다.")
        
        if st.button("💳 결제 페이지로 이동", type="primary", use_container_width=True, key="redirect_pay"):
            with st.spinner("결제 페이지 생성 중..."):
                checkout_url, session_id = payment_service.create_checkout_session(user_id, user_email)
            
            if checkout_url:
                st.session_state.checkout_session_id = session_id
                st.markdown(f'''
                    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem; text-align: center; margin-top: 1rem;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔗</div>
                        <a href="{checkout_url}" target="_blank" style="color: #2563eb; font-weight: 600; font-size: 1.1rem;">결제 페이지 열기 (클릭)</a>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.5rem;">결제 완료 후 아래 버튼으로 확인</div>
                    </div>
                ''', unsafe_allow_html=True)
        
        session_id = st.session_state.get('checkout_session_id', '')
        if session_id:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ 결제 완료 확인", use_container_width=True, key="verify_redirect"):
                is_paid, payment_info = payment_service.verify_payment(session_id)
                if is_paid:
                    payment_service.record_payment_to_db(user_id, payment_info)
                    st.success("🎉 결제 완료!")
                    st.rerun()
                else:
                    st.warning("결제가 아직 완료되지 않았습니다.")