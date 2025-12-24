# K-Stay Document Template Mapping Guide
# ======================================
# 이 문서는 Word 템플릿과 데이터 필드 간의 매핑을 정의합니다.

"""
📋 문서 데이터 엔지니어링 가이드

각 문서별로 다음 작업이 필요합니다:
1. 하이코리아에서 공식 서식 다운로드
2. .hwp → .docx 변환 (필요시)
3. 템플릿 필드 분석 및 매핑 정의
4. AI 시맨틱 매핑용 라벨 추출
"""

# =============================================================================
# 통합신청서 (별지 제34호) 매핑
# =============================================================================

UNIFIED_APPLICATION_MAPPING = {
    "template_file": "unified_application.docx",
    "sections": {
        "applicant_info": {
            "fields": [
                {"label": "성명 (한글)", "data_key": "name_korean", "layer": "universal"},
                {"label": "성명 (영문)", "data_key": ["surname", "given_name"], "layer": "universal"},
                {"label": "성별", "data_key": "gender", "layer": "universal"},
                {"label": "생년월일", "data_key": "birth_date", "layer": "universal"},
                {"label": "국적", "data_key": "nationality", "layer": "universal"},
                {"label": "여권번호", "data_key": "passport_no", "layer": "universal"},
                {"label": "여권발급일", "data_key": "passport_issue_date", "layer": "universal"},
                {"label": "여권만료일", "data_key": "passport_expiry_date", "layer": "universal"},
                {"label": "외국인등록번호", "data_key": "alien_registration_no", "layer": "universal"},
            ]
        },
        "contact_info": {
            "fields": [
                {"label": "국내 체류지", "data_key": "korea_address", "layer": "universal"},
                {"label": "전화번호", "data_key": "korea_phone", "layer": "universal"},
                {"label": "휴대전화", "data_key": "korea_phone", "layer": "universal"},
                {"label": "이메일", "data_key": "email", "layer": "universal"},
                {"label": "본국 주소", "data_key": "home_country_address", "layer": "universal"},
            ]
        },
        "application_type": {
            "fields": [
                {"label": "신청구분", "data_key": "application_type", "layer": "variable"},
                {"label": "희망 체류자격", "data_key": "desired_visa_type", "layer": "variable"},
                {"label": "희망 체류기간", "data_key": "desired_stay_period", "layer": "variable"},
            ]
        }
    }
}

# =============================================================================
# 구직활동계획서 매핑
# =============================================================================

JOB_SEARCH_PLAN_MAPPING = {
    "template_file": "job_search_plan.docx",
    "sections": {
        "applicant_info": {
            "fields": [
                {"label": "성명", "data_key": ["surname", "given_name"], "layer": "universal"},
                {"label": "국적", "data_key": "nationality", "layer": "universal"},
                {"label": "외국인등록번호", "data_key": "alien_registration_no", "layer": "universal"},
            ]
        },
        "education": {
            "fields": [
                {"label": "최종학력", "data_key": "education_level", "layer": "variable"},
                {"label": "전공", "data_key": "major", "layer": "variable"},
                {"label": "졸업일", "data_key": "graduation_date", "layer": "variable"},
                {"label": "학교명", "data_key": "school_name", "layer": "variable"},
            ]
        },
        "job_search_plan": {
            "fields": [
                {"label": "희망 산업", "data_key": "target_industry", "layer": "variable"},
                {"label": "희망 직무", "data_key": "target_position", "layer": "variable"},
                {"label": "구직활동계획", "data_key": "job_search_plan", "layer": "narrative"},
            ]
        }
    },
    "narrative_section": {
        "field_name": "job_search_plan",
        "min_length": 200,
        "max_length": 2000,
        "ai_validation_rules": [
            "월별 구체적 계획 포함 필수",
            "'취업 확정', '내정' 표현 금지",
            "실현 가능한 계획인지 검증"
        ]
    }
}

# =============================================================================
# 결혼배경 진술서 매핑
# =============================================================================

MARRIAGE_BACKGROUND_MAPPING = {
    "template_file": "marriage_background_statement.docx",
    "sections": {
        "applicant_info": {
            "fields": [
                {"label": "신청인 성명", "data_key": ["surname", "given_name"], "layer": "universal"},
                {"label": "국적", "data_key": "nationality", "layer": "universal"},
                {"label": "생년월일", "data_key": "birth_date", "layer": "universal"},
            ]
        },
        "spouse_info": {
            "fields": [
                {"label": "배우자 성명", "data_key": "spouse_name", "layer": "variable"},
                {"label": "배우자 주민등록번호", "data_key": "spouse_resident_no", "layer": "variable"},
                {"label": "배우자 직업", "data_key": "spouse_occupation", "layer": "variable"},
            ]
        },
        "marriage_info": {
            "fields": [
                {"label": "혼인신고일", "data_key": "marriage_date", "layer": "variable"},
                {"label": "첫 만남", "data_key": "first_meeting_date", "layer": "variable"},
                {"label": "첫 만남 장소", "data_key": "first_meeting_location", "layer": "variable"},
            ]
        },
        "narrative": {
            "fields": [
                {"label": "교제 과정", "data_key": "love_story", "layer": "narrative"},
            ]
        }
    },
    "narrative_section": {
        "field_name": "love_story",
        "min_length": 500,
        "max_length": 3000,
        "ai_validation_rules": [
            "시간순 서술 필수",
            "구체적 에피소드 포함",
            "'위장 결혼', '돈을 받고' 등 의심 표현 절대 금지",
            "진정성 검증"
        ]
    }
}

