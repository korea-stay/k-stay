"""
K-Stay Configuration Settings
"""

import streamlit as st
from dataclasses import dataclass
from typing import Optional, Dict, Any

# =============================================================================
# 🔑 API KEYS & SECRETS (Streamlit Secrets에서 로드)
# =============================================================================

def get_secret(key: str, default: str = "") -> str:
    """Streamlit secrets에서 값을 안전하게 가져옴"""
    try:
        return st.secrets.get(key, default)
    except:
        return default

# Supabase
SUPABASE_URL = get_secret("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = get_secret("SUPABASE_KEY", "your-supabase-anon-key")

# OpenAI
OPENAI_API_KEY = get_secret("OPENAI_API_KEY", "sk-your-openai-api-key")

# Stripe
STRIPE_API_KEY = get_secret("STRIPE_API_KEY", "sk_test_your-stripe-key")
STRIPE_PRICE_ID = get_secret("STRIPE_PRICE_ID", "price_your-price-id")
STRIPE_SUCCESS_URL = get_secret("STRIPE_SUCCESS_URL", "https://your-app.streamlit.app/?payment=success")
STRIPE_CANCEL_URL = get_secret("STRIPE_CANCEL_URL", "https://your-app.streamlit.app/?payment=cancel")

# =============================================================================
# 📊 시나리오 설정
# =============================================================================

@dataclass
class Scenario:
    id: str
    name: str
    name_en: str
    visa_type: str
    icon: str
    description: str
    track: str  # high_volume, high_margin, recurring
    required_docs: list
    smart_form_fields: list
    ai_prompts: dict
    price: float = 9.99

SCENARIOS: Dict[str, Scenario] = {
    "A": Scenario(
        id="A",
        name="구직 준비",
        name_en="Job Seeking",
        visa_type="D-10",
        icon="💼",
        description="구직 활동을 위한 비자 연장 및 체류자격 변경",
        track="high_volume",
        required_docs=[
            "통합신청서",
            "구직활동계획서",
            "거주숙소제공확인서",
            "신원보증서",
            "제출 체크리스트"
        ],
        smart_form_fields=[
            {"name": "education_level", "label": "최종 학력", "type": "select", 
             "options": ["학사", "석사", "박사", "기타"]},
            {"name": "major", "label": "전공", "type": "text"},
            {"name": "graduation_date", "label": "졸업일", "type": "date"},
            {"name": "certificates", "label": "보유 자격증", "type": "textarea"},
            {"name": "target_industry", "label": "희망 산업", "type": "text"},
            {"name": "target_position", "label": "희망 직무", "type": "text"},
            {"name": "housing_provider_name", "label": "숙소 제공인 성명", "type": "text"},
            {"name": "housing_provider_phone", "label": "숙소 제공인 연락처", "type": "text"},
            {"name": "housing_address", "label": "거주지 주소", "type": "text"},
        ],
        ai_prompts={
            "narrative_field": "job_search_plan",
            "narrative_label": "월별 구직 활동 계획",
            "narrative_placeholder": "향후 6개월간의 구직 활동 계획을 구체적으로 작성해주세요...",
            "validation_prompt": """
                당신은 D-10 비자 구직활동계획서 검토 전문가입니다.
                다음 내용을 검토하고 문제점과 개선점을 제안하세요:
                
                검토 기준:
                1. 구체적인 월별 계획이 있는가?
                2. 목표 기업/산업이 명확한가?
                3. "취업 확정", "내정" 등 D-10에 부적합한 표현이 없는가?
                4. 실현 가능한 계획인가?
                
                문제가 있으면 구체적인 수정 제안을 해주세요.
            """,
            "generation_prompt": """
                다음 정보를 바탕으로 설득력 있는 구직활동계획서를 작성하세요:
                - 학력: {education_level}
                - 전공: {major}
                - 희망 산업: {target_industry}
                - 희망 직무: {target_position}
                
                월별로 구체적인 활동 계획을 포함하고,
                한국에서 구직 활동을 해야 하는 이유를 논리적으로 설명하세요.
            """
        }
    ),
    
    "B": Scenario(
        id="B",
        name="아르바이트",
        name_en="Part-time Work",
        visa_type="시간제 취업",
        icon="⏰",
        description="유학생/연수생 시간제 취업 허가 신청",
        track="high_volume",
        required_docs=[
            "시간제취업 확인서",
            "표준근로계약서",
            "요건 준수 확인서",
            "통합신청서",
            "사업자등록증 사본"
        ],
        smart_form_fields=[
            {"name": "school_name", "label": "학교명", "type": "text"},
            {"name": "student_status", "label": "재학 상태", "type": "select",
             "options": ["재학중", "휴학중", "수료"]},
            {"name": "semester", "label": "현재 학기", "type": "text"},
            {"name": "gpa", "label": "평균 성적 (GPA)", "type": "number"},
            {"name": "employer_name", "label": "고용주 상호", "type": "text"},
            {"name": "employer_business_no", "label": "사업자등록번호", "type": "text"},
            {"name": "employer_representative", "label": "대표자명", "type": "text"},
            {"name": "employer_phone", "label": "고용주 연락처", "type": "text"},
            {"name": "work_address", "label": "근무지 주소", "type": "text"},
            {"name": "hourly_wage", "label": "시급 (원)", "type": "number"},
            {"name": "weekly_hours", "label": "주당 근무시간", "type": "number"},
            {"name": "work_period_start", "label": "근무 시작일", "type": "date"},
            {"name": "work_period_end", "label": "근무 종료일", "type": "date"},
            {"name": "job_description", "label": "담당 업무", "type": "textarea"},
        ],
        ai_prompts={
            "narrative_field": "work_description",
            "narrative_label": "업무 내용 상세",
            "narrative_placeholder": "담당하게 될 업무를 구체적으로 설명해주세요...",
            "validation_prompt": """
                당신은 시간제 취업 허가 서류 검토 전문가입니다.
                다음 내용을 검토하세요:
                
                검토 기준:
                1. 주 20시간 이내인가? (학기중)
                2. 최저임금 이상인가?
                3. 유흥업소 등 금지 업종이 아닌가?
                4. 학업에 지장이 없는 시간대인가?
                
                문제가 있으면 구체적인 수정 제안을 해주세요.
            """
        }
    ),
    
    "C": Scenario(
        id="C",
        name="결혼 이민",
        name_en="Marriage Immigration",
        visa_type="F-6",
        icon="💍",
        description="한국인 배우자와의 결혼을 통한 비자 신청",
        track="high_margin",
        required_docs=[
            "통합신청서",
            "결혼배경 진술서",
            "배우자 초청장",
            "신원보증서",
            "소득요건 면제신청서"
        ],
        smart_form_fields=[
            {"name": "spouse_name", "label": "배우자 성명", "type": "text"},
            {"name": "spouse_resident_no", "label": "배우자 주민등록번호", "type": "text"},
            {"name": "spouse_phone", "label": "배우자 연락처", "type": "text"},
            {"name": "spouse_occupation", "label": "배우자 직업", "type": "text"},
            {"name": "spouse_income", "label": "배우자 연 소득 (만원)", "type": "number"},
            {"name": "marriage_date", "label": "혼인신고일", "type": "date"},
            {"name": "marriage_location", "label": "혼인신고 장소", "type": "text"},
            {"name": "residence_type", "label": "주거 형태", "type": "select",
             "options": ["자가", "전세", "월세", "기타"]},
            {"name": "first_meeting_date", "label": "첫 만남 시기", "type": "date"},
            {"name": "first_meeting_location", "label": "첫 만남 장소", "type": "text"},
        ],
        ai_prompts={
            "narrative_field": "love_story",
            "narrative_label": "교제 과정 및 결혼 배경",
            "narrative_placeholder": "배우자와의 첫 만남부터 결혼까지의 과정을 진솔하게 작성해주세요...",
            "validation_prompt": """
                당신은 F-6 결혼이민 비자 서류 검토 전문가입니다.
                다음 결혼배경 진술 내용을 검토하세요:
                
                검토 기준:
                1. 시간순으로 논리적인가?
                2. 구체적인 에피소드가 있는가?
                3. "위장 결혼", "돈을 받고" 등 의심 표현이 없는가?
                4. 진정성이 느껴지는가?
                
                문제가 있으면 수정 제안을 해주세요.
                위장결혼 의심 표현이 있으면 반드시 경고하세요.
            """,
            "generation_prompt": """
                다음 정보를 바탕으로 진정성 있는 결혼배경 진술서를 작성하세요:
                - 첫 만남: {first_meeting_date}, {first_meeting_location}
                - 결혼일: {marriage_date}
                
                진심 어린 감정과 구체적인 에피소드를 포함하세요.
            """
        }
    ),
    
    "D": Scenario(
        id="D",
        name="가족 초청",
        name_en="Family Invitation",
        visa_type="F-1-5",
        icon="👨‍👩‍👧",
        description="부모님 또는 가족을 한국으로 초청",
        track="high_margin",
        required_docs=[
            "가족 초청장",
            "불법취업 방지 서약서",
            "신원보증서",
            "사증발급인정신청서"
        ],
        smart_form_fields=[
            {"name": "invitee_name", "label": "피초청인 성명", "type": "text"},
            {"name": "invitee_relation", "label": "관계", "type": "select",
             "options": ["부", "모", "형제", "자녀", "기타"]},
            {"name": "invitee_birth_date", "label": "피초청인 생년월일", "type": "date"},
            {"name": "invitee_passport_no", "label": "피초청인 여권번호", "type": "text"},
            {"name": "invitee_address", "label": "피초청인 본국 주소", "type": "text"},
            {"name": "invitation_purpose", "label": "초청 목적", "type": "select",
             "options": ["방문", "요양", "가족 돌봄", "기타"]},
            {"name": "stay_period", "label": "예정 체류 기간", "type": "text"},
            {"name": "inviter_income", "label": "초청인 연 소득 (만원)", "type": "number"},
            {"name": "inviter_assets", "label": "초청인 자산 (만원)", "type": "number"},
        ],
        ai_prompts={
            "narrative_field": "invitation_reason",
            "narrative_label": "초청 사유 및 필요성",
            "narrative_placeholder": "가족을 초청해야 하는 구체적인 이유를 설명해주세요...",
            "validation_prompt": """
                당신은 가족초청 비자 서류 검토 전문가입니다.
                다음 초청 사유를 검토하세요:
                
                검토 기준:
                1. 인도적 사유가 명확한가?
                2. 불법 취업 의도가 느껴지지 않는가?
                3. 경제적 부양 능력이 증명되는가?
                4. 체류 기간이 합리적인가?
                
                문제가 있으면 수정 제안을 해주세요.
            """
        }
    ),
    
    "E": Scenario(
        id="E",
        name="전문 인력",
        name_en="Professional Worker",
        visa_type="E-7",
        icon="🎓",
        description="특정 분야 전문 인력 채용을 위한 비자 신청",
        track="recurring",
        required_docs=[
            "사증발급인정신청서",
            "고용활용계획서",
            "신원보증서"
        ],
        smart_form_fields=[
            {"name": "company_name", "label": "기업명", "type": "text"},
            {"name": "company_business_no", "label": "사업자등록번호", "type": "text"},
            {"name": "company_address", "label": "기업 주소", "type": "text"},
            {"name": "company_industry", "label": "업종", "type": "text"},
            {"name": "company_employees", "label": "상시 근로자 수", "type": "number"},
            {"name": "position_title", "label": "채용 직위", "type": "text"},
            {"name": "position_duties", "label": "담당 업무", "type": "textarea"},
            {"name": "annual_salary", "label": "연봉 (만원)", "type": "number"},
            {"name": "contract_period", "label": "계약 기간", "type": "text"},
            {"name": "foreigner_name", "label": "외국인 성명", "type": "text"},
            {"name": "foreigner_nationality", "label": "외국인 국적", "type": "text"},
            {"name": "foreigner_education", "label": "외국인 학력", "type": "text"},
            {"name": "foreigner_experience", "label": "외국인 경력 (년)", "type": "number"},
        ],
        ai_prompts={
            "narrative_field": "employment_necessity",
            "narrative_label": "채용 필요성 및 기대 효과",
            "narrative_placeholder": "이 외국인 인력을 채용해야 하는 이유와 기대 효과를 설명해주세요...",
            "validation_prompt": """
                당신은 E-7 전문인력 비자 서류 검토 전문가입니다.
                다음 고용활용계획서 내용을 검토하세요:
                
                검토 기준:
                1. 직무가 단순 노무가 아닌가?
                2. 해당 분야 전문성이 필요한가?
                3. 국내 인력으로 대체 불가한가?
                4. 급여가 적정 수준인가?
                
                문제가 있으면 수정 제안을 해주세요.
                단순 노무 직무로 보이면 반드시 경고하세요.
            """,
            "generation_prompt": """
                다음 정보를 바탕으로 설득력 있는 고용활용계획서를 작성하세요:
                - 기업: {company_name} ({company_industry})
                - 직위: {position_title}
                - 담당 업무: {position_duties}
                - 외국인 학력: {foreigner_education}
                - 외국인 경력: {foreigner_experience}년
                
                이 인력의 채용 필요성과 기대 효과를 논리적으로 설명하세요.
            """
        }
    ),
    
    "F": Scenario(
        id="F",
        name="국적 귀화",
        name_en="Naturalization",
        visa_type="귀화",
        icon="🏛️",
        description="대한민국 국적 취득을 위한 귀화 신청",
        track="recurring",
        required_docs=[
            "귀화허가신청서",
            "귀화동기서",
            "귀화추천서",
            "가족관계통보서"
        ],
        smart_form_fields=[
            {"name": "korea_stay_years", "label": "한국 거주 기간 (년)", "type": "number"},
            {"name": "first_entry_date", "label": "최초 입국일", "type": "date"},
            {"name": "current_visa_type", "label": "현재 체류자격", "type": "text"},
            {"name": "criminal_record", "label": "범죄 이력", "type": "select",
             "options": ["없음", "있음"]},
            {"name": "korean_language_level", "label": "한국어 능력", "type": "select",
             "options": ["TOPIK 1급", "TOPIK 2급", "TOPIK 3급", "TOPIK 4급", "TOPIK 5급", "TOPIK 6급", "사회통합프로그램 이수"]},
            {"name": "korean_spouse", "label": "한국인 배우자 유무", "type": "select",
             "options": ["있음", "없음"]},
            {"name": "children_in_korea", "label": "한국 내 자녀 수", "type": "number"},
            {"name": "property_value", "label": "보유 재산 (만원)", "type": "number"},
            {"name": "annual_income", "label": "연 소득 (만원)", "type": "number"},
        ],
        ai_prompts={
            "narrative_field": "naturalization_motivation",
            "narrative_label": "귀화 동기 및 한국 사회 기여 계획",
            "narrative_placeholder": "한국 국적을 취득하고자 하는 이유와 한국 사회에 기여할 계획을 작성해주세요...",
            "validation_prompt": """
                당신은 귀화 서류 검토 전문가입니다.
                다음 귀화동기서 내용을 검토하세요:
                
                검토 기준:
                1. 한국에 대한 진정한 애정이 느껴지는가?
                2. 구체적인 사회 기여 계획이 있는가?
                3. 장기 거주 의지가 명확한가?
                4. 한국 문화에 대한 이해가 있는가?
                
                문제가 있으면 수정 제안을 해주세요.
            """,
            "generation_prompt": """
                다음 정보를 바탕으로 진정성 있는 귀화동기서를 작성하세요:
                - 한국 거주 기간: {korea_stay_years}년
                - 한국어 능력: {korean_language_level}
                - 배우자: {korean_spouse}
                
                한국에 대한 애정과 사회 기여 의지를 진솔하게 표현하세요.
            """
        }
    ),
}

# =============================================================================
# 📄 문서 템플릿 매핑
# =============================================================================

DOCUMENT_TEMPLATES = {
    "통합신청서": "unified_application.docx",
    "구직활동계획서": "job_search_plan.docx",
    "거주숙소제공확인서": "housing_confirmation.docx",
    "신원보증서": "identity_guarantee.docx",
    "시간제취업 확인서": "part_time_work_confirmation.docx",
    "표준근로계약서": "standard_labor_contract.docx",
    "요건 준수 확인서": "compliance_confirmation.docx",
    "결혼배경 진술서": "marriage_background_statement.docx",
    "배우자 초청장": "spouse_invitation.docx",
    "소득요건 면제신청서": "income_exemption_application.docx",
    "가족 초청장": "family_invitation.docx",
    "불법취업 방지 서약서": "illegal_work_prevention_pledge.docx",
    "사증발급인정신청서": "visa_issuance_application.docx",
    "고용활용계획서": "employment_plan.docx",
    "귀화허가신청서": "naturalization_application.docx",
    "귀화동기서": "naturalization_motivation.docx",
    "귀화추천서": "naturalization_recommendation.docx",
    "가족관계통보서": "family_relation_notice.docx",
    "제출 체크리스트": "submission_checklist.docx",
}

# =============================================================================
# 🔧 앱 초기화 함수
# =============================================================================

def init_page_config():
    """Streamlit 페이지 설정"""
    st.set_page_config(
        page_title="K-Stay | Korea Stay Assistant",
        page_icon="🇰🇷",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def init_session_state():
    """세션 상태 초기화"""
    defaults = {
        'authenticated': False,
        'user_id': None,
        'user_email': None,
        'user_data': {},
        'is_paid': False,
        'is_admin': False,
        'current_page': 'dashboard',
        'selected_scenario': None,
        'form_data': {},
        'narrative_data': {},
        'ai_feedback': {},
        'chat_history': [],
        'generated_documents': [],
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
