"""
K-Stay Main Dashboard
결제 없이 시나리오 시작 가능, Phase 4에서 결제
with i18n support + K-ETA Tab

Merged Features:
1. Tab Structure (Visa Docs vs K-ETA)
2. Updated Scenario List (Medical added, Marriage/Professional removed)
"""

import streamlit as st
from services.payment_service import PaymentService
from utils.i18n import t, get_current_language


def render():
    """메인 대시보드 렌더링"""
    
    # 결제 콜백 처리
    handle_payment_callback()
    
    user_data = st.session_state.get('user_data', {})
    name = user_data.get('given_name', 'Guest')
    nationality = user_data.get('nationality', '')
    passport = user_data.get('passport_no', '')
    passport_masked = passport[:3] + '****' if passport else ''
    
    # 환영 배너
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
        ">
            <h1 style="font-size: 2rem; font-weight: 700; color: white !important; margin: 0 0 0.5rem 0;">
                {t('dashboard.welcome')}, {name}! 👋
            </h1>
            <p style="color: rgba(255,255,255,0.9) !important; font-size: 1rem; margin: 0 0 1rem 0;">
                {t('dashboard.what_help')}
            </p>
            <div style="display: flex; gap: 2rem;">
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">{t('dashboard.nationality')}: <b style="color: white;">{nationality}</b></span>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">{t('dashboard.passport')}: <b style="color: white;">{passport_masked}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 결제 상태 표시
    is_paid = st.session_state.get('is_paid', False)
    if is_paid:
        st.success(f"✅ {t('dashboard.premium_active')}")
    else:
        st.info(f"💡 {t('dashboard.free_info')}")
    
    # 탭 분리: 비자 서류 vs K-ETA
    current_lang = get_current_language()
    tab_visa = "📋 비자 서류" if current_lang == "ko" else "📋 Visa Documents"
    tab_keta = "🛫 K-ETA" if current_lang == "ko" else "🛫 K-ETA"
    
    # K-ETA를 첫 번째 탭으로 설정하여 기본값이 되도록 변경
    tab1, tab2 = st.tabs([tab_keta, tab_visa])
    
    with tab1:
        # K-ETA 탭
        render_keta_tab()
    
    with tab2:
        # 비자 탭: 업데이트된 시나리오 리스트 (의료관광 포함, 결혼/전문인력 제거)
        render_scenario_list()


def handle_payment_callback():
    """URL 파라미터로 결제 결과 처리"""
    params = st.query_params
    
    if params.get("payment") == "success":
        session_id = params.get("session_id", "")
        payment_service = PaymentService()
        
        success, info = payment_service.verify_payment(session_id)
        if success:
            user_id = st.session_state.get('user_id', '')
            payment_service.record_payment_to_db(user_id, info)
            st.success(f"🎉 {t('dashboard.payment_success')}")
            st.balloons()
        
        st.query_params.clear()
    
    elif params.get("payment") == "cancel":
        st.warning(t('dashboard.payment_cancel'))
        st.query_params.clear()


