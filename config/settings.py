"""
K-Stay Configuration Settings
Layer 기반 데이터 구조 설계
- Layer 1 (Universal): users 테이블에서 자동 로드 (회원가입 시 입력, 수정 불가)
- Layer 2 (Variable): 시나리오별 폼 입력 (객관적 사실)
- Layer 3 (Narrative): AI가 검토하는 서술형 데이터
"""

import streamlit as st
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

# =============================================================================
# 🔑 API KEYS & SECRETS
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
# 📊 LAYER 1: Universal Facts (불변 정보 - users 테이블)
# =============================================================================

LAYER1_UNIVERSAL_FIELDS = [
    # 계정 정보
    {
        "data_key": "email",
        "label": "이메일",
        "label_en": "Email",
        "type": "text",
        "category": "account"
    },
    
    # 인적사항
    {
        "data_key": "surname",
        "label": "성",
        "label_en": "Surname",
        "type": "text",
        "category": "personal"
    },
    {
        "data_key": "given_name",
        "label": "이름",
        "label_en": "Given Name",
        "type": "text",
        "category": "personal"
    },
    {
        "data_key": "birth_date",
        "label": "생년월일",
        "label_en": "Date of Birth",
        "type": "date",
        "category": "personal"
    },
    {
        "data_key": "gender",
        "label": "성별",
        "label_en": "Gender",
        "type": "select",
        "options": ["Male", "Female"],
        "category": "personal"
    },
    {
        "data_key": "nationality",
        "label": "국적",
        "label_en": "Nationality",
        "type": "text",
        "category": "personal"
    },
    {
        "data_key": "alien_registration_no",
        "label": "외국인등록번호",
        "label_en": "Alien Registration No.",
        "type": "text",
        "category": "personal"
    },
    
    # 여권정보
    {
        "data_key": "passport_no",
        "label": "여권번호",
        "label_en": "Passport No.",
        "type": "text",
        "category": "passport"
    },
    {
        "data_key": "passport_issue_date",
        "label": "여권 발급일",
        "label_en": "Passport Issue Date",
        "type": "date",
        "category": "passport"
    },
    {
        "data_key": "passport_expiry_date",
        "label": "여권 만료일",
        "label_en": "Passport Expiry Date",
        "type": "date",
        "category": "passport"
    },
    
    # 연락처
    {
        "data_key": "korea_address",
        "label": "한국 주소",
        "label_en": "Address in Korea",
        "type": "text",
        "category": "contact"
    },
    {
        "data_key": "korea_phone",
        "label": "한국 전화번호",
        "label_en": "Phone in Korea",
        "type": "text",
        "category": "contact"
    },
    {
        "data_key": "home_country_address",
        "label": "본국 주소",
        "label_en": "Home Country Address",
        "type": "text",
        "category": "contact"
    },
    {
        "data_key": "home_country_phone",
        "label": "본국 전화번호",
        "label_en": "Home Country Phone",
        "type": "text",
        "category": "contact"
    },
]

# Layer 1 필드 키 목록 (빠른 조회용)
LAYER1_KEYS = [f["data_key"] for f in LAYER1_UNIVERSAL_FIELDS]

# =============================================================================
# 📊 LAYER 2: Variable Facts (가변 정보 - 시나리오별 폼 입력)
# =============================================================================

