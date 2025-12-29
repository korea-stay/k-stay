# mapping_guide.py
# K-Stay Document Template Mapping Guide
# ======================================
# 문서 템플릿 내 앵커 텍스트 기반 데이터 매핑 정의

"""
[데이터 레이어 정의]
- Layer 1 (universal): users 테이블에서 자동 로드 (수정 불가)
- Layer 2 (variable): 시나리오별 추가 폼 입력 (객관적 사실)
- Layer 3 (narrative): AI가 생성/보정하는 서술형 데이터

[매핑 전략 (Strategy)]
- BELOW_CELL: 앵커 텍스트 아래 셀에 값 입력
- NEXT_CELL: 앵커 텍스트 오른쪽 셀에 값 입력
- APPEND_TO_SAME_CELL: 같은 셀에 값 덧붙이기
- CHECKBOX: 체크박스 선택 ([ ] -> [V])
- SPLIT_CELLS: 값을 각 글자별로 분할하여 셀에 입력 (주민번호 등)
- INSERT_IMAGE: 이미지 삽입 (서명 등)
"""

from typing import Dict, List, Any

# =============================================================================
# 성별 체크박스 매핑 (공통)
# =============================================================================

GENDER_CHECKBOX_MAP = {
    "Male": ["남", "Male", "M", "Man"],
    "M": ["남", "Male", "M", "Man"],
    "남": ["남", "Male", "M", "Man"],
    "Female": ["여", "Female", "F", "Woman"],
    "F": ["여", "Female", "F", "Woman"],
    "여": ["여", "Female", "F", "Woman"],
}

# =============================================================================
# 1. 구직활동계획서 (Job Search Plan) - 시나리오 A
# =============================================================================

