"""
결제 테스트 페이지
"""
import streamlit as st

st.title("결제 테스트")

# 상태 표시
st.write("현재 dashboard_mode:", st.session_state.get('dashboard_mode', 'scenarios'))
st.write("현재 is_paid:", st.session_state.get('is_paid', False))

st.markdown("---")

# 테스트 버튼 1: 결제 페이지로 전환
if st.button("1. 결제 페이지로 이동"):
    st.session_state.dashboard_mode = 'payment'
    st.write("✅ dashboard_mode를 'payment'로 변경했습니다")
    st.rerun()

# 테스트 버튼 2: 시나리오 페이지로 전환
if st.button("2. 시나리오 페이지로 이동"):
    st.session_state.dashboard_mode = 'scenarios'
    st.write("✅ dashboard_mode를 'scenarios'로 변경했습니다")
    st.rerun()

# 테스트 버튼 3: 결제 완료 처리
if st.button("3. 결제 완료 처리"):
    st.session_state.is_paid = True
    st.write("✅ is_paid를 True로 변경했습니다")
    st.rerun()

# 테스트 버튼 4: 결제 초기화
if st.button("4. 결제 초기화"):
    st.session_state.is_paid = False
    st.session_state.dashboard_mode = 'scenarios'
    st.write("✅ 초기화했습니다")
    st.rerun()

st.markdown("---")

# 현재 모드에 따라 다른 내용 표시
mode = st.session_state.get('dashboard_mode', 'scenarios')

if mode == 'payment':
    st.success("🔒 결제 페이지입니다!")
    st.markdown("## Premium 구매")
    st.write("여기에 결제 내용이 표시됩니다")
else:
    st.info("📋 시나리오 페이지입니다!")
    st.markdown("## 시나리오 선택")
    st.write("여기에 시나리오 목록이 표시됩니다")