LAYER2_VARIABLE_FIELDS = {
    # -----------------------------------------------------------------
    # 시나리오 A: 구직 준비 (D-10)
    # -----------------------------------------------------------------
    "A": {
        "scenario_name": "구직 준비",
        "visa_type": "D-10",
        "fields": [
            {
                "data_key": "chinese_name",
                "label": "한자 이름",
                "label_en": "Chinese Name",
                "type": "text",
                "placeholder": "예: 洪吉童",
                "required": False,
                "section": "기본정보"
            },
            {
                "data_key": "school_name",
                "label": "출신 대학교",
                "label_en": "University/College Name",
                "type": "text",
                "placeholder": "예: 서강대학교",
                "required": True,
                "section": "학력"
            },
            {
                "data_key": "major_degree",
                "label": "전공 및 학위",
                "label_en": "Major & Degree",
                "type": "text",
                "placeholder": "예: 컴퓨터공학 학사",
                "required": True,
                "section": "학력"
            },
            {
                "data_key": "work_experience",
                "label": "경력사항",
                "label_en": "Work Experience",
                "type": "textarea",
                "placeholder": "예: ABC회사 인턴 6개월, XYZ프로젝트 참여",
                "required": False,
                "section": "경력"
            },
            {
                "data_key": "target_industry",
                "label": "희망 산업/직종",
                "label_en": "Target Industry/Occupation",
                "type": "text",
                "placeholder": "예: IT/소프트웨어 개발",
                "required": True,
                "section": "구직목표"
            },
            {
                "data_key": "target_company",
                "label": "희망 기업",
                "label_en": "Target Company",
                "type": "text",
                "placeholder": "예: 네이버, 카카오, 삼성전자",
                "required": False,
                "section": "구직목표"
            },
            {
                "data_key": "desired_salary",
                "label": "희망 연봉 (만원)",
                "label_en": "Desired Salary",
                "type": "number",
                "placeholder": "예: 4000",
                "required": False,
                "section": "구직목표"
            },
            {
                "data_key": "living_expenses_cash",
                "label": "생활비 - 현금 (만원)",
                "label_en": "Living Expenses - Cash",
                "type": "number",
                "placeholder": "예: 500",
                "required": False,
                "section": "재정"
            },
            {
                "data_key": "living_expenses_deposit",
                "label": "생활비 - 예금 (만원)",
                "label_en": "Living Expenses - Deposit",
                "type": "number",
                "placeholder": "예: 2000",
                "required": False,
                "section": "재정"
            },
            {
                "data_key": "living_expenses_credit_card",
                "label": "신용카드 보유",
                "label_en": "Credit Card",
                "type": "select",
                "options": ["있음", "없음"],
                "required": False,
                "section": "재정"
            },
            {
                "data_key": "living_expenses_remittance",
                "label": "송금 예정액 (만원)",
                "label_en": "Remittance",
                "type": "number",
                "placeholder": "예: 100",
                "required": False,
                "section": "재정"
            },
        ]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 B: 아르바이트 (시간제 취업)
    # -----------------------------------------------------------------
    "B": {
        "scenario_name": "아르바이트",
        "visa_type": "시간제 취업",
        "fields": [
            {
                "data_key": "school_name",
                "label": "학교명",
                "label_en": "School Name",
                "type": "text",
                "placeholder": "예: 서울대학교",
                "required": True,
                "section": "학교정보"
            },
            {
                "data_key": "student_status",
                "label": "재학 상태",
                "label_en": "Student Status",
                "type": "select",
                "options": ["재학중", "휴학중", "수료"],
                "required": True,
                "section": "학교정보"
            },
            {
                "data_key": "semester",
                "label": "현재 학기",
                "label_en": "Current Semester",
                "type": "text",
                "placeholder": "예: 3학년 2학기",
                "required": True,
                "section": "학교정보"
            },
            {
                "data_key": "gpa",
                "label": "평균 성적 (GPA)",
                "label_en": "GPA",
                "type": "number",
                "min_value": 0.0,
                "max_value": 4.5,
                "step": 0.1,
                "required": False,
                "section": "학교정보"
            },
            {
                "data_key": "employer_name",
                "label": "고용주 상호",
                "label_en": "Employer Name",
                "type": "text",
                "placeholder": "예: 스타벅스 강남점",
                "required": True,
                "section": "고용주정보"
            },
            {
                "data_key": "employer_business_no",
                "label": "사업자등록번호",
                "label_en": "Business Registration No.",
                "type": "text",
                "placeholder": "예: 123-45-67890",
                "required": True,
                "section": "고용주정보"
            },
            {
                "data_key": "employer_representative",
                "label": "대표자명",
                "label_en": "Representative",
                "type": "text",
                "placeholder": "예: 김대표",
                "required": True,
                "section": "고용주정보"
            },
            {
                "data_key": "employer_phone",
                "label": "고용주 연락처",
                "label_en": "Employer Phone",
                "type": "text",
                "placeholder": "예: 02-1234-5678",
                "required": True,
                "section": "고용주정보"
            },
            {
                "data_key": "work_address",
                "label": "근무지 주소",
                "label_en": "Work Address",
                "type": "text",
                "placeholder": "예: 서울시 강남구 테헤란로 123",
                "required": True,
                "section": "고용주정보"
            },
            {
                "data_key": "hourly_wage",
                "label": "시급 (원)",
                "label_en": "Hourly Wage",
                "type": "number",
                "min_value": 9860,
                "step": 100,
                "required": True,
                "section": "근무조건"
            },
            {
                "data_key": "weekly_hours",
                "label": "주당 근무시간",
                "label_en": "Weekly Hours",
                "type": "number",
                "min_value": 1,
                "max_value": 20,
                "required": True,
                "section": "근무조건"
            },
            {
                "data_key": "work_period_start",
                "label": "근무 시작일",
                "label_en": "Work Start Date",
                "type": "date",
                "required": True,
                "section": "근무조건"
            },
            {
                "data_key": "work_period_end",
                "label": "근무 종료일",
                "label_en": "Work End Date",
                "type": "date",
                "required": True,
                "section": "근무조건"
            },
        ]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 C: 결혼 이민 (F-6)
    # -----------------------------------------------------------------
    "C": {
        "scenario_name": "결혼 이민",
        "visa_type": "F-6",
        "fields": [
            {
                "data_key": "spouse_name",
                "label": "배우자 성명",
                "label_en": "Spouse Name",
                "type": "text",
                "placeholder": "예: 김철수",
                "required": True,
                "section": "배우자정보"
            },
            {
                "data_key": "spouse_resident_no",
                "label": "배우자 주민등록번호",
                "label_en": "Spouse Resident No.",
                "type": "text",
                "placeholder": "예: 900101-1234567",
                "required": True,
                "section": "배우자정보"
            },
            {
                "data_key": "spouse_phone",
                "label": "배우자 연락처",
                "label_en": "Spouse Phone",
                "type": "text",
                "placeholder": "예: 010-1234-5678",
                "required": True,
                "section": "배우자정보"
            },
            {
                "data_key": "spouse_occupation",
                "label": "배우자 직업",
                "label_en": "Spouse Occupation",
                "type": "text",
                "placeholder": "예: 회사원",
                "required": True,
                "section": "배우자정보"
            },
            {
                "data_key": "spouse_income",
                "label": "배우자 연 소득 (만원)",
                "label_en": "Spouse Annual Income",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "배우자정보"
            },
            {
                "data_key": "marriage_date",
                "label": "혼인신고일",
                "label_en": "Marriage Date",
                "type": "date",
                "required": True,
                "section": "혼인정보"
            },
            {
                "data_key": "marriage_location",
                "label": "혼인신고 장소",
                "label_en": "Marriage Registration Location",
                "type": "text",
                "placeholder": "예: 서울시 강남구청",
                "required": True,
                "section": "혼인정보"
            },
            {
                "data_key": "residence_type",
                "label": "주거 형태",
                "label_en": "Residence Type",
                "type": "select",
                "options": ["자가", "전세", "월세", "기타"],
                "required": True,
                "section": "혼인정보"
            },
            {
                "data_key": "first_meeting_date",
                "label": "첫 만남 시기",
                "label_en": "First Meeting Date",
                "type": "date",
                "required": True,
                "section": "만남정보"
            },
            {
                "data_key": "first_meeting_location",
                "label": "첫 만남 장소",
                "label_en": "First Meeting Location",
                "type": "text",
                "placeholder": "예: 서울 종로구 인사동 카페",
                "required": True,
                "section": "만남정보"
            },
        ]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 D: 가족 초청 (F-1-5)
    # -----------------------------------------------------------------
    "D": {
        "scenario_name": "가족 초청",
        "visa_type": "F-1-5",
        "fields": [
            {
                "data_key": "invitee_name",
                "label": "피초청인 성명",
                "label_en": "Invitee Name",
                "type": "text",
                "placeholder": "예: 홍길순",
                "required": True,
                "section": "피초청인정보"
            },
            {
                "data_key": "invitee_relation",
                "label": "관계",
                "label_en": "Relationship",
                "type": "select",
                "options": ["부", "모", "형제", "자녀", "기타"],
                "required": True,
                "section": "피초청인정보"
            },
            {
                "data_key": "invitee_birth_date",
                "label": "피초청인 생년월일",
                "label_en": "Invitee Birth Date",
                "type": "date",
                "required": True,
                "section": "피초청인정보"
            },
            {
                "data_key": "invitee_passport_no",
                "label": "피초청인 여권번호",
                "label_en": "Invitee Passport No.",
                "type": "text",
                "placeholder": "예: M12345678",
                "required": True,
                "section": "피초청인정보"
            },
            {
                "data_key": "invitee_address",
                "label": "피초청인 본국 주소",
                "label_en": "Invitee Home Address",
                "type": "text",
                "placeholder": "예: 123 Main St, City, Country",
                "required": True,
                "section": "피초청인정보"
            },
            {
                "data_key": "invitation_purpose",
                "label": "초청 목적",
                "label_en": "Invitation Purpose",
                "type": "select",
                "options": ["방문", "요양", "가족 돌봄", "기타"],
                "required": True,
                "section": "초청정보"
            },
            {
                "data_key": "stay_period",
                "label": "예정 체류 기간",
                "label_en": "Planned Stay Period",
                "type": "text",
                "placeholder": "예: 6개월",
                "required": True,
                "section": "초청정보"
            },
            {
                "data_key": "inviter_income",
                "label": "초청인 연 소득 (만원)",
                "label_en": "Inviter Annual Income",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "초청인재정"
            },
            {
                "data_key": "inviter_assets",
                "label": "초청인 자산 (만원)",
                "label_en": "Inviter Assets",
                "type": "number",
                "min_value": 0,
                "required": False,
                "section": "초청인재정"
            },
        ]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 E: 전문 인력 (E-7)
    # -----------------------------------------------------------------
    "E": {
        "scenario_name": "전문 인력",
        "visa_type": "E-7",
        "fields": [
            {
                "data_key": "company_name",
                "label": "기업명",
                "label_en": "Company Name",
                "type": "text",
                "placeholder": "예: 삼성전자",
                "required": True,
                "section": "기업정보"
            },
            {
                "data_key": "company_business_no",
                "label": "사업자등록번호",
                "label_en": "Business Registration No.",
                "type": "text",
                "placeholder": "예: 123-45-67890",
                "required": True,
                "section": "기업정보"
            },
            {
                "data_key": "company_address",
                "label": "기업 주소",
                "label_en": "Company Address",
                "type": "text",
                "placeholder": "예: 경기도 수원시 영통구",
                "required": True,
                "section": "기업정보"
            },
            {
                "data_key": "company_industry",
                "label": "업종",
                "label_en": "Industry",
                "type": "text",
                "placeholder": "예: 전자제품 제조",
                "required": True,
                "section": "기업정보"
            },
            {
                "data_key": "company_employees",
                "label": "상시 근로자 수",
                "label_en": "Number of Employees",
                "type": "number",
                "min_value": 1,
                "required": True,
                "section": "기업정보"
            },
            {
                "data_key": "position_title",
                "label": "채용 직위",
                "label_en": "Position Title",
                "type": "text",
                "placeholder": "예: 소프트웨어 엔지니어",
                "required": True,
                "section": "채용정보"
            },
            {
                "data_key": "position_duties",
                "label": "담당 업무",
                "label_en": "Job Duties",
                "type": "textarea",
                "placeholder": "예: AI 모델 개발 및 최적화",
                "required": True,
                "section": "채용정보"
            },
            {
                "data_key": "annual_salary",
                "label": "연봉 (만원)",
                "label_en": "Annual Salary",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "채용정보"
            },
            {
                "data_key": "contract_period",
                "label": "계약 기간",
                "label_en": "Contract Period",
                "type": "text",
                "placeholder": "예: 2년",
                "required": True,
                "section": "채용정보"
            },
            {
                "data_key": "foreigner_name",
                "label": "외국인 성명",
                "label_en": "Foreigner Name",
                "type": "text",
                "placeholder": "예: John Smith",
                "required": True,
                "section": "외국인정보"
            },
            {
                "data_key": "foreigner_nationality",
                "label": "외국인 국적",
                "label_en": "Foreigner Nationality",
                "type": "text",
                "placeholder": "예: 미국",
                "required": True,
                "section": "외국인정보"
            },
            {
                "data_key": "foreigner_education",
                "label": "외국인 학력",
                "label_en": "Foreigner Education",
                "type": "text",
                "placeholder": "예: MIT 컴퓨터공학 석사",
                "required": True,
                "section": "외국인정보"
            },
            {
                "data_key": "foreigner_experience",
                "label": "외국인 경력 (년)",
                "label_en": "Foreigner Experience (years)",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "외국인정보"
            },
        ]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 F: 국적 귀화
    # -----------------------------------------------------------------
    "F": {
        "scenario_name": "국적 귀화",
        "visa_type": "귀화",
        "fields": [
            {
                "data_key": "korea_stay_years",
                "label": "한국 거주 기간 (년)",
                "label_en": "Years in Korea",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "체류정보"
            },
            {
                "data_key": "first_entry_date",
                "label": "최초 입국일",
                "label_en": "First Entry Date",
                "type": "date",
                "required": True,
                "section": "체류정보"
            },
            {
                "data_key": "current_visa_type",
                "label": "현재 체류자격",
                "label_en": "Current Visa Type",
                "type": "text",
                "placeholder": "예: F-2-7",
                "required": True,
                "section": "체류정보"
            },
            {
                "data_key": "criminal_record",
                "label": "범죄 이력",
                "label_en": "Criminal Record",
                "type": "select",
                "options": ["없음", "있음"],
                "required": True,
                "section": "체류정보"
            },
            {
                "data_key": "korean_language_level",
                "label": "한국어 능력",
                "label_en": "Korean Language Level",
                "type": "select",
                "options": ["TOPIK 1급", "TOPIK 2급", "TOPIK 3급", "TOPIK 4급", "TOPIK 5급", "TOPIK 6급", "사회통합프로그램 이수"],
                "required": True,
                "section": "자격요건"
            },
            {
                "data_key": "korean_spouse",
                "label": "한국인 배우자 유무",
                "label_en": "Korean Spouse",
                "type": "select",
                "options": ["있음", "없음"],
                "required": True,
                "section": "가족정보"
            },
            {
                "data_key": "children_in_korea",
                "label": "한국 내 자녀 수",
                "label_en": "Children in Korea",
                "type": "number",
                "min_value": 0,
                "required": False,
                "section": "가족정보"
            },
            {
                "data_key": "property_value",
                "label": "보유 재산 (만원)",
                "label_en": "Property Value",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "재정정보"
            },
            {
                "data_key": "annual_income",
                "label": "연 소득 (만원)",
                "label_en": "Annual Income",
                "type": "number",
                "min_value": 0,
                "required": True,
                "section": "재정정보"
            },
        ]
    },
}

# =============================================================================
# 📊 LAYER 3: Narrative Fields (서술형 - AI 검토)
# =============================================================================

LAYER3_NARRATIVE_FIELDS = {
    # -----------------------------------------------------------------
    # 시나리오 A: 구직 준비 (D-10)
    # -----------------------------------------------------------------
    "A": {
        "scenario_name": "구직 준비",
        "visa_type": "D-10",
        "narrative_label": "월별 구직 활동 계획",
        "fields": [
            {
                "data_key": "plan_month_1",
                "label": "1개월차 계획",
                "label_en": "1st Month Plan",
                "hint": "첫 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 이력서 및 자기소개서 작성, 잡코리아/사람인 등록, IT 기업 10곳 서류 지원",
                "min_chars": 50,
                "required": True,
                "anchor_text": "1st month"
            },
            {
                "data_key": "plan_month_2",
                "label": "2개월차 계획",
                "label_en": "2nd Month Plan",
                "hint": "두 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 면접 준비, 코딩테스트 대비, 추가 기업 지원",
                "min_chars": 50,
                "required": True,
                "anchor_text": "2nd month"
            },
            {
                "data_key": "plan_month_3",
                "label": "3개월차 계획",
                "label_en": "3rd Month Plan",
                "hint": "세 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 1차 면접 참여, 피드백 반영 및 보완",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3rd month"
            },
            {
                "data_key": "plan_month_4",
                "label": "4개월차 계획",
                "label_en": "4th Month Plan",
                "hint": "네 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 최종 면접 준비, 연봉 협상 준비",
                "min_chars": 50,
                "required": True,
                "anchor_text": "4th month"
            },
            {
                "data_key": "plan_month_5",
                "label": "5개월차 계획",
                "label_en": "5th Month Plan",
                "hint": "다섯 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 취업 확정 시 비자 변경 준비, 미확정 시 추가 지원",
                "min_chars": 50,
                "required": True,
                "anchor_text": "5th month"
            },
            {
                "data_key": "plan_month_6",
                "label": "6개월차 계획",
                "label_en": "6th Month Plan",
                "hint": "여섯 번째 달의 구직 활동 계획을 작성해주세요.",
                "placeholder": "예: 입사 준비 또는 비자 연장 준비",
                "min_chars": 50,
                "required": True,
                "anchor_text": "6th month"
            },
        ],
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
        "danger_patterns": ["취업 확정", "내정", "채용 확정", "이미 취업", "입사 예정"]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 B: 아르바이트 (시간제 취업)
    # -----------------------------------------------------------------
    "B": {
        "scenario_name": "아르바이트",
        "visa_type": "시간제 취업",
        "narrative_label": "업무 내용 및 근무 계획",
        "fields": [
            {
                "data_key": "work_description",
                "label": "담당 업무 내용",
                "label_en": "Job Description",
                "hint": "맡게 될 업무를 구체적으로 설명해주세요. (단순 노무가 아님을 증명)",
                "placeholder": "예: 카페에서 바리스타로 근무하며 음료 제조, 고객 응대, 재고 관리 등의 업무를 담당합니다...",
                "min_chars": 100,
                "required": True,
                "anchor_text": "업무 내용"
            },
            {
                "data_key": "work_schedule",
                "label": "근무 일정",
                "label_en": "Work Schedule",
                "hint": "주당 근무 시간과 요일별 스케줄을 작성해주세요. (주 20시간 이내)",
                "placeholder": "예: 월, 수, 금 오후 2시~6시 (주 12시간) 학업에 지장이 없는 시간대에 근무합니다...",
                "min_chars": 80,
                "required": True,
                "anchor_text": "근무 일정"
            },
            {
                "data_key": "study_balance",
                "label": "학업과의 병행 계획",
                "label_en": "Study Balance Plan",
                "hint": "아르바이트와 학업을 어떻게 병행할 것인지 설명해주세요.",
                "placeholder": "예: 수업이 없는 시간대에만 근무하여 학업에 집중하면서도...",
                "min_chars": 80,
                "required": False,
                "anchor_text": "병행 계획"
            },
        ],
        "validation_prompt": """
            당신은 시간제 취업 허가 서류 검토 전문가입니다.
            다음 내용을 검토하세요:
            
            검토 기준:
            1. 주 20시간 이내인가? (학기중)
            2. 최저임금 이상인가?
            3. 유흥업소 등 금지 업종이 아닌가?
            4. 학업에 지장이 없는 시간대인가?
            
            문제가 있으면 구체적인 수정 제안을 해주세요.
        """,
        "danger_patterns": ["풀타임", "40시간", "주 40", "전일제", "야간", "유흥"]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 C: 결혼 이민 (F-6)
    # -----------------------------------------------------------------
    "C": {
        "scenario_name": "결혼 이민",
        "visa_type": "F-6",
        "narrative_label": "교제 과정 및 결혼 배경",
        "fields": [
            {
                "data_key": "first_meeting",
                "label": "첫 만남과 교제 과정",
                "label_en": "First Meeting & Dating",
                "hint": "배우자와 처음 만난 계기와 교제 과정을 진솔하게 작성해주세요.",
                "placeholder": "예: 2022년 3월 친구의 소개로 처음 만났습니다. 첫 만남은 서울 종로구의 한 카페에서...",
                "min_chars": 200,
                "required": True,
                "anchor_text": "첫 만남"
            },
            {
                "data_key": "marriage_decision",
                "label": "결혼 결심 계기",
                "label_en": "Marriage Decision",
                "hint": "결혼을 결심하게 된 구체적인 계기나 에피소드를 작성해주세요.",
                "placeholder": "예: 1년간의 교제 후, 서로의 가치관과 미래 계획이 일치한다는 것을 확인하고...",
                "min_chars": 150,
                "required": True,
                "anchor_text": "결혼 결심"
            },
            {
                "data_key": "future_plan",
                "label": "결혼 후 계획",
                "label_en": "Future Plan",
                "hint": "결혼 후 한국에서의 생활 계획을 작성해주세요.",
                "placeholder": "예: 배우자와 함께 서울에서 거주하며, 한국어 공부를 계속하고...",
                "min_chars": 100,
                "required": True,
                "anchor_text": "결혼 후 계획"
            },
            {
                "data_key": "family_approval",
                "label": "양가 부모님 반응",
                "label_en": "Family Approval",
                "hint": "양가 부모님의 결혼에 대한 반응과 만남 과정을 작성해주세요.",
                "placeholder": "예: 2023년 설날에 배우자의 부모님을 처음 뵙고 인사드렸습니다...",
                "min_chars": 100,
                "required": False,
                "anchor_text": "양가 반응"
            },
        ],
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
        "danger_patterns": ["돈을 받고", "위장", "계약 결혼", "비자 때문에", "돈을 벌기 위해", "가짜"]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 D: 가족 초청 (F-1-5)
    # -----------------------------------------------------------------
    "D": {
        "scenario_name": "가족 초청",
        "visa_type": "F-1-5",
        "narrative_label": "초청 사유 및 계획",
        "fields": [
            {
                "data_key": "invitation_reason",
                "label": "초청 사유",
                "label_en": "Invitation Reason",
                "hint": "부모님/가족을 초청해야 하는 구체적인 사유를 작성해주세요.",
                "placeholder": "예: 어머니의 건강이 좋지 않아 한국에서 함께 지내며 돌봐드리고자 합니다...",
                "min_chars": 150,
                "required": True,
                "anchor_text": "초청 사유"
            },
            {
                "data_key": "stay_plan",
                "label": "체류 중 계획",
                "label_en": "Stay Plan",
                "hint": "초청 기간 동안의 구체적인 생활 계획을 작성해주세요.",
                "placeholder": "예: 저의 집에서 함께 거주하며, 정기적으로 병원 검진을 받고...",
                "min_chars": 100,
                "required": True,
                "anchor_text": "체류 계획"
            },
            {
                "data_key": "financial_support",
                "label": "재정 지원 계획",
                "label_en": "Financial Support",
                "hint": "체류 기간 동안의 재정적 지원 계획을 설명해주세요.",
                "placeholder": "예: 월 급여 350만원 중 100만원을 생활비로 지원하고...",
                "min_chars": 80,
                "required": True,
                "anchor_text": "재정 지원"
            },
        ],
        "validation_prompt": """
            당신은 가족초청 비자 서류 검토 전문가입니다.
            다음 초청 사유를 검토하세요:
            
            검토 기준:
            1. 인도적 사유가 명확한가?
            2. 불법 취업 의도가 느껴지지 않는가?
            3. 경제적 부양 능력이 증명되는가?
            4. 체류 기간이 합리적인가?
            
            문제가 있으면 수정 제안을 해주세요.
        """,
        "danger_patterns": ["취업하러", "일하러", "돈 벌러", "불법", "취업 알선"]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 E: 전문 인력 (E-7)
    # -----------------------------------------------------------------
    "E": {
        "scenario_name": "전문 인력",
        "visa_type": "E-7",
        "narrative_label": "채용 필요성 및 기대 효과",
        "fields": [
            {
                "data_key": "hiring_reason",
                "label": "채용 필요성",
                "label_en": "Hiring Necessity",
                "hint": "해당 외국인 인력을 채용해야 하는 구체적인 이유를 작성해주세요.",
                "placeholder": "예: 당사는 베트남 시장 진출을 위해 베트남어 원어민이면서 IT 개발 역량을 갖춘 인력이 필요합니다...",
                "min_chars": 150,
                "required": True,
                "anchor_text": "채용 필요성"
            },
            {
                "data_key": "job_duties",
                "label": "담당 업무 상세",
                "label_en": "Job Duties Detail",
                "hint": "담당하게 될 업무의 전문성과 구체적인 내용을 작성해주세요.",
                "placeholder": "예: 베트남 현지 고객사와의 기술 미팅 통역, 현지화 소프트웨어 개발...",
                "min_chars": 150,
                "required": True,
                "anchor_text": "담당 업무"
            },
            {
                "data_key": "expected_contribution",
                "label": "기대 효과",
                "label_en": "Expected Contribution",
                "hint": "채용으로 인한 회사 및 국가 경제에 대한 기대 효과를 작성해주세요.",
                "placeholder": "예: 베트남 시장 매출 30% 증가 예상, 양국 간 기술 교류 활성화...",
                "min_chars": 100,
                "required": False,
                "anchor_text": "기대 효과"
            },
        ],
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
        "danger_patterns": ["단순 노무", "청소", "설거지", "포장", "배달", "공장"]
    },
    
    # -----------------------------------------------------------------
    # 시나리오 F: 국적 귀화
    # -----------------------------------------------------------------
    "F": {
        "scenario_name": "국적 귀화",
        "visa_type": "귀화",
        "narrative_label": "귀화 동기 및 사회 기여 계획",
        "fields": [
            {
                "data_key": "naturalization_reason",
                "label": "귀화 동기",
                "label_en": "Naturalization Motivation",
                "hint": "한국 국적을 취득하고자 하는 동기를 진솔하게 작성해주세요.",
                "placeholder": "예: 한국에서 15년간 생활하며 이곳이 제 삶의 터전이 되었습니다...",
                "min_chars": 200,
                "required": True,
                "anchor_text": "귀화 동기"
            },
            {
                "data_key": "korea_adaptation",
                "label": "한국 사회 적응 과정",
                "label_en": "Korea Adaptation",
                "hint": "한국 사회에 어떻게 적응해왔는지 구체적으로 작성해주세요.",
                "placeholder": "예: 처음 한국에 왔을 때 언어와 문화의 차이로 어려움이 있었지만...",
                "min_chars": 150,
                "required": True,
                "anchor_text": "적응 과정"
            },
            {
                "data_key": "contribution_plan",
                "label": "사회 기여 계획",
                "label_en": "Contribution Plan",
                "hint": "한국 사회에 어떻게 기여할 계획인지 작성해주세요.",
                "placeholder": "예: 다문화 가정 지원 봉사활동에 참여하고, 제 경험을 바탕으로...",
                "min_chars": 100,
                "required": True,
                "anchor_text": "기여 계획"
            },
        ],
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
        "danger_patterns": ["한국이 싫", "빨리 떠나", "다른 나라", "임시", "잠시"]
    },
}

# =============================================================================
# 📊 시나리오 기본 정보
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
    required_docs: List[str]
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
        required_docs=["통합신청서", "구직활동계획서", "신원보증서"],
        price=9.99
    ),
    "B": Scenario(
        id="B",
        name="아르바이트",
        name_en="Part-time Work",
        visa_type="시간제 취업",
        icon="⏰",
        description="유학생/연수생 시간제 취업 허가 신청",
        track="high_volume",
        required_docs=["시간제취업 확인서", "표준근로계약서", "요건 준수 확인서", "통합신청서", "사업자등록증 사본"],
        price=9.99
    ),
    "C": Scenario(
        id="C",
        name="결혼 이민",
        name_en="Marriage Immigration",
        visa_type="F-6",
        icon="💍",
        description="한국인 배우자와의 결혼을 통한 비자 신청",
        track="high_margin",
        required_docs=["통합신청서", "결혼배경 진술서", "배우자 초청장", "신원보증서", "소득요건 면제신청서"],
        price=19.99
    ),
    "D": Scenario(
        id="D",
        name="가족 초청",
        name_en="Family Invitation",
        visa_type="F-1-5",
        icon="👨‍👩‍👧",
        description="부모님 또는 가족을 한국으로 초청",
        track="high_margin",
        required_docs=["가족 초청장", "불법취업 방지 서약서", "신원보증서", "사증발급인정신청서"],
        price=19.99
    ),
    "E": Scenario(
        id="E",
        name="전문 인력",
        name_en="Professional Worker",
        visa_type="E-7",
        icon="🎓",
        description="특정 분야 전문 인력 채용을 위한 비자 신청",
        track="recurring",
        required_docs=["사증발급인정신청서", "고용활용계획서", "신원보증서"],
        price=29.99
    ),
    "F": Scenario(
        id="F",
        name="국적 귀화",
        name_en="Naturalization",
        visa_type="귀화",
        icon="🏛️",
        description="대한민국 국적 취득을 위한 귀화 신청",
        track="recurring",
        required_docs=["귀화허가신청서", "귀화동기서", "귀화추천서", "가족관계통보서"],
        price=49.99
    ),
}

# =============================================================================
# 📄 문서 템플릿 매핑 (실제 파일명)
# =============================================================================

DOCUMENT_TEMPLATES = {
    # 공통 문서
    "통합신청서": "통합신청서(신고서).docx",
    "신원보증서": "신원보증서(한글).docx",
    "신원보증서(영문)": "신원보증서(영문).docx",
    "사증발급인정신청서": "사증발급인정신청서.docx",
    
    # 시나리오 A: 구직 (D-10)
    "구직활동계획서": "구직활동계획서.docx",
    
    # 시나리오 B: 아르바이트 (시간제 취업)
    "시간제취업확인서": "시간제취업확인서.docx",
    "유학생 시간제취업 요건 준수 확인서": "유학생 시간제취업 요건 준수 확인서(제조업_농축산어업_건설업 업종용).doc",
    
    # 시나리오 C: 결혼 이민 (F-6)
    "결혼배경진술서": "영주자격자의 배우자 결혼배경진술서(F-2-3).docx",
    "외국인 배우자 초청장": "외국인 배우자 초청장.docx",
    
    # 시나리오 D: 가족 초청 (F-1-5)
    "가족 초청장": "결혼이민자의 부모 등 가족 초청장(F-1-5 비자 신청용).docx",
    "불법체류 취업 방지 서약서": "불법체류 취업 방지 서약서(F-1-5).docx",
    
    # 시나리오 E: 전문 인력 (E-7)
    "고용사유서": "고용사유서.docx",
    
    # 시나리오 F: 국적 귀화
    "귀화허가신청서": "귀화허가신청서.docx",
    "귀화추천서": "귀화추천서.docx",
    "가족관계통보서": "가족관계통보서.docx",
    
    # 기타
    "거주숙소제공사실확인서": "거주숙소제공사실확인서(영문병기).docx",
}

# =============================================================================
# 🔧 유틸리티 함수
# =============================================================================

def get_layer2_fields(scenario_id: str) -> List[Dict]:
    """시나리오별 Layer 2 필드 가져오기"""
    scenario_data = LAYER2_VARIABLE_FIELDS.get(scenario_id, {})
    return scenario_data.get("fields", [])

def get_layer3_fields(scenario_id: str) -> List[Dict]:
    """시나리오별 Layer 3 필드 가져오기"""
    scenario_data = LAYER3_NARRATIVE_FIELDS.get(scenario_id, {})
    return scenario_data.get("fields", [])

def get_narrative_config(scenario_id: str) -> Dict:
    """시나리오별 Narrative 설정 가져오기"""
    return LAYER3_NARRATIVE_FIELDS.get(scenario_id, {})

def get_danger_patterns(scenario_id: str) -> List[str]:
    """시나리오별 위험 표현 패턴 가져오기"""
    scenario_data = LAYER3_NARRATIVE_FIELDS.get(scenario_id, {})
    return scenario_data.get("danger_patterns", [])

def get_validation_prompt(scenario_id: str) -> str:
    """시나리오별 AI 검증 프롬프트 가져오기"""
    scenario_data = LAYER3_NARRATIVE_FIELDS.get(scenario_id, {})
    return scenario_data.get("validation_prompt", "")

def is_layer1_field(data_key: str) -> bool:
    """해당 필드가 Layer 1인지 확인"""
    return data_key in LAYER1_KEYS

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
        'user_data': {},  # Layer 1 데이터 (DB에서 로드)
        'form_data': {},  # Layer 2 데이터 (폼 입력)
        'narrative_data': {},  # Layer 3 데이터 (서술형)
        'is_paid': False,
        'is_admin': False,
        'current_page': 'dashboard',
        'selected_scenario': None,
        'form_step': 1,
        'ai_feedbacks': [],
        'chat_history': [],
        'generated_documents': [],
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value