JOB_SEARCH_PLAN_MAPPING = {
    "template_file": "job_search_plan.docx",
    "document_name": "구직활동계획서",
    "scenario_id": "A",
    "type": "narrative",
    "fields": [
        # --- Layer 1: 기본 인적사항 (Users 테이블) ---
        {
            "data_key": "surname",
            "layer": "universal",
            "anchor_text": ["Surname", "성명", "성(Surname)"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "given_name",
            "layer": "universal",
            "anchor_text": ["Given names", "이름", "명(Given"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "gender",
            "layer": "universal",
            "anchor_text": ["Gender", "성별"],
            "strategy": "CHECKBOX",
            "value_map": GENDER_CHECKBOX_MAP
        },
        {
            "data_key": "birth_date",
            "layer": "universal",
            "anchor_text": ["Date of Birth", "생년월일", "Date of Birth or Alien Registration No"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "nationality",
            "layer": "universal",
            "anchor_text": ["Nationality", "국적"],
            "strategy": "NEXT_CELL"
        },
        
        # --- Layer 2: 학력 및 경력 (폼 입력) ---
        {
            "data_key": "chinese_name",
            "layer": "variable",
            "anchor_text": ["中文姓名", "한자이름"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "school_name",
            "layer": "variable",
            "anchor_text": ["Name of University or College", "학교명", "Name of University"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "major_degree",
            "layer": "variable",
            "anchor_text": ["Major & Degree", "전공", "Graduate-to-be"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "work_experience",
            "layer": "variable",
            "anchor_text": ["Work Experience", "경력"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "target_industry",
            "layer": "variable",
            "anchor_text": ["Occupational Category", "희망직종", "직종"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "target_company",
            "layer": "variable",
            "anchor_text": ["Name of company", "희망기업"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "desired_salary",
            "layer": "variable",
            "anchor_text": ["Salary", "희망연봉"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "living_expenses_cash",
            "layer": "variable",
            "anchor_text": ["Cash", "현금"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "living_expenses_deposit",
            "layer": "variable",
            "anchor_text": ["Deposit", "예금"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "living_expenses_credit_card",
            "layer": "variable",
            "anchor_text": ["Credit card", "신용카드"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "living_expenses_remittance",
            "layer": "variable",
            "anchor_text": ["Remittance", "송금"],
            "strategy": "NEXT_CELL"
        },
        
        # --- Layer 3: 월별 구직 활동 계획 (AI 생성/보정) ---
        {
            "data_key": "plan_month_1",
            "layer": "narrative",
            "anchor_text": ["1st month", "1개월", "첫째달"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "plan_month_2",
            "layer": "narrative",
            "anchor_text": ["2nd month", "2개월", "둘째달"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "plan_month_3",
            "layer": "narrative",
            "anchor_text": ["3rd month", "3개월", "셋째달"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "plan_month_4",
            "layer": "narrative",
            "anchor_text": ["4th month", "4개월", "넷째달"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "plan_month_5",
            "layer": "narrative",
            "anchor_text": ["5th month", "5개월", "다섯째달"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "plan_month_6",
            "layer": "narrative",
            "anchor_text": ["6th month", "6개월", "여섯째달"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 2. 신원보증서 (Letter of Guarantee) - 공통 문서
# =============================================================================

GUARANTEE_LETTER_MAPPING = {
    "template_file": "guarantee_letter.docx",
    "document_name": "신원보증서",
    "scenario_id": "common",  # 여러 시나리오에서 사용
    "type": "form",
    "fields": [
        # --- Layer 1: 피보증인(신청자) 기본 정보 ---
        {
            "data_key": "full_name",  # surname + given_name 조합
            "layer": "universal",
            "anchor_text": ["성 명", "성명"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 0
        },
        {
            "data_key": "birth_date",
            "layer": "universal",
            "anchor_text": ["생년월일"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 0
        },
        {
            "data_key": "gender",
            "layer": "universal",
            "anchor_text": ["성별", "성 별"],
            "strategy": "CHECKBOX",
            "value_map": GENDER_CHECKBOX_MAP,
            "index": 0
        },
        {
            "data_key": "nationality",
            "layer": "universal",
            "anchor_text": ["국적"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 0
        },
        {
            "data_key": "passport_no",
            "layer": "universal",
            "anchor_text": ["여권번호", "여권번호 또는 생년월일"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 0
        },
        {
            "data_key": "korea_address",
            "layer": "universal",
            "anchor_text": ["대한민국 주소", "한국 주소"],
            "strategy": "APPEND_TO_SAME_CELL"
        },
        {
            "data_key": "korea_phone",
            "layer": "universal",
            "anchor_text": ["전화번호"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 0
        },
        
        # --- Layer 2: 보증인 정보 (폼 입력) ---
        {
            "data_key": "stay_purpose",
            "layer": "variable",
            "anchor_text": ["체류목적"],
            "strategy": "APPEND_TO_SAME_CELL"
        },
        {
            "data_key": "guarantor_name",
            "layer": "variable",
            "anchor_text": ["성명", "성 명"],
            "strategy": "APPEND_TO_SAME_CELL",
            "index": 1  # 두 번째 등장 (보증인)
        },
        {
            "data_key": "guarantor_relationship",
            "layer": "variable",
            "anchor_text": ["피보증인과의 관계", "관계"],
            "strategy": "APPEND_TO_SAME_CELL"
        },
        {
            "data_key": "guarantee_period",
            "layer": "variable",
            "anchor_text": ["보증기간"],
            "strategy": "APPEND_TO_SAME_CELL"
        },
    ]
}

# =============================================================================
# 3. 통합신청서 (Unified Application Form) - 공통 문서
# =============================================================================

UNIFIED_APPLICATION_MAPPING = {
    "template_file": "unified_application.docx",
    "document_name": "통합신청서",
    "scenario_id": "common",
    "type": "form",
    "fields": [
        # --- Layer 1: 핵심 인적사항 (Users 테이블) ---
        {
            "data_key": "surname",
            "layer": "universal",
            "anchor_text": ["Surname"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "given_name",
            "layer": "universal",
            "anchor_text": ["Given names"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "gender",
            "layer": "universal",
            "anchor_text": ["성 별", "성별", "Gender"],
            "strategy": "CHECKBOX",
            "value_map": GENDER_CHECKBOX_MAP
        },
        {
            "data_key": "dob_year",
            "layer": "universal",
            "anchor_text": ["년 yyyy"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "dob_month",
            "layer": "universal",
            "anchor_text": ["월 mm"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "dob_day",
            "layer": "universal",
            "anchor_text": ["일 dd"],
            "strategy": "BELOW_CELL"
        },
        {
            "data_key": "nationality",
            "layer": "universal",
            "anchor_text": ["국 적", "국적"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "passport_no",
            "layer": "universal",
            "anchor_text": ["여권 번호"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "passport_issue_date",
            "layer": "universal",
            "anchor_text": ["여권 발급일자"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "passport_expiry_date",
            "layer": "universal",
            "anchor_text": ["여권 유효기간"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "alien_registration_no",
            "layer": "universal",
            "anchor_text": ["외국인등록번호"],
            "strategy": "SPLIT_CELLS",
            "options": {"skip_chars": ["-"]}
        },
        {
            "data_key": "korea_address",
            "layer": "universal",
            "anchor_text": ["대한민국 내 주소"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "korea_phone",
            "layer": "universal",
            "anchor_text": ["전화 번호"],
            "strategy": "NEXT_CELL",
            "index": 0
        },
        {
            "data_key": "korea_phone",
            "layer": "universal",
            "anchor_text": ["휴대 전화"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "email",
            "layer": "universal",
            "anchor_text": ["전자우편"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "home_country_address",
            "layer": "universal",
            "anchor_text": ["본국 주소"],
            "strategy": "NEXT_CELL"
        },
        
        # --- Layer 2: 신청 정보 (폼 입력) ---
        {
            "data_key": "chinese_name",
            "layer": "variable",
            "anchor_text": ["漢字姓名"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "workplace_name",
            "layer": "variable",
            "anchor_text": ["근무처"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "business_reg_no",
            "layer": "variable",
            "anchor_text": ["사업자등록번호"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "application_date",
            "layer": "variable",
            "anchor_text": ["신청일"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 4. 시간제취업 확인서 - 시나리오 B (템플릿)
# =============================================================================

PART_TIME_WORK_MAPPING = {
    "template_file": "part_time_work_confirmation.docx",
    "document_name": "시간제취업 확인서",
    "scenario_id": "B",
    "type": "form",
    "fields": [
        # Layer 1
        {
            "data_key": "full_name",
            "layer": "universal",
            "anchor_text": ["성명", "이름"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "alien_registration_no",
            "layer": "universal",
            "anchor_text": ["외국인등록번호"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 2
        {
            "data_key": "school_name",
            "layer": "variable",
            "anchor_text": ["학교명", "재학학교"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "employer_name",
            "layer": "variable",
            "anchor_text": ["사업장명", "고용주"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "employer_business_no",
            "layer": "variable",
            "anchor_text": ["사업자등록번호"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "work_address",
            "layer": "variable",
            "anchor_text": ["근무지", "사업장주소"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "weekly_hours",
            "layer": "variable",
            "anchor_text": ["주당근무시간", "근무시간"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "hourly_wage",
            "layer": "variable",
            "anchor_text": ["시급", "급여"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 3
        {
            "data_key": "work_description",
            "layer": "narrative",
            "anchor_text": ["업무내용", "담당업무"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 5. 결혼배경 진술서 - 시나리오 C (템플릿)
# =============================================================================

MARRIAGE_STATEMENT_MAPPING = {
    "template_file": "marriage_background_statement.docx",
    "document_name": "결혼배경 진술서",
    "scenario_id": "C",
    "type": "narrative",
    "fields": [
        # Layer 1
        {
            "data_key": "full_name",
            "layer": "universal",
            "anchor_text": ["신청인 성명", "성명"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "nationality",
            "layer": "universal",
            "anchor_text": ["국적"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 2
        {
            "data_key": "spouse_name",
            "layer": "variable",
            "anchor_text": ["배우자 성명", "한국인 배우자"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "marriage_date",
            "layer": "variable",
            "anchor_text": ["혼인신고일", "결혼일"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "first_meeting_date",
            "layer": "variable",
            "anchor_text": ["첫 만남", "교제시작"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 3
        {
            "data_key": "first_meeting",
            "layer": "narrative",
            "anchor_text": ["교제경위", "만남과정"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "marriage_decision",
            "layer": "narrative",
            "anchor_text": ["결혼결심", "결혼계기"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "future_plan",
            "layer": "narrative",
            "anchor_text": ["결혼후계획", "향후계획"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 6. 가족 초청장 - 시나리오 D (템플릿)
# =============================================================================

FAMILY_INVITATION_MAPPING = {
    "template_file": "family_invitation.docx",
    "document_name": "가족 초청장",
    "scenario_id": "D",
    "type": "narrative",
    "fields": [
        # Layer 1
        {
            "data_key": "full_name",
            "layer": "universal",
            "anchor_text": ["초청인 성명", "초청인"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "korea_address",
            "layer": "universal",
            "anchor_text": ["초청인 주소"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 2
        {
            "data_key": "invitee_name",
            "layer": "variable",
            "anchor_text": ["피초청인 성명", "피초청인"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "invitee_relation",
            "layer": "variable",
            "anchor_text": ["관계"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "stay_period",
            "layer": "variable",
            "anchor_text": ["체류기간", "방문기간"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 3
        {
            "data_key": "invitation_reason",
            "layer": "narrative",
            "anchor_text": ["초청사유", "방문목적"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "stay_plan",
            "layer": "narrative",
            "anchor_text": ["체류계획"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 7. 고용활용계획서 - 시나리오 E (템플릿)
# =============================================================================

EMPLOYMENT_PLAN_MAPPING = {
    "template_file": "employment_plan.docx",
    "document_name": "고용활용계획서",
    "scenario_id": "E",
    "type": "narrative",
    "fields": [
        # Layer 2
        {
            "data_key": "company_name",
            "layer": "variable",
            "anchor_text": ["기업명", "회사명"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "company_business_no",
            "layer": "variable",
            "anchor_text": ["사업자등록번호"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "foreigner_name",
            "layer": "variable",
            "anchor_text": ["외국인 성명", "고용예정자"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "position_title",
            "layer": "variable",
            "anchor_text": ["직위", "채용직위"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "annual_salary",
            "layer": "variable",
            "anchor_text": ["연봉", "급여"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 3
        {
            "data_key": "hiring_reason",
            "layer": "narrative",
            "anchor_text": ["채용사유", "고용필요성"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "job_duties",
            "layer": "narrative",
            "anchor_text": ["담당업무", "업무내용"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "expected_contribution",
            "layer": "narrative",
            "anchor_text": ["기대효과"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 8. 귀화동기서 - 시나리오 F (템플릿)
# =============================================================================

NATURALIZATION_MOTIVATION_MAPPING = {
    "template_file": "naturalization_motivation.docx",
    "document_name": "귀화동기서",
    "scenario_id": "F",
    "type": "narrative",
    "fields": [
        # Layer 1
        {
            "data_key": "full_name",
            "layer": "universal",
            "anchor_text": ["신청인", "성명"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "nationality",
            "layer": "universal",
            "anchor_text": ["현재국적", "국적"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 2
        {
            "data_key": "korea_stay_years",
            "layer": "variable",
            "anchor_text": ["거주기간", "체류기간"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "korean_language_level",
            "layer": "variable",
            "anchor_text": ["한국어능력", "어학수준"],
            "strategy": "NEXT_CELL"
        },
        
        # Layer 3
        {
            "data_key": "naturalization_reason",
            "layer": "narrative",
            "anchor_text": ["귀화동기", "귀화사유"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "korea_adaptation",
            "layer": "narrative",
            "anchor_text": ["적응과정", "한국생활"],
            "strategy": "NEXT_CELL"
        },
        {
            "data_key": "contribution_plan",
            "layer": "narrative",
            "anchor_text": ["기여계획", "사회기여"],
            "strategy": "NEXT_CELL"
        },
    ]
}

# =============================================================================
# 전체 매핑 내보내기
# =============================================================================

ALL_DOCUMENT_MAPPINGS = {
    "구직활동계획서": JOB_SEARCH_PLAN_MAPPING,
    "신원보증서": GUARANTEE_LETTER_MAPPING,
    "통합신청서": UNIFIED_APPLICATION_MAPPING,
    "시간제취업 확인서": PART_TIME_WORK_MAPPING,
    "결혼배경 진술서": MARRIAGE_STATEMENT_MAPPING,
    "가족 초청장": FAMILY_INVITATION_MAPPING,
    "고용활용계획서": EMPLOYMENT_PLAN_MAPPING,
    "귀화동기서": NATURALIZATION_MOTIVATION_MAPPING,
}

# 시나리오별 필요 문서 매핑
SCENARIO_DOCUMENTS = {
    "A": ["통합신청서", "구직활동계획서", "신원보증서"],
    "B": ["통합신청서", "시간제취업 확인서", "신원보증서"],
    "C": ["통합신청서", "결혼배경 진술서", "신원보증서"],
    "D": ["통합신청서", "가족 초청장", "신원보증서"],
    "E": ["통합신청서", "고용활용계획서", "신원보증서"],
    "F": ["귀화동기서", "신원보증서"],
}

def get_document_mapping(doc_name: str) -> Dict:
    """문서명으로 매핑 정보 가져오기"""
    return ALL_DOCUMENT_MAPPINGS.get(doc_name, {})

def get_scenario_documents(scenario_id: str) -> List[str]:
    """시나리오별 필요 문서 목록 가져오기"""
    return SCENARIO_DOCUMENTS.get(scenario_id, [])

def get_fields_by_layer(doc_name: str, layer: str) -> List[Dict]:
    """문서의 특정 레이어 필드만 가져오기"""
    mapping = get_document_mapping(doc_name)
    fields = mapping.get("fields", [])
    return [f for f in fields if f.get("layer") == layer]