# =============================================================================
# 고용활용계획서 매핑 (E-7)
# =============================================================================

EMPLOYMENT_PLAN_MAPPING = {
    "template_file": "employment_plan.docx",
    "sections": {
        "company_info": {
            "fields": [
                {"label": "기업명", "data_key": "company_name", "layer": "variable"},
                {"label": "사업자등록번호", "data_key": "company_business_no", "layer": "variable"},
                {"label": "업종", "data_key": "company_industry", "layer": "variable"},
                {"label": "주소", "data_key": "company_address", "layer": "variable"},
            ]
        },
        "foreigner_info": {
            "fields": [
                {"label": "외국인 성명", "data_key": "foreigner_name", "layer": "variable"},
                {"label": "국적", "data_key": "foreigner_nationality", "layer": "variable"},
                {"label": "학력", "data_key": "foreigner_education", "layer": "variable"},
                {"label": "경력", "data_key": "foreigner_experience", "layer": "variable"},
            ]
        },
        "employment_details": {
            "fields": [
                {"label": "직위", "data_key": "position_title", "layer": "variable"},
                {"label": "담당업무", "data_key": "position_duties", "layer": "variable"},
                {"label": "연봉", "data_key": "annual_salary", "layer": "variable"},
            ]
        },
        "narrative": {
            "fields": [
                {"label": "채용 필요성", "data_key": "employment_necessity", "layer": "narrative"},
            ]
        }
    },
    "narrative_section": {
        "field_name": "employment_necessity",
        "min_length": 300,
        "max_length": 2000,
        "ai_validation_rules": [
            "전문성 강조 필수",
            "단순 노무 표현 금지",
            "국내 인력 대체 불가 설명",
            "기대 효과 구체적 서술"
        ]
    }
}

# =============================================================================
# 귀화동기서 매핑
# =============================================================================

NATURALIZATION_MOTIVATION_MAPPING = {
    "template_file": "naturalization_motivation.docx",
    "sections": {
        "applicant_info": {
            "fields": [
                {"label": "성명", "data_key": ["surname", "given_name"], "layer": "universal"},
                {"label": "국적", "data_key": "nationality", "layer": "universal"},
                {"label": "외국인등록번호", "data_key": "alien_registration_no", "layer": "universal"},
            ]
        },
        "residence_info": {
            "fields": [
                {"label": "한국 거주 기간", "data_key": "korea_stay_years", "layer": "variable"},
                {"label": "최초 입국일", "data_key": "first_entry_date", "layer": "variable"},
                {"label": "현재 체류자격", "data_key": "current_visa_type", "layer": "variable"},
            ]
        },
        "narrative": {
            "fields": [
                {"label": "귀화 동기", "data_key": "naturalization_motivation", "layer": "narrative"},
            ]
        }
    },
    "narrative_section": {
        "field_name": "naturalization_motivation",
        "min_length": 500,
        "max_length": 3000,
        "ai_validation_rules": [
            "한국에 대한 진정한 애정 표현",
            "구체적 사회 기여 계획",
            "장기 거주 의지 명시",
            "한국 문화 이해도 표현"
        ]
    }
}

# =============================================================================
# 전체 문서 매핑 목록
# =============================================================================

ALL_DOCUMENT_MAPPINGS = {
    "통합신청서": UNIFIED_APPLICATION_MAPPING,
    "구직활동계획서": JOB_SEARCH_PLAN_MAPPING,
    "결혼배경 진술서": MARRIAGE_BACKGROUND_MAPPING,
    "고용활용계획서": EMPLOYMENT_PLAN_MAPPING,
    "귀화동기서": NATURALIZATION_MOTIVATION_MAPPING,
}

# =============================================================================
# 데이터 레이어 정의
# =============================================================================

DATA_LAYERS = {
    "universal": {
        "description": "불변 정보 - 회원가입 시 1회 입력",
        "source": "users 테이블",
        "ai_intervention": False
    },
    "variable": {
        "description": "가변 정보 - 시나리오별 폼 입력",
        "source": "scenario_submissions.form_data",
        "ai_intervention": False
    },
    "narrative": {
        "description": "사연 정보 - AI가 적극적으로 검토",
        "source": "scenario_submissions.narrative_data",
        "ai_intervention": True,
        "ai_actions": ["validation", "suggestion", "generation"]
    }
}
