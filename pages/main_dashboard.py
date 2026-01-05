"""
K-Stay Main Dashboard
결제 없이 시나리오 시작 가능, Phase 4에서 결제
with i18n support + K-ETA Tab

Fixed Issues:
1. Tab selection persistence using session_state with styled buttons (no :has selector)
2. Header colors properly set with -webkit-text-fill-color
3. Coming soon card height matched with min-height
"""

import streamlit as st
from services.payment_service import PaymentService
from utils.i18n import t, get_current_language
from utils.scroll import scroll_to_top


def render():
    """메인 대시보드 렌더링"""
    
    # 페이지 진입 시 스크롤 맨 위로
    scroll_to_top()

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
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; margin: 0 0 1rem 0;">
                {t('dashboard.what_help')}
            </p>
            <div style="display: flex; gap: 2rem;">
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">{t('dashboard.nationality')}: <b style="color: white;">{nationality}</b></span>
                <span style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">{t('dashboard.passport')}: <b style="color: white;">{passport_masked}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    
    current_lang = get_current_language()
    
    # 탭 라벨 정의
    keta_label = "🛫 K-ETA"
    visa_label = "📋 Visa Documents" if current_lang == "en" else "📋 비자 서류"
    
    # Streamlit 기본 탭 사용
    tab_keta, tab_visa = st.tabs([keta_label, visa_label])
    
    with tab_keta:
        render_keta_tab()
    
    with tab_visa:
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
    
    # 헤더 - 명시적 색상 지정
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin: 1.5rem 0;">
            <span style="font-size: 1.5rem;">📋</span>
            <h2 style="font-size: 1.25rem; font-weight: 700; color: #1e293b !important; margin: 0; -webkit-text-fill-color: #1e293b !important;">
                {t('dashboard.scenario_select')}
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Track 1 - 유학생/취업준비
    st.markdown(f'<div style="background: #f1f5f9; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #475569;">💼 TRACK 1 — {t("dashboard.track1")}</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        render_scenario_card("💼", "#fef3c7", t("scenarios.job_search"), "D-10", t("scenarios.job_search_desc"), 3, "A")
    with col2:
        render_scenario_card("⏰", "#fce7f3", t("scenarios.part_time"), t("scenarios.part_time"), t("scenarios.part_time_desc"), 3, "B")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 2 - 고마진
    st.markdown(f'<div style="background: #fef3c7; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #92400e;">💎 TRACK 2 — {t("dashboard.track2")}</span></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        render_scenario_card("👨‍👩‍👧", "#d1fae5", t("scenarios.family_invite"), "F-1-5", t("scenarios.family_invite_desc"), 3, "D")
    with col4:
        render_scenario_card("🏥", "#e0f2fe", t("scenarios.medical"), "C-3-3/G-1-10", t("scenarios.medical_desc"), 3, "G")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track 3 - 국적 귀화
    st.markdown(f'<div style="background: #e0e7ff; display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; margin-bottom: 1rem;"><span style="font-size: 0.8rem; font-weight: 600; color: #3730a3;">🔄 TRACK 3 — {t("dashboard.track3")}</span></div>', unsafe_allow_html=True)
    
    col5, col6 = st.columns(2)
    with col5:
        render_scenario_card("🏛️", "#fef3c7", t("scenarios.naturalization"), t("scenarios.naturalization"), t("scenarios.naturalization_desc"), 2, "F")
    with col6:
        render_coming_soon_card()


def render_keta_tab():
    """K-ETA 탭 렌더링 - 편안한 UI/UX 디자인"""
    current_lang = get_current_language()
    
    # 다국어 텍스트 정의
    texts = get_keta_texts(current_lang)
    
    # =========================================================================
    # 섹션 1: 부드러운 헤더 카드
    # =========================================================================
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdfa 100%);
            border: 1px solid #bae6fd;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="
                    width: 56px; height: 56px;
                    background: linear-gradient(135deg, #38bdf8, #0ea5e9);
                    border-radius: 16px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.75rem;
                    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25);
                ">✈️</div>
                <div>
                    <h2 style="font-size: 1.4rem; font-weight: 700; color: #0c4a6e !important; margin: 0; -webkit-text-fill-color: #0c4a6e;">{texts['intro_title']}</h2>
                    <p style="font-size: 0.85rem; color: #0369a1 !important; margin: 0.25rem 0 0 0; -webkit-text-fill-color: #0369a1;">Korea Electronic Travel Authorization</p>
                </div>
            </div>
            <p style="color: #475569 !important; margin: 0; font-size: 0.95rem; line-height: 1.7; -webkit-text-fill-color: #475569;">{texts['intro_text']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # =========================================================================
    # 섹션 2: 핵심 정보 카드 (3열)
    # =========================================================================
    col1, col2, col3 = st.columns(3)
    
    info_cards = [
        ("💰", texts['fee_title'], texts['fee_value'], texts['fee_note'], "#fefce8", "#ca8a04", "#fef9c3"),
        ("⏱️", texts['time_title'], texts['time_value'], texts['time_note'], "#f0fdf4", "#16a34a", "#dcfce7"),
        ("📅", texts['valid_title'], texts['valid_value'], texts['valid_note'], "#eff6ff", "#2563eb", "#dbeafe"),
    ]
    
    for col, (icon, title, value, note, bg, color, icon_bg) in zip([col1, col2, col3], info_cards):
        with col:
            st.markdown(f"""
                <div style="
                    background: {bg};
                    border-radius: 16px;
                    padding: 1.25rem;
                    text-align: center;
                    height: 100%;
                    border: 1px solid {icon_bg};
                ">
                    <div style="
                        width: 48px; height: 48px;
                        background: {icon_bg};
                        border-radius: 12px;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 1.5rem;
                        margin: 0 auto 0.75rem auto;
                    ">{icon}</div>
                    <p style="font-size: 0.8rem; color: #64748b !important; margin: 0; -webkit-text-fill-color: #64748b;">{title}</p>
                    <p style="font-size: 1.25rem; font-weight: 700; color: {color} !important; margin: 0.25rem 0; -webkit-text-fill-color: {color};">{value}</p>
                    <p style="font-size: 0.75rem; color: #94a3b8 !important; margin: 0; -webkit-text-fill-color: #94a3b8;">{note}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # =========================================================================
    # 섹션 3: 자격 확인 + 바로가기 (2열, 고정 높이)
    # =========================================================================
    col_left, col_right = st.columns([1.2, 0.8], gap="large")
    
    with col_left:
        # 자격 확인 카드 (고정 높이 컨테이너)
        st.markdown(f"""
            <div style="
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                min-height: 180px;
            ">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                    <div style="
                        width: 40px; height: 40px;
                        background: linear-gradient(135deg, #a78bfa, #8b5cf6);
                        border-radius: 10px;
                        display: flex; align-items: center; justify-content: center;
                        font-size: 1.25rem;
                    ">🔍</div>
                    <div>
                        <h3 style="font-size: 1.1rem; font-weight: 600; color: #1e293b !important; margin: 0; -webkit-text-fill-color: #1e293b;">{texts['check_title']}</h3>
                        <p style="font-size: 0.8rem; color: #64748b !important; margin: 0; -webkit-text-fill-color: #64748b;">{texts['check_desc']}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        nationality_input = st.text_input(
            texts['nationality_label'], 
            placeholder="USA, Japan, Germany, China...", 
            key="keta_nationality",
            label_visibility="collapsed"
        )
        
        check_clicked = st.button(f"🔍 {texts['check_btn']}", key="check_keta", type="primary", use_container_width=True)
    
    with col_right:
        # 바로가기 카드 (고정 높이)
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border: 1px solid #a7f3d0;
                border-radius: 16px;
                padding: 1.5rem;
                text-align: center;
                min-height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🌐</div>
                <p style="font-size: 0.9rem; font-weight: 600; color: #065f46 !important; margin: 0 0 1rem 0; -webkit-text-fill-color: #065f46;">{texts['official_title']}</p>
                <a href="https://www.k-eta.go.kr" target="_blank" style="
                    display: inline-block;
                    background: #10b981;
                    color: white !important;
                    text-decoration: none;
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    font-weight: 600;
                    font-size: 0.9rem;
                    transition: all 0.2s;
                ">{texts['official_btn']} ↗</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # AI 상담 버튼
        if st.button(f"💬 {texts['ai_chat_btn']}", key="keta_ai_chat", use_container_width=True):
            st.session_state.current_page = 'ai_chat'
            st.session_state.ai_chat_preset = "K-ETA에 대해 알려주세요" if current_lang == "ko" else "Tell me about K-ETA"
            st.rerun()
    
    # =========================================================================
    # 섹션 3-1: 자격 확인 결과 (컬럼 밖에서 전체 너비로 표시)
    # =========================================================================
    if check_clicked:
        if nationality_input:
            result = check_keta_eligibility(nationality_input)
            if result["eligible"]:
                st.success(f"✅ {result['message']}")
                st.info(f"💡 {result['note']}")
            else:
                st.error(f"❌ {result['message']}")
                st.warning(f"💡 {result['note']}")
        else:
            st.warning(texts['enter_nationality'])
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # =========================================================================
    # 섹션 4: 신청 절차 (원본 디자인 - 3열 × 2행)
    # =========================================================================
    st.markdown("---")
    st.markdown(f"<h3 style='font-size: 1.2rem; font-weight: 700; color: #1e293b;'>{texts['steps_title']}</h3>", unsafe_allow_html=True)
    
    steps_full = texts['steps_full']
    cols = st.columns(3)
    for i, step in enumerate(steps_full):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="
                    background: white; 
                    border: 1px solid #e2e8f0; 
                    border-radius: 0.75rem; 
                    padding: 1rem; 
                    margin-bottom: 1rem; 
                    min-height: 80px;
                    display: flex;
                    align-items: center;
                    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                ">
                    <p style="margin: 0; font-size: 0.9rem; font-weight: 500; color: #475569 !important; -webkit-text-fill-color: #475569 !important; line-height: 1.4;">{step}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # =========================================================================
    # 섹션 5: 제외 대상 & 비교 (원본 디자인)
    # =========================================================================
    st.markdown("---")
    col_exempt, col_compare = st.columns(2, gap="large")
    
    with col_exempt:
        st.markdown(f"<h3 style='font-size: 1.1rem; font-weight: 700; color: #1e293b;'>{texts['exempt_title']}</h3>", unsafe_allow_html=True)
        list_html = "".join([f"<li style='margin-bottom: 0.5rem; color: #475569;'>{item}</li>" for item in texts['exempt_list']])
        st.markdown(f"""
            <ul style="padding-left: 1.25rem; margin-top: 0.5rem;">
                {list_html}
            </ul>
        """, unsafe_allow_html=True)
    
    with col_compare:
        st.markdown(f"<h3 style='font-size: 1.1rem; font-weight: 700; color: #1e293b;'>{texts['compare_title']}</h3>", unsafe_allow_html=True)
        if current_lang == "ko":
            st.markdown("""
| 구분 | K-ETA | 비자 (VISA) |
|:---:|:---:|:---:|
| **대상** | 112개국 (무비자) | 모든 국가 |
| **목적** | 관광/단기 방문 | 유학/취업/장기 |
| **신청** | 온라인 (간편) | 재외공관 방문 |
| **비용** | 1만원 | 비자별 상이 |
            """)
        else:
            st.markdown("""
| Category | K-ETA | VISA |
|:---:|:---:|:---:|
| **Target** | 112 countries | All countries |
| **Purpose** | Tourism/Short | Long/Work/Study |
| **Apply** | Online | Embassy |
| **Fee** | ~$10 | Varies |
            """)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # =========================================================================
    # 섹션 6: 주의사항 (부드러운 경고)
    # =========================================================================
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 1px solid #fcd34d;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            display: flex;
            gap: 0.75rem;
            align-items: center;
            margin-top: 0.5rem;
        ">
            <div style="font-size: 1.25rem;">💡</div>
            <div>
                <p style="margin: 0; font-weight: 600; color: #92400e !important; font-size: 0.9rem; -webkit-text-fill-color: #92400e;">{texts['warning_title']}</p>
                <p style="margin: 0.25rem 0 0 0; color: #a16207 !important; font-size: 0.85rem; -webkit-text-fill-color: #a16207;">{texts['warning_text']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def get_keta_texts(lang: str) -> dict:
    """K-ETA 다국어 텍스트 반환"""
    if lang == "ko":
        return {
            "intro_title": "K-ETA란?",
            "intro_text": "K-ETA는 무비자 협정국 국민이 한국 입국 전 온라인으로 받는 전자여행허가입니다. 비자가 아니며, 관광·단기방문(90일 이내) 목적으로 한국을 방문할 때 필요합니다.",
            "fee_title": "수수료",
            "fee_value": "₩10,000",
            "fee_note": "약 $9 (+ 카드수수료)",
            "time_title": "처리 시간",
            "time_value": "72시간",
            "time_note": "통상 24시간 내 완료",
            "valid_title": "유효기간",
            "valid_value": "3년",
            "valid_note": "복수 입국 가능",
            "check_title": "K-ETA 자격 확인",
            "check_desc": "국적을 입력해 신청 가능 여부를 확인하세요",
            "nationality_label": "국적 입력",
            "check_btn": "자격 확인",
            "enter_nationality": "국적을 입력해주세요",
            "official_title": "공식 신청 사이트",
            "official_btn": "바로가기",
            "ai_chat_btn": "AI 상담",
            "steps_title": "신청 절차",
            "steps_full": [
                "1️⃣ 공식 사이트 접속 (www.k-eta.go.kr)",
                "2️⃣ 약관 동의 및 회원가입",
                "3️⃣ 여권정보 입력",
                "4️⃣ 신청정보 입력",
                "5️⃣ 수수료 결제 (VISA/MASTER 등)",
                "6️⃣ 결과 확인 (72시간 이내)"
            ],
            "exempt_title": "🚫 K-ETA 제외 대상",
            "exempt_list": ["비자(VISA) 소지자", "외국인등록증 소지자", "17세 이하, 65세 이상", "복수국적자 (한국여권 소지)", "ABTC 소지자 (미국/캐나다 제외)", "환승객 (입국심사 미통과 시)"],
            "compare_title": "📊 K-ETA vs 비자 비교",
            "warning_title": "공식 사이트만 이용하세요",
            "warning_text": "www.k-eta.go.kr 외 사이트에서 고액 수수료를 부과하는 사례가 있습니다."
        }
    else:
        return {
            "intro_title": "What is K-ETA?",
            "intro_text": "K-ETA is an electronic travel authorization for citizens of visa-waiver countries visiting Korea. It's required for tourism and short visits (under 90 days), not a visa.",
            "fee_title": "Fee",
            "fee_value": "~$10",
            "fee_note": "KRW 10,000 + card fee",
            "time_title": "Processing",
            "time_value": "72 hrs",
            "time_note": "Usually within 24 hrs",
            "valid_title": "Validity",
            "valid_value": "3 years",
            "valid_note": "Multiple entries",
            "check_title": "Check Eligibility",
            "check_desc": "Enter your nationality to verify",
            "nationality_label": "Enter Nationality",
            "check_btn": "Check",
            "enter_nationality": "Please enter your nationality",
            "official_title": "Official Website",
            "official_btn": "Visit",
            "ai_chat_btn": "AI Chat",
            "steps_title": "Application Steps",
            "steps_full": [
                "1️⃣ Visit official site (www.k-eta.go.kr)",
                "2️⃣ Agree to terms & register",
                "3️⃣ Enter passport information",
                "4️⃣ Fill in application details",
                "5️⃣ Pay fee (VISA/MASTER/JCB/AMEX)",
                "6️⃣ Check result (within 72 hours)"
            ],
            "exempt_title": "🚫 K-ETA Exemptions",
            "exempt_list": ["VISA holders", "Alien Registration Card holders", "Under 17 or over 65 years old", "Dual citizens (with Korean passport)", "ABTC holders (except US/Canada)", "Transit passengers (not passing immigration)"],
            "compare_title": "📊 K-ETA vs VISA Comparison",
            "warning_title": "Use Official Site Only",
            "warning_text": "Only www.k-eta.go.kr is official. Beware of fake sites charging high fees."
        }


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
    """시나리오 카드 - 고정 높이"""
    
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 0.5rem;
            min-height: 220px;
        ">
            <div style="width: 40px; height: 40px; background: {icon_bg}; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 0.75rem;">{icon}</div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #1e293b !important; margin: 0 0 0.25rem 0; -webkit-text-fill-color: #1e293b !important;">{title}</h3>
            <p style="font-size: 0.8rem; color: #2563eb !important; margin: 0 0 0.5rem 0; font-weight: 500; -webkit-text-fill-color: #2563eb !important;">{visa_type}</p>
            <p style="font-size: 0.85rem; color: #64748b !important; margin: 0 0 0.75rem 0; -webkit-text-fill-color: #64748b !important;">{description}</p>
            <div style="display: inline-block; background: #dbeafe; color: #1e40af !important; font-size: 0.75rem; font-weight: 500; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">📄 {doc_count} {t('dashboard.documents')}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🚀 {t('dashboard.start_btn')}", key=f"start_{key}", use_container_width=True, type="primary"):
        start_scenario(key)


def render_coming_soon_card():
    """준비 중 카드 - 시나리오 카드와 동일 높이"""
    current_lang = get_current_language()
    
    coming_soon_title = "준비 중" if current_lang == "ko" else "Coming Soon"
    coming_soon_desc = "새로운 시나리오가 곧 추가됩니다" if current_lang == "ko" else "New scenarios coming soon"
    coming_soon_btn = "🔒 준비 중" if current_lang == "ko" else "🔒 Coming Soon"
    
    # 시나리오 카드와 동일한 구조 (태그 포함)
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 2px dashed #cbd5e1;
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 0.5rem;
            min-height: 220px;
        ">
            <div style="width: 40px; height: 40px; background: #e2e8f0; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; margin-bottom: 0.75rem;">🔜</div>
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #94a3b8 !important; margin: 0 0 0.25rem 0; -webkit-text-fill-color: #94a3b8 !important;">{coming_soon_title}</h3>
            <p style="font-size: 0.8rem; color: #94a3b8 !important; margin: 0 0 0.5rem 0; font-weight: 500; -webkit-text-fill-color: #94a3b8 !important;">Coming Soon</p>
            <p style="font-size: 0.85rem; color: #94a3b8 !important; margin: 0 0 0.75rem 0; -webkit-text-fill-color: #94a3b8 !important;">{coming_soon_desc}</p>
            <div style="display: inline-block; background: #e2e8f0; color: #94a3b8 !important; font-size: 0.75rem; font-weight: 500; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">🔒 준비 중</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.button(coming_soon_btn, disabled=True, use_container_width=True)


def start_scenario(scenario_id: str):
    """시나리오 시작 - 결제 없이 바로 시작"""
    st.session_state.selected_scenario = scenario_id
    st.session_state.current_page = 'scenario_form'
    st.session_state.form_step = 1
    st.rerun()