def render_scenario_list():
    """시나리오 목록 렌더링 - 결혼이민(C), 전문인력(E) 제거, 의료관광(G) 추가"""
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin: 1.5rem 0;">
            <span style="font-size: 1.5rem;">📋</span>
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #1e293b !important; margin: 0;">
                {t('dashboard.scenario_select')}
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Track 1 - 유학생/취업준비
    st.markdown(f'<div style="background: #f1f5f9; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #475569;">💼 TRACK 1 — {t("dashboard.track1")}</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        render_scenario_card("💼", "#fef3c7", t("scenarios.job_search"), "D-10", t("scenarios.job_search_desc"), 5, "A")
    with col2:
        render_scenario_card("⏰", "#fce7f3", t("scenarios.part_time"), t("scenarios.part_time"), t("scenarios.part_time_desc"), 5, "B")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 2 - 고마진 (결혼이민 제거, 가족초청 유지, 의료관광 추가)
    st.markdown(f'<div style="background: #fef3c7; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #92400e;">💎 TRACK 2 — {t("dashboard.track2")}</span></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        # 가족 초청 (D)
        render_scenario_card("👨‍👩‍👧", "#d1fae5", t("scenarios.family_invite"), "F-1-5", t("scenarios.family_invite_desc"), 4, "D")
    with col4:
        # 의료 관광 (G) - 새로 추가
        render_scenario_card("🏥", "#e0f2fe", t("scenarios.medical"), "C-3-3/G-1-10", t("scenarios.medical_desc"), 3, "G")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 3 - 국적 귀화 (전문인력 제거)
    st.markdown(f'<div style="background: #e0e7ff; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #3730a3;">🔄 TRACK 3 — {t("dashboard.track3")}</span></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        # 국적 귀화 (F)
        render_scenario_card("🏛️", "#fef3c7", t("scenarios.naturalization"), t("scenarios.naturalization"), t("scenarios.naturalization_desc"), 4, "F")
    with col6:
        # 빈 카드 또는 "준비 중" 표시
        render_coming_soon_card()


def render_keta_tab():
    """K-ETA 탭 렌더링"""
    current_lang = get_current_language()
    
    # K-ETA 소개 텍스트 및 UI 요소 정의
    if current_lang == "ko":
        intro_title = "K-ETA (전자여행허가)란?"
        intro_text = "K-ETA는 무비자 협정국 국민이 한국 입국 전 온라인으로 받는 여행허가입니다. 비자가 아니며, 관광·단기방문(90일 이내) 목적에 적용됩니다."
        check_title = "🔍 K-ETA 자격 확인"
        check_desc = "국적을 입력하면 K-ETA 신청 가능 여부를 확인할 수 있습니다."
        nationality_label = "국적 입력"
        check_btn = "자격 확인"
        guide_title = "📝 K-ETA 신청 가이드"
        official_btn = "🌐 K-ETA 공식 홈페이지 바로가기"
        fee_title = "💰 수수료"
        fee_text = "10,000원 (약 $9~10) + 카드수수료 3%"
        time_title = "⏱️ 심사 시간"
        time_text = "통상 72시간 이내 (급행 서비스 없음)"
        valid_title = "📅 유효기간"
        valid_text = "3년간 유효, 반복 입국 가능"
        steps_title = "신청 절차"
        step1 = "1️⃣ 공식 사이트 접속 (www.k-eta.go.kr)"
        step2 = "2️⃣ 약관 동의 및 회원가입"
        step3 = "3️⃣ 여권정보 입력"
        step4 = "4️⃣ 신청정보 입력"
        step5 = "5️⃣ 수수료 결제 (VISA/MASTER/JCB/AMEX)"
        step6 = "6️⃣ 결과 확인 (72시간 이내)"
        exempt_title = "🚫 K-ETA 제외 대상"
        exempt_list = ["비자(VISA) 소지자", "외국인등록증 소지자", "17세 이하, 65세 이상", "복수국적자 (한국여권 소지)", "ABTC 소지자 (미국/캐나다 제외)", "환승객 (입국심사 미통과 시)"]
        compare_title = "📊 K-ETA vs 비자 비교"
        warning_title = "⚠️ 주의사항"
        warning_text = "www.k-eta.go.kr만이 공식 사이트입니다. 유사 사이트에서 고액 수수료를 부과하는 사례가 있으니 주의하세요!"
        ai_chat_btn = "💬 K-ETA 관련 AI 상담하기"
    else:
        intro_title = "What is K-ETA?"
        intro_text = "K-ETA is an electronic travel authorization for visa-waiver countries. It's not a visa and applies to tourism/short visits (under 90 days)."
        check_title = "🔍 Check K-ETA Eligibility"
        check_desc = "Enter your nationality to check if you can apply for K-ETA."
        nationality_label = "Enter Nationality"
        check_btn = "Check Eligibility"
        guide_title = "📝 K-ETA Application Guide"
        official_btn = "🌐 Go to Official K-ETA Website"
        fee_title = "💰 Fee"
        fee_text = "10,000 KRW (~$9~10) + 3% card fee"
        time_title = "⏱️ Processing Time"
        time_text = "Usually within 72 hours (no express service)"
        valid_title = "📅 Validity"
        valid_text = "Valid for 3 years, multiple entries allowed"
        steps_title = "Application Steps"
        step1 = "1️⃣ Visit official site (www.k-eta.go.kr)"
        step2 = "2️⃣ Agree to terms & register"
        step3 = "3️⃣ Enter passport information"
        step4 = "4️⃣ Fill in application details"
        step5 = "5️⃣ Pay fee (VISA/MASTER/JCB/AMEX)"
        step6 = "6️⃣ Check result (within 72 hours)"
        exempt_title = "🚫 K-ETA Exemptions"
        exempt_list = ["VISA holders", "Alien Registration Card holders", "Under 17 or over 65 years old", "Dual citizens (with Korean passport)", "ABTC holders (except US/Canada)", "Transit passengers (not passing immigration)"]
        compare_title = "📊 K-ETA vs VISA Comparison"
        warning_title = "⚠️ Warning"
        warning_text = "Only www.k-eta.go.kr is the official site. Beware of fake sites charging excessive fees!"
        ai_chat_btn = "💬 AI Chat about K-ETA"
    
    # K-ETA 소개 카드
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        ">
            <h2 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.3rem;">🛫 {intro_title}</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;">{intro_text}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # K-ETA 자격 확인
        st.markdown(f"### {check_title}")
        st.caption(check_desc)
        
        nationality_input = st.text_input(nationality_label, placeholder="USA, Japan, Germany...", key="keta_nationality")
        
        if st.button(check_btn, key="check_keta", type="primary", use_container_width=True):
            if nationality_input:
                result = check_keta_eligibility(nationality_input)
                if result["eligible"]:
                    st.success(f"✅ {result['message']}")
                    st.info(f"💡 {result['note']}")
                else:
                    st.error(f"❌ {result['message']}")
                    st.warning(f"💡 {result['note']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 공식 홈페이지 바로가기
        st.markdown(f"""
            <a href="https://www.k-eta.go.kr" target="_blank" style="
                display: block;
                background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                color: white;
                text-decoration: none;
                padding: 1rem;
                border-radius: 0.75rem;
                text-align: center;
                font-weight: 600;
                font-size: 1rem;
                margin-bottom: 1rem;
            ">{official_btn}</a>
        """, unsafe_allow_html=True)
        
        # AI 상담 버튼
        if st.button(ai_chat_btn, key="keta_ai_chat", use_container_width=True):
            st.session_state.current_page = 'ai_chat'
            st.session_state.ai_chat_preset = "K-ETA에 대해 알려주세요" if current_lang == "ko" else "Tell me about K-ETA"
            st.rerun()
    
    with col2:
        # 주요 정보 카드
        st.markdown(f"### {guide_title}")
        
        info_cards = [
            (fee_title, fee_text, "#fef3c7", "#92400e"),
            (time_title, time_text, "#dbeafe", "#1e40af"),
            (valid_title, valid_text, "#dcfce7", "#166534"),
        ]
        
        for title, text, bg, color in info_cards:
            st.markdown(f"""
                <div style="background: {bg}; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 0.5rem;">
                    <p style="margin: 0; font-weight: 600; color: {color}; font-size: 0.85rem;">{title}</p>
                    <p style="margin: 0.25rem 0 0 0; color: {color}; font-size: 0.8rem;">{text}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # 신청 절차
    st.markdown("---")
    st.markdown(f"### {steps_title}")
    
    steps = [step1, step2, step3, step4, step5, step6]
    cols = st.columns(3)
    for i, step in enumerate(steps):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.5rem; padding: 0.75rem; margin-bottom: 0.5rem; min-height: 60px;">
                    <p style="margin: 0; font-size: 0.8rem; color: #475569;">{step}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # 제외 대상 & 비교
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"### {exempt_title}")
        for item in exempt_list:
            st.markdown(f"• {item}")
    
    with col4:
        st.markdown(f"### {compare_title}")
        if current_lang == "ko":
            st.markdown("""
            | 구분 | K-ETA | 비자 |
            |------|-------|------|
            | 대상 | 112개국 | 모든 국가 |
            | 목적 | 관광/단기 | 장기/취업/유학 |
            | 신청 | 온라인 | 대사관 |
            | 비용 | 1만원 | 비자별 상이 |
            | 기간 | 72시간 | 수일~수주 |
            """)
        else:
            st.markdown("""
            | Category | K-ETA | VISA |
            |----------|-------|------|
            | Target | 112 countries | All countries |
            | Purpose | Tourism/Short | Long/Work/Study |
            | Apply | Online | Embassy |
            | Fee | ~$10 | Varies |
            | Time | 72 hours | Days~Weeks |
            """)
    
    # 주의사항
    st.markdown("---")
    st.markdown(f"""
        <div style="background: #fef2f2; border: 1px solid #ef4444; border-radius: 0.75rem; padding: 1rem;">
            <p style="margin: 0; font-weight: 600; color: #dc2626;">{warning_title}</p>
            <p style="margin: 0.5rem 0 0 0; color: #b91c1c; font-size: 0.9rem;">{warning_text}</p>
        </div>
    """, unsafe_allow_html=True)


def check_keta_eligibility(nationality: str) -> dict:
    """K-ETA 자격 확인"""
    current_lang = get_current_language()
    
    # K-ETA 대상 국가 목록
    keta_countries = [
        "usa", "united states", "미국", "uk", "united kingdom", "영국", "japan", "일본",
        "canada", "캐나다", "australia", "호주", "germany", "독일", "france", "프랑스",
        "italy", "이탈리아", "spain", "스페인", "netherlands", "네덜란드", "belgium", "벨기에",
        "switzerland", "스위스", "sweden", "스웨덴", "norway", "노르웨이", "denmark", "덴마크",
        "finland", "핀란드", "austria", "오스트리아", "ireland", "아일랜드", "portugal", "포르투갈",
        "greece", "그리스", "poland", "폴란드", "czech", "czechia", "체코", "hungary", "헝가리",
        "singapore", "싱가포르", "taiwan", "대만", "hong kong", "홍콩", "malaysia", "말레이시아",
        "thailand", "태국", "brazil", "브라질", "mexico", "멕시코", "argentina", "아르헨티나",
        "chile", "칠레", "new zealand", "뉴질랜드", "russia", "러시아", "turkey", "터키", "türkiye",
        "israel", "이스라엘", "uae", "united arab emirates", "아랍에미리트",
        "saudi arabia", "사우디아라비아", "qatar", "카타르", "kuwait", "쿠웨이트",
        "bahrain", "바레인", "oman", "오만"
    ]
    
    nationality_lower = nationality.lower().strip()
    
    is_eligible = any(country in nationality_lower or nationality_lower in country for country in keta_countries)
    
    if is_eligible:
        if current_lang == "ko":
            return {
                "eligible": True,
                "message": f"{nationality}은(는) K-ETA 신청 가능 국가입니다!",
                "note": "2024년 12월 31일까지 일부 국가는 K-ETA가 한시적으로 면제될 수 있습니다. 공식 홈페이지에서 확인하세요."
            }
        else:
            return {
                "eligible": True,
                "message": f"{nationality} is eligible for K-ETA!",
                "note": "Some countries may have temporary K-ETA exemption until Dec 31, 2024. Please check the official website."
            }
    else:
        if current_lang == "ko":
            return {
                "eligible": False,
                "message": f"{nationality}은(는) K-ETA 대상 국가가 아닙니다.",
                "note": "대한민국 대사관/영사관에서 비자(VISA)를 신청하세요."
            }
        else:
            return {
                "eligible": False,
                "message": f"{nationality} is not eligible for K-ETA.",
                "note": "Please apply for a VISA at the Korean Embassy/Consulate."
            }


def render_scenario_card(icon, icon_bg, title, visa_type, description, doc_count, key):
    """시나리오 카드"""
    
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 0.5rem;
        ">
            <div style="width: 40px; height: 40px; background: {icon_bg}; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 0.75rem;">{icon}</div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">{title}</h3>
            <p style="font-size: 0.8rem; color: #2563eb; margin: 0 0 0.5rem 0; font-weight: 500;">{visa_type}</p>
            <p style="font-size: 0.85rem; color: #64748b; margin: 0 0 0.75rem 0;">{description}</p>
            <div style="display: inline-block; background: #dbeafe; color: #1e40af; font-size: 0.75rem; font-weight: 500; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">📄 {doc_count} {t('dashboard.documents')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🚀 {t('dashboard.start_btn')}", key=f"start_{key}", use_container_width=True, type="primary"):
        start_scenario(key)


def render_coming_soon_card():
    """준비 중 카드 (빈 슬롯용)"""
    
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 2px dashed #cbd5e1;
            border-radius: 0.75rem;ㄱ
            padding: 1.25rem;
            margin-bottom: 0.5rem;
            text-align: center;
        ">
            <div style="width: 40px; height: 40px; background: #e2e8f0; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin: 0 auto 0.75rem auto;">🔜</div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #94a3b8; margin: 0 0 0.25rem 0;">준비 중</h3>
            <p style="font-size: 0.8rem; color: #94a3b8; margin: 0 0 0.5rem 0; font-weight: 500;">Coming Soon</p>
            <p style="font-size: 0.85rem; color: #94a3b8; margin: 0 0 0.75rem 0;">새로운 시나리오가 곧 추가됩니다</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.button("🔒 준비 중", disabled=True, use_container_width=True)


def start_scenario(scenario_id: str):
    """시나리오 시작 - 결제 없이 바로 시작"""
    st.session_state.selected_scenario = scenario_id
    st.session_state.current_page = 'scenario_form'
    st.session_state.form_step = 1
    st.rerun()