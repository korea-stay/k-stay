"""
K-Stay Document Template Mapping Guide
Auto-generated at: 2025-12-30 01:00:49

[데이터 레이어 정의]
- Layer 1 (universal): users 테이블에서 자동 로드 (본인 정보)
- Layer 2 (variable): 시나리오별 추가 폼 입력 (타인 정보 포함)
- Layer 3 (narrative): AI가 검토하는 서술형 데이터

[섹션 Target 정의]
- self: 신청자 본인 → Layer 1 필드 사용
- other_guarantor: 신원보증인 → Layer 2 (guarantor_ prefix)
- other_spouse: 배우자 → Layer 2 (spouse_ prefix)
- other_inviter: 초청인 → Layer 2 (inviter_ prefix)
- other_employer: 고용주 → Layer 2 (employer_ prefix)

[매핑 전략 (Strategy)]
- BELOW_CELL: 앵커 텍스트 아래 셀에 값 입력
- NEXT_CELL: 앵커 텍스트 오른쪽 셀에 값 입력
- APPEND_TO_SAME_CELL: 같은 셀에 값 덧붙이기
- CHECKBOX: 체크박스 선택
- SPLIT_CELLS: 값을 글자별로 분할하여 셀에 입력
"""

from typing import Dict, List, Any

# ======================================================================
# 공통 Value Map
# ======================================================================

GENDER_CHECKBOX_MAP = {
    "Male": ["남", "Male", "M", "남자"],
    "M": ["남", "Male", "M", "남자"],
    "Female": ["여", "Female", "F", "여자"],
    "F": ["여", "Female", "F", "여자"],
}

VALUE_MAPS = {
    "GENDER": GENDER_CHECKBOX_MAP,
}
##사증발급인정신청서##
VISA_ISSUANCE_MAPPING = {
    "template_file": "사증발급인정신청서 (7).docx",
    "document_name": "사증발급인정신청서",
    "type": "form",
    "sections": [
        {
            "section_name": "인적사항",
            "section_name_en": "Personal Details",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "성 Family Name",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "명 Given Names",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "full_name_hanja",
                    "layer": "universal",
                    "anchor_text": "1.2 한자성명 漢字姓名",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "1.3 성별 Sex",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "1.4 생년월일 Date of Birth (yyyy/mm/dd)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "1.5 국적 Nationality",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "birth_country",
                    "layer": "universal",
                    "anchor_text": "1.6 출생국가 Country of Birth",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "national_id_no",
                    "layer": "universal",
                    "anchor_text": "1.7 국가신분증번호 National Identity No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "has_used_other_names",
                    "layer": "variable",
                    "anchor_text": "1.8 이전에 한국에 출입국하였을 때 다른 성명을 사용했는지 여부",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "has_multiple_nationalities",
                    "layer": "variable",
                    "anchor_text": "1.9 복수 국적 여부 Is the the appliant a citizen of more",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "여권정보",
            "section_name_en": "Passport Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "passport_type",
                    "layer": "universal",
                    "anchor_text": "2.1 여권종류 Passport Type",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "passport_type_other",
                    "layer": "variable",
                    "anchor_text": "→ ‘기타’상세내용 If‘Other’, please provide details",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_no",
                    "layer": "universal",
                    "anchor_text": "2.2 여권번호 Passport No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_issuing_country",
                    "layer": "universal",
                    "anchor_text": "2.3 발급국가 Country of Passport",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_place_of_issue",
                    "layer": "variable",
                    "anchor_text": "2.4 발급지 Place of Issue",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "passport_issue_date",
                    "layer": "universal",
                    "anchor_text": "2.5 발급일자 Date of Issue",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_expiry_date",
                    "layer": "universal",
                    "anchor_text": "2.6 기간만료일 Date Of Expiry",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "has_other_passport",
                    "layer": "variable",
                    "anchor_text": "2.7 다른 여권 소지 여부 Does the the applicant have any ot",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "other_passport_type",
                    "layer": "variable",
                    "anchor_text": "a) 여권종류 Passport Type",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "other_passport_no",
                    "layer": "variable",
                    "anchor_text": "b) 여권번호 Passport No.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "other_passport_country",
                    "layer": "variable",
                    "anchor_text": "c) 발급국가 Country of Passport",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "other_passport_expiry",
                    "layer": "variable",
                    "anchor_text": "d) 기간만료일 Date of Expiry",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "연락처",
            "section_name_en": "Contact Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "home_country_address",
                    "layer": "variable",
                    "anchor_text": "3.1 본국 주소 Home Country Address of the Applicant",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "address",
                    "layer": "universal",
                    "anchor_text": "3.2 현 거주지 Current Residential Address",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "phone",
                    "layer": "universal",
                    "anchor_text": "3.3 휴대전화 Cell Phone No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "phone_alt",
                    "layer": "variable",
                    "anchor_text": "3.4 일반전화 Telephone No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "email",
                    "layer": "universal",
                    "anchor_text": "3.5 이메일 E-mail",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "비상시 연락처",
            "section_name_en": "Emergency Contact",
            "target": "other_emergency_contact",
            "target_prefix": "emergency_",
            "fields": [
                {
                    "data_key": "emergency_name",
                    "layer": "variable",
                    "anchor_text": "a) 성명 Full Name in English",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "emergency_country_of_residence",
                    "layer": "variable",
                    "anchor_text": "b) 거주국가 Country of Residence",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "emergency_phone",
                    "layer": "variable",
                    "anchor_text": "c) 전화번호 Telephone No.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "emergency_relationship",
                    "layer": "variable",
                    "anchor_text": "d) 관계 Relationship to the applicant",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "혼인 및 가족사항",
            "section_name_en": "Marital and Family Details",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "marital_status",
                    "layer": "variable",
                    "anchor_text": "4.1 현재 혼인사항 Current Marital Status",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "has_children",
                    "layer": "variable",
                    "anchor_text": "4.3 자녀 유무 Does the applicant have children?",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "children_count",
                    "layer": "variable",
                    "anchor_text": "자녀수 Number of children",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "배우자 인적사항",
            "section_name_en": "Spouse Information",
            "target": "other_spouse",
            "target_prefix": "spouse_",
            "fields": [
                {
                    "data_key": "spouse_surname",
                    "layer": "variable",
                    "anchor_text": "a) 성 Family Name (in English)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "spouse_given_name",
                    "layer": "variable",
                    "anchor_text": "b) 명 Given Names (in English)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "spouse_birth_date",
                    "layer": "variable",
                    "anchor_text": "c) 생년월일 Date of Birth (yyyy/mm/dd)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "spouse_nationality",
                    "layer": "variable",
                    "anchor_text": "d) 국적 Nationality",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "spouse_address",
                    "layer": "variable",
                    "anchor_text": "e) 거주지 Residential Address",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "spouse_phone",
                    "layer": "variable",
                    "anchor_text": "f) 연락처 Contact No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "학력",
            "section_name_en": "Education",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "education_level",
                    "layer": "variable",
                    "anchor_text": "5.1 최종학력 What is the highest degree or level of ed",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "education_other_details",
                    "layer": "variable",
                    "anchor_text": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, please provide detai",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "school_name",
                    "layer": "variable",
                    "anchor_text": "5.2 학교명 Name of School",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "school_location",
                    "layer": "variable",
                    "anchor_text": "5.3 학교 소재지 Location of School(city/province/countr",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "직업 상태",
            "section_name_en": "Employment Status",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "occupation_status",
                    "layer": "variable",
                    "anchor_text": "6.1 직업  Current personal circumstances",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "occupation_other_details",
                    "layer": "variable",
                    "anchor_text": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, please provide detai",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "고용주/회사 정보",
            "section_name_en": "Employer/Company Details",
            "target": "other_employer",
            "target_prefix": "employer_",
            "fields": [
                {
                    "data_key": "employer_name",
                    "layer": "variable",
                    "anchor_text": "a) 회사/기관/학교명 Name of Company/Institute/School",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_position",
                    "layer": "variable",
                    "anchor_text": "b) 직위/과정 Position/Course",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_address",
                    "layer": "variable",
                    "anchor_text": "c) 회사/기관/학교 주소 Address of Company/Institute/School",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_phone",
                    "layer": "variable",
                    "anchor_text": "d) 전화번호 Telephone No.",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "방문정보",
            "section_name_en": "Details of Visit",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "purpose_of_visit",
                    "layer": "variable",
                    "anchor_text": "7.1 입국목적 Purpose of Visit to Korea",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "purpose_other_details",
                    "layer": "variable",
                    "anchor_text": "→ ‘기타’선택 시 상세내용 기재 If ‘Other’ , please provide det",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "intended_stay_period",
                    "layer": "variable",
                    "anchor_text": "7.2 체류예정기간 Intended Period of Stay",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "intended_entry_date",
                    "layer": "variable",
                    "anchor_text": "7.3 입국예정일 Intended Date of Entry",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "address_in_korea",
                    "layer": "variable",
                    "anchor_text": "7.4 체류예정지(호텔 포함) Address in Korea (including hotel",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "contact_in_korea_phone",
                    "layer": "variable",
                    "anchor_text": "7.5 한국 내 연락처 Contact No. in Korea",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "past_korea_visits",
                    "layer": "variable",
                    "anchor_text": "7.6 과거 5년간 한국을 방문한 경력",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "past_travel_country",
                    "layer": "variable",
                    "anchor_text": "국가명 Name of Country (in English)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "past_travel_purpose",
                    "layer": "variable",
                    "anchor_text": "방문목적 Purpose of Visit",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "past_travel_period",
                    "layer": "variable",
                    "anchor_text": "방문기간 Period of Stay  (yyyy/mm/dd)~ (yyyy/mm/dd)",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "국내 체류 가족",
            "section_name_en": "Family Staying in Korea",
            "target": "other_family",
            "target_prefix": "family_korea_",
            "fields": [
                {
                    "data_key": "family_korea_name",
                    "layer": "variable",
                    "anchor_text": "성명 Full name in English",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "family_korea_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일 Date of Birth  (yyyy/mm/dd)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "family_korea_nationality",
                    "layer": "variable",
                    "anchor_text": "국적 Nationality",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "family_korea_relationship",
                    "layer": "variable",
                    "anchor_text": "관계 Relationship to the applicant",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "동반입국 가족",
            "section_name_en": "Accompanying Family",
            "target": "other_family",
            "target_prefix": "companion_",
            "fields": [
                {
                    "data_key": "companion_name",
                    "layer": "variable",
                    "anchor_text": "성명 Full name in English",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "companion_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일 Date of Birth  (yyyy/mm/dd)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "companion_nationality",
                    "layer": "variable",
                    "anchor_text": "국적 Nationality",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "companion_relationship",
                    "layer": "variable",
                    "anchor_text": "관계 Relationship to the invitee",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "서류 작성 도움 여부",
            "section_name_en": "Assistance With This Form",
            "target": "other_assistant",
            "target_prefix": "assistant_",
            "fields": [
                {
                    "data_key": "assistant_name",
                    "layer": "variable",
                    "anchor_text": "8.1 이 신청서를 작성하는데 다른 사람의 도움을 받았습니까?",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "assistant_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일 Date of Birth  (yyyy/mm/dd)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "assistant_phone",
                    "layer": "variable",
                    "anchor_text": "연락처 Phone No.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "assistant_relationship",
                    "layer": "variable",
                    "anchor_text": "관계 Relationship to  the applicant",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "초청 정보",
            "section_name_en": "Details of Invitation",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "inviter_exists",
                    "layer": "variable",
                    "anchor_text": "9.1 초청인/초청회사 Is there anyone inviting the applican",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_name",
                    "layer": "variable",
                    "anchor_text": "a) 초청인/초청회사명 Name of inviting person/organization",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_birth_or_business_no",
                    "layer": "variable",
                    "anchor_text": "b) 생년월일/사업자등록번호 Date of Birth / Business Registrat",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_relationship",
                    "layer": "variable",
                    "anchor_text": "c) 관계 Relationship to the",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_address",
                    "layer": "variable",
                    "anchor_text": "d) 주소 Address",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "inviter_phone",
                    "layer": "variable",
                    "anchor_text": "e) 전화번호 Phone No.",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "신청인(초청인) 서명",
            "section_name_en": "Applicant (Inviting Person) Signature",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "application_date",
                    "layer": "variable",
                    "anchor_text": "신청일자 (년. 월. 일) DATE OF APPLICATION (yyyy/mm/dd)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_applicant_name",
                    "layer": "variable",
                    "anchor_text": "신청인(초청인) 성명 NAME OF APPLICANT(INVITING PERSON)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_signature",
                    "layer": "variable",
                    "anchor_text": "신청인(초청인) 서명(인) SIGNATURE(SEAL) OF APPLICANT(INVITI",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 통합신청서
# ======================================================================

UNIFIED_APPLICATION_MAPPING = {
    "template_file": "통합신청서(신고서) (7).docx",
    "document_name": "통합신청서",
    "type": "form",
    "sections": [
        {
            "section_name": "신청 정보",
            "section_name_en": "Application Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "성 Surname",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "명 Given names",
                    "strategy": "BELOW_CELL"
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
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "[ ]남 M [ ]여 F",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "국 적 Nationality",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "alien_registration_no",
                    "layer": "universal",
                    "anchor_text": "외국인등록번호  Foreign Resident Registration No.",
                    "strategy": "SPLIT_CELLS"
                },
                {
                    "data_key": "passport_no",
                    "layer": "universal",
                    "anchor_text": "여권 번호 Passport No.",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "passport_issue_date",
                    "layer": "universal",
                    "anchor_text": "여권 발급일자 Passport Issue Date",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "passport_expiry_date",
                    "layer": "universal",
                    "anchor_text": "여권 유효기간 Passport Expiry Date",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "address_korea",
                    "layer": "variable",
                    "anchor_text": "대한민국 내 주소 Address In Korea",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "korea_phone",
                    "layer": "universal",
                    "anchor_text": "전화 번호 Telephone No.",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "korea_phone",
                    "layer": "universal",
                    "anchor_text": "휴대 전화 Cell phone No.",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "home_country_address",
                    "layer": "variable",
                    "anchor_text": "본국 주소 Address In Home Country",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "school_name",
                    "layer": "variable",
                    "anchor_text": "학교 이름 Name of School",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "current_workplace_name",
                    "layer": "variable",
                    "anchor_text": "원 근무처 Current Workplace",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "new_workplace_name",
                    "layer": "variable",
                    "anchor_text": "예정 근무처 New Workplace",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "annual_income_amount",
                    "layer": "variable",
                    "anchor_text": "연 소득금액 Annual Income Amount",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "occupation",
                    "layer": "variable",
                    "anchor_text": "직업 Occupation",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "intended_reentry_period",
                    "layer": "variable",
                    "anchor_text": "재입국 신청 기간 Intended Period Of Reentry",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "email",
                    "layer": "universal",
                    "anchor_text": "전자우편 E-Mail",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "refund_bank_account_no",
                    "layer": "variable",
                    "anchor_text": "반환용 계좌번호(외국인등록 및 외국인등록증 재발급 신청 시에만 기재) Refund Bank",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "application_date",
                    "layer": "variable",
                    "anchor_text": "신청일 Date of application",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
    ]
}




# ======================================================================
# 고용사유서
# ======================================================================

EMPLOYMENT_REASON_MAPPING = {
    "template_file": "고용사유서 (7).docx",
    "document_name": "고용사유서",
    "type": "form",
    "sections": [
        {
            "section_name": "1. 고용 기업 사항",
            "section_name_en": "Employer Company Details",
            "target": "other_employer",
            "target_prefix": "employer_",
            "fields": [
                {
                    "data_key": "employer_company_name",
                    "layer": "variable",
                    "anchor_text": "회사명",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_business_registration_no",
                    "layer": "variable",
                    "anchor_text": "사업자등록번호 (법인등록번호)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_representative_name",
                    "layer": "variable",
                    "anchor_text": "대표자명",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_address",
                    "layer": "variable",
                    "anchor_text": "회사 주소",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_capital_amount",
                    "layer": "variable",
                    "anchor_text": "자본금",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_total_sales",
                    "layer": "variable",
                    "anchor_text": "총매출액",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_total_liabilities",
                    "layer": "variable",
                    "anchor_text": "부채총액",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_operating_profit",
                    "layer": "variable",
                    "anchor_text": "영업이익",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_num_employees",
                    "layer": "variable",
                    "anchor_text": "상시종업원수",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_num_foreign_professionals",
                    "layer": "variable",
                    "anchor_text": "외국전문인력수",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_company_intro",
                    "layer": "narrative",
                    "anchor_text": "회사 및 사업(업무) 소개",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "2. 전문외국인력의 이력 개요",
            "section_name_en": "Overview of Professional Foreign Worker's Profile",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "full_name",
                    "layer": "universal",
                    "anchor_text": "성 명 (영문)",
                    "strategy": "APPEND_TO_SAME_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "성 별",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "국 적",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "생년월일",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_no",
                    "layer": "universal",
                    "anchor_text": "여권번호",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "address",
                    "layer": "universal",
                    "anchor_text": "(현지)주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "phone",
                    "layer": "universal",
                    "anchor_text": "전화번호",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "education_school_name",
                    "layer": "variable",
                    "anchor_text": "학 교 명",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "education_degree",
                    "layer": "variable",
                    "anchor_text": "학 위",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "education_major",
                    "layer": "variable",
                    "anchor_text": "전 공",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "education_graduation_year",
                    "layer": "variable",
                    "anchor_text": "졸업년도",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "experience_company",
                    "layer": "variable",
                    "anchor_text": "업 체 명",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "experience_period",
                    "layer": "variable",
                    "anchor_text": "재직기간",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "experience_field",
                    "layer": "variable",
                    "anchor_text": "근무분야",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "experience_position",
                    "layer": "variable",
                    "anchor_text": "직 위",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employment_period",
                    "layer": "variable",
                    "anchor_text": "고용(예정)기간",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "sojourn_status",
                    "layer": "variable",
                    "anchor_text": "체류자격 (직종코드)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "job_field",
                    "layer": "variable",
                    "anchor_text": "근무(예정)분야",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_title",
                    "layer": "variable",
                    "anchor_text": "직 위",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "workplace",
                    "layer": "variable",
                    "anchor_text": "근무(예정)지",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "salary_and_benefits",
                    "layer": "variable",
                    "anchor_text": "급여 및 처우",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "3. 고용사유 및 인력활용계획",
            "section_name_en": "Employment Reasons and Utilization Plan",
            "target": "other_employer",
            "target_prefix": "employer_",
            "fields": [
                {
                    "data_key": "employer_employment_reason",
                    "layer": "narrative",
                    "anchor_text": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 ",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_tech_import_effect",
                    "layer": "narrative",
                    "anchor_text": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_utilization_plan",
                    "layer": "narrative",
                    "anchor_text": "3) 활용계획",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_other_notes",
                    "layer": "narrative",
                    "anchor_text": "4) 기타사항",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 구직활동계획서
# ======================================================================

JOB_SEARCH_PLAN_MAPPING = {
    "template_file": "구직활동계획서 (7).docx",
    "document_name": "구직활동계획서",
    "type": "form",
    "sections": [
        {
            "section_name": "1. 个人事项 / Personal Information",
            "section_name_en": "Personal Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "Surname(英文)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "Given names(英文)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "full_name_hanja",
                    "layer": "universal",
                    "anchor_text": "中文姓名",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "性 别 Gender",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "出生年月日/外国人登录证号码 Date of Birth or Alien Registration",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "alien_registration_no",
                    "layer": "universal",
                    "anchor_text": "出生年月日/外国人登录证号码 Date of Birth or Alien Registration",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "国籍 Nationality",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "university_name",
                    "layer": "variable",
                    "anchor_text": "毕业学校 Name of University or College",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "major_degree",
                    "layer": "variable",
                    "anchor_text": "专业 & 学位 (预毕业) Major & Degree (Graduate-to-be)",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "work_experience",
                    "layer": "variable",
                    "anchor_text": "工作经验 Work Experience",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "2. 求职事项 / Desired Employment Detail",
            "section_name_en": "Desired Employment Detail",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "occupational_category",
                    "layer": "variable",
                    "anchor_text": "业种 Occupational Category",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "company_name",
                    "layer": "variable",
                    "anchor_text": "单位名称 Name of company",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "expected_salary",
                    "layer": "variable",
                    "anchor_text": "期望薪资 Salary",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "3. 求职计划 / Plans for Employment-seeking Activities",
            "section_name_en": "Plans for Employment-seeking Activities",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "job_search_plan_month1",
                    "layer": "narrative",
                    "anchor_text": "第一月 / 1st month",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_search_plan_month2",
                    "layer": "narrative",
                    "anchor_text": "第二月 / 2nd month",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_search_plan_month3",
                    "layer": "narrative",
                    "anchor_text": "第三月 / 3rd month",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_search_plan_month4",
                    "layer": "narrative",
                    "anchor_text": "第四月 / 4th month",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_search_plan_month5",
                    "layer": "narrative",
                    "anchor_text": "第五月 / 5th month",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "job_search_plan_month6",
                    "layer": "narrative",
                    "anchor_text": "第六月 /6th month",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "4. 滞留费用及支付方式 / Financing Plan for Living Costs",
            "section_name_en": "Financing Plan for Living Costs",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "living_cost_cash",
                    "layer": "variable",
                    "anchor_text": "现金 Cash",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "living_cost_deposit",
                    "layer": "variable",
                    "anchor_text": "存款 Deposit",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "living_cost_credit_card",
                    "layer": "variable",
                    "anchor_text": "信用卡 Credit card",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "living_cost_remittance",
                    "layer": "variable",
                    "anchor_text": "汇款 Remittance",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 가족초청장
# ======================================================================

FAMILY_INVITATION_MAPPING = {
    "template_file": "결혼이민자의 부모 등 가족 초청장(F-1-5 비자 신청) (7).docx",
    "document_name": "가족초청장",
    "type": "form",
    "sections": [
        {
            "section_name": "초청인의 인적사항",
            "section_name_en": "Inviter's Personal Information",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "inviter_name",
                    "layer": "variable",
                    "anchor_text": "1.1 성명",
                    "strategy": "APPEND_TO_SAME_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "inviter_gender",
                    "layer": "variable",
                    "anchor_text": "1.2 성별",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "inviter_nationality",
                    "layer": "variable",
                    "anchor_text": "1.3 국적(외국인인 경우 체류자격도 함께 기재)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_birth_date",
                    "layer": "variable",
                    "anchor_text": "1.4 생년월일 년 월 일",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_address",
                    "layer": "variable",
                    "anchor_text": "1.5 주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_home_phone",
                    "layer": "variable",
                    "anchor_text": "1.6 집 전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_mobile_phone",
                    "layer": "variable",
                    "anchor_text": "1.7 휴대전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_email",
                    "layer": "variable",
                    "anchor_text": "1.8 전자우편(e-mail) 주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        # 2. 초청인의 가족사항
        {
            "section_name": "초청인의 가족사항",
            "target": "other_inviter",
            "fields": [
                {
                    "data_key": "household_members",
                    "anchor_text": "2. 초청인의 가족사항",
                    "strategy": "TABLE_ROWS",
                    "table_config": {
                        "header_row_text": ["관계", "성명", "국적", "생년월일", "연락처"],
                        "start_row_offset": 1,
                        "max_rows": 10,
                        "columns": [
                            {"key": "relationship", "col_index": 0},
                            {"key": "name", "col_index": 1},
                            {"key": "nationality", "col_index": 2},
                            {"key": "birth_date", "col_index": 3},
                            {"key": "phone", "col_index": 4},
                        ]
                    }
                }
            ]
        },

        # 4. 초청 전력 (헤더와 인덱스 정밀 수정)
        {
            "section_name": "초청 전력",
            "target": "other_inviter",
            "fields": [
                {
                    "data_key": "invitation_history",
                    "anchor_text": "4. 초청 전력",
                    "strategy": "TABLE_ROWS",
                    "table_config": {
                        "must_contain": ["초청횟수", "체류"],
                        # [중요] '초청 횟수'는 이 표에만 있는 단어이므로 반드시 포함
                        "header_row_text": ["관계", "성명", "국적", "생년월일", "초청 횟수", "체류"],
                        "start_row_offset": 1,
                        "max_rows": 5,
                        "columns": [
                            {"key": "relationship", "col_index": 0},  # 관계
                            {"key": "name", "col_index": 1},          # 성명(영문 성명) - 키 이름 'name'으로 통일
                            {"key": "nationality", "col_index": 2},   # 국적
                            {"key": "birth_date", "col_index": 3},    # 생년월일
                            {"key": "invite_count", "col_index": 4},  # 초청 횟수
                            {"key": "is_staying", "col_index": 5},    # 체류 여부
                        ]
                    }
                }
            ]
        },

        # 6. 피초청인 가족관계 (헤더와 인덱스 정밀 수정)
        {
            "section_name": "피초청인 인적사항 및 가족관계",
            "target": "self",
            "fields": [
                {
                    "data_key": "invitee_family_members",
                    "anchor_text": "6. 피초청인 인적사항 및 가족관계",
                    "strategy": "TABLE_ROWS",
                    "table_config": {
                        # [중요] '거주지'는 이 표에만 있는 단어이므로 반드시 포함
                        "must_contain": ["거주지"],
                        "header_row_text": ["관계", "성명", "국적", "거주지", "생년월일", "연락처"],
                        "start_row_offset": 1,
                        "max_rows": 8,
                        "columns": [
                            # 실제 문서 순서: 관계 -> 성명 -> 국적 -> 거주지 -> 생년월일 -> 연락처
                            {"key": "relationship", "col_index": 0},  # 관계
                            {"key": "name", "col_index": 1},          # 성명
                            {"key": "nationality", "col_index": 2},   # 국적
                            {"key": "residence", "col_index": 3},     # 거주지 (순서 주의! 4번 아님)
                            {"key": "birth_date", "col_index": 4},    # 생년월일
                            {"key": "phone", "col_index": 5},         # 연락처
                        ]
                    }
                }
            ]
        },
        {
            "section_name": "초청인의 가족사항",
            "section_name_en": "Inviter's Family Information",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "inviter_household_members",
                    "layer": "variable",
                    "anchor_text": "2.1 초청인의 동거 가족(외국인 포함)과 관련된 정보를 아래 서식에 맞게 빠짐없이 모두",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "초청 목적(사유)",
            "section_name_en": "Purpose of Invitation",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "invitation_reason",
                    "layer": "variable",
                    "anchor_text": "3.1아래 초청 사유 중 해당하는 곳에 √표를 하시기 바랍니다.",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "inviter_activity_status",
                    "layer": "narrative",
                    "anchor_text": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "current_caregiving_status",
                    "layer": "narrative",
                    "anchor_text": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "invitee_expected_role",
                    "layer": "narrative",
                    "anchor_text": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "invitee_support_plan",
                    "layer": "narrative",
                    "anchor_text": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "초청 전력",
            "section_name_en": "Prior Invitation History",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "prior_invitation_history",
                    "layer": "variable",
                    "anchor_text": "4.1 초청인은 과거 결혼이민자(초청인 본인 또는 배우자)의 부모 등 가족을 방문동거(F-",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "prior_invited_person_details",
                    "layer": "variable",
                    "anchor_text": "4.2 위 “4.1” 항목에 “예”라고 답하였다면, 초청한 사람(피초청인)의 인적사항 정보",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "법위반 사실 유무",
            "section_name_en": "Record of Law Violations",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "inviter_law_violation_record",
                    "layer": "variable",
                    "anchor_text": "5.1 초청인은 과거 ｢출입국관리법｣ 제7조의2, 제12조의3, 제18조제3항부터 제5항,",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "invited_foreigner_violation_record",
                    "layer": "variable",
                    "anchor_text": "5.2 과거 초청인의 초청을 받고 입국한 외국인 중, 국내법을 위반하여, ｢출입국관리법｣에",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
            ]
        },
        {
            "section_name": "피초청인 인적사항 및 가족관계",
            "section_name_en": "Invitee's Information and Family Relationship",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "relationship_to_inviter",
                    "layer": "variable",
                    "anchor_text": "6.1 초청인과 피초청(사증발급 신청인)의 중 해당하는 곳에 √표를 하시기 바랍니다.",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "family_members_info",
                    "layer": "variable",
                    "anchor_text": "6.2 피초청인과 그의 배우자, 부모, 자녀, 형제자매의 관련 정보를 아래 서식에 맞게 빠",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "previous_visit_korea",
                    "layer": "variable",
                    "anchor_text": "6.3 피초청인은 과거 한국에 방문한 적이 있습니까(해당하는 곳에 √표를 하시기 바랍니다)",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "previous_violation_korea",
                    "layer": "variable",
                    "anchor_text": "6.4 위 “6.3” 항목에 “예”라고 답하였다면, 피초청인은 과거 국내법을 위반하여 벌금",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
            ]
        },
        {
            "section_name": "기타 관련 정보",
            "section_name_en": "Other Relevant Information",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "additional_info",
                    "layer": "narrative",
                    "anchor_text": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "서류 작성 시 도움 여부",
            "section_name_en": "Assistance in Filling the Form",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "help_received",
                    "layer": "variable",
                    "anchor_text": "9.1 이 신청서를 작성하는데 다른 사람의 도움을 받았습니까(해당하는 곳에 √표를 하시기",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
            ]
        },
    ]
}

# ======================================================================
# 결혼배경진술서
# ======================================================================

MARRIAGE_STATEMENT_MAPPING = {
    "template_file": "영주자격자의 배우자 결혼배경진술서(F-2-3) (7).docx",
    "document_name": "결혼배경진술서",
    "type": "form",
    "sections": [
        {
            "section_name": "1. 인적사항",
            "section_name_en": "1. Personal Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "1.1 여권에 기재된 성명 / Your full name (as shown in your passport)  ⟶ Family name",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "1.1 여권에 기재된 성명 / Your full name (as shown in your passport)  ⟶ Given name",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "1.2 성별 / Sex",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "surname_native",
                    "layer": "variable",
                    "anchor_text": "1.3 현지 언어로 성명을 기재하시오 / Your full name written in your native language  ⟶ Family name",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "given_name_native",
                    "layer": "variable",
                    "anchor_text": "1.3 현지 언어로 성명을 기재하시오 / Your full name written in your native language  ⟶ Given name",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "used_other_names",
                    "layer": "variable",
                    "anchor_text": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "other_names_explanation",
                    "layer": "narrative",
                    "anchor_text": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "2. 가족 및 혼인관계",
            "section_name_en": "2. Your Family and Spouse",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "family_knows_marriage",
                    "layer": "variable",
                    "anchor_text": "2.1 신청인의 부모, 형제, 자매가 혼인에 대해 알고 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "ever_been_married",
                    "layer": "variable",
                    "anchor_text": "2.2 신청인은 과거에 혼인한 적이 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "has_other_spouse_currently",
                    "layer": "variable",
                    "anchor_text": "2.3 현재 배우자 이외에 혼인관계를 유지하고 있는 다른 배우자가 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "has_children_from_previous_marriage",
                    "layer": "variable",
                    "anchor_text": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "children_from_previous_marriage_details",
                    "layer": "narrative",
                    "anchor_text": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "3. 과거 입국경력",
            "section_name_en": "3. History of Past Entries",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "visited_korea_before",
                    "layer": "variable",
                    "anchor_text": "3.1 신청인은 과거 한국에 방문한 적이 있습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "immigration_issues_history",
                    "layer": "variable",
                    "anchor_text": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "immigration_issues_details",
                    "layer": "narrative",
                    "anchor_text": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "4. 서류작성 시 도움 여부",
            "section_name_en": "4. Assistance With This Form",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "received_assistance",
                    "layer": "variable",
                    "anchor_text": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                    "strategy": "CHECKBOX",
                    "value_map": "YES_NO"
                },
                {
                    "data_key": "assistance_details",
                    "layer": "narrative",
                    "anchor_text": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 시간제취업확인서
# ======================================================================

PART_TIME_WORK_MAPPING = {
    "template_file": "시간제취업확인서 (7).docx",
    "document_name": "시간제취업확인서",
    "type": "form",
    "sections": [
        {
            "section_name": "대상자",
            "section_name_en": "Applicant",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "full_name",
                    "layer": "universal",
                    "anchor_text": "성명",
                    "strategy": "NEXT_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "alien_registration_no",
                    "layer": "universal",
                    "anchor_text": "외 국 인 등록번 호",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "department_major",
                    "layer": "variable",
                    "anchor_text": "학과(전 공 )",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "semester",
                    "layer": "variable",
                    "anchor_text": "이수학기",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "phone",
                    "layer": "variable",
                    "anchor_text": "전 화번 호",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "email",
                    "layer": "universal",
                    "anchor_text": "e-m ai l",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "취업 예정 근무처",
            "section_name_en": "Expected Workplace",
            "target": "other_employer",
            "target_prefix": "employer_",
            "fields": [
                {
                    "data_key": "employer_company_name",
                    "layer": "variable",
                    "anchor_text": "업	체	명",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_business_registration_no",
                    "layer": "variable",
                    "anchor_text": "사 업	자 등 록 번 호",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_industry",
                    "layer": "variable",
                    "anchor_text": "업 종",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_address",
                    "layer": "variable",
                    "anchor_text": "주	소",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_phone",
                    "layer": "variable",
                    "anchor_text": "전 화 번 호",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employment_period",
                    "layer": "variable",
                    "anchor_text": "취 업 기 간",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_wage_hourly",
                    "layer": "variable",
                    "anchor_text": "급 여 ( 시 급 )",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "employer_weekday_total_hours",
                    "layer": "variable",
                    "anchor_text": "평  일 : 총	시간",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_weekend_total_hours",
                    "layer": "variable",
                    "anchor_text": "주말 : 총	시간",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employer_working_hours_mon",
                    "layer": "variable",
                    "anchor_text": "월.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_tue",
                    "layer": "variable",
                    "anchor_text": "화.",
                    "index": 5,
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_wed",
                    "layer": "variable",
                    "anchor_text": "수.",
                    "index": 5,
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_thu",
                    "layer": "variable",
                    "anchor_text": "목.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_fri",
                    "layer": "variable",
                    "anchor_text": "금.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_sat",
                    "layer": "variable",
                    "anchor_text": "토.",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_working_hours_sun",
                    "layer": "variable",
                    "anchor_text": "일.",
                    "index": 11,
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "유학생 담당자 확인란",
            "section_name_en": "Confirmation by University Officer",
            "target": "other_university_officer",
            "target_prefix": "university_officer_",
            "fields": [
                {
                    "data_key": "university_officer_ieqas",
                    "layer": "variable",
                    "anchor_text": "인증대 학 여부",
                    "strategy": "CHECKBOX"
                },
                {
                    "data_key": "university_officer_position_phone",
                    "layer": "variable",
                    "anchor_text": "직위 (연락처)",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 불법체류취업방지서약서
# ======================================================================

ILLEGAL_WORK_PREVENTION_MAPPING = {
    "template_file": "불법체류 취업 방지 서약서(F-1-5) (7).docx",
    "document_name": "불법체류취업방지서약서",
    "type": "form",
    "sections": [
        # ============================================
        # 초청인 = 서비스 사용자 본인 (user_data에서 가져옴)
        # ============================================
        {
            "section_name": "초청인",
            "section_name_en": "Inviter",
            "target": "self",              # ★ user_data 사용
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "full_name",    # user_data의 full_name
                    "layer": "universal",
                    "anchor_text": "성",
                    "strategy": "TABLE_CELL",
                    "column_index": 1
                },
                {
                    "data_key": "birth_date",   # user_data의 birth_date
                    "layer": "universal",
                    "anchor_text": "생년월일",
                    "strategy": "TABLE_CELL",
                    "column_index": 1
                },
                {
                    "data_key": "korea_address", # user_data의 korea_address
                    "layer": "universal",
                    "anchor_text": "주",
                    "strategy": "TABLE_CELL",
                    "column_index": 1
                },
                {
                    "data_key": "korea_phone",   # user_data의 korea_phone
                    "layer": "universal",
                    "anchor_text": "연",
                    "strategy": "TABLE_CELL",
                    "column_index": 1
                },
            ]
        },
        
        # ============================================
        # 피초청인 = 별도 입력 (form_data에서 가져옴)
        # ============================================
        {
            "section_name": "피초청인",
            "section_name_en": "Invitee",
            "target": "other_invitee",
            "target_prefix": "invitee_",
            "fields": [
                {
                    "data_key": "invitee_name",
                    "layer": "variable",
                    "anchor_text": "성",
                    "strategy": "TABLE_CELL",
                    "column_index": 2
                },
                {
                    "data_key": "invitee_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일",
                    "strategy": "TABLE_CELL",
                    "column_index": 2
                },
                {
                    "data_key": "invitee_address",
                    "layer": "variable",
                    "anchor_text": "주",
                    "strategy": "TABLE_CELL",
                    "column_index": 2
                },
                {
                    "data_key": "invitee_phone",
                    "layer": "variable",
                    "anchor_text": "연",
                    "strategy": "TABLE_CELL",
                    "column_index": 2
                },
            ]
        },
    ]
}
# ======================================================================
# 신원보증서
# ======================================================================

GUARANTEE_LETTER_MAPPING = {
    "template_file": "신원보증서(한글) (7).docx",
    "document_name": "신원보증서",
    "type": "form",
    "sections": [
        {
            "section_name": "피보증 외국인",
            "section_name_en": "Guaranteed Foreigner",
            "table_match_text": "피보증외국인",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "성",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "명",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "full_name_hanja",
                    "layer": "universal",
                    "anchor_text": "漢字",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "생년월일",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "성별",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "국적",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "passport_no",
                    "layer": "universal",
                    "anchor_text": "여권번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "korea_address",
                    "layer": "universal",
                    "anchor_text": "대한민국 주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "korea_phone",
                    "layer": "universal",
                    "anchor_text": "전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "stay_purpose",
                    "layer": "variable",
                    "anchor_text": "체류목적",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "신원보증인",
            "section_name_en": "Guarantor",
            "table_match_text": "신원보증인",
            "target": "other_guarantor",
            "target_prefix": "guarantor_",
            "fields": [
                {
                    "data_key": "guarantor_name",
                    "layer": "variable",
                    "anchor_text": "성명",
                    "strategy": "APPEND_TO_SAME_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "guarantor_name_hanja",
                    "layer": "variable",
                    "anchor_text": "漢字",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_nationality",
                    "layer": "variable",
                    "anchor_text": "국적",
                    "index": 40,
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_gender",
                    "layer": "variable",
                    "anchor_text": "성별",
                    "strategy": "CHECKBOX",
                    "value_map": "GENDER"
                },
                {
                    "data_key": "guarantor_passport_or_birth",
                    "layer": "variable",
                    "anchor_text": "여권번호 또는 생년월일",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_phone",
                    "layer": "variable",
                    "anchor_text": "전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_address",
                    "layer": "variable",
                    "anchor_text": "주소",
                    "index": 40,
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_relationship",
                    "layer": "variable",
                    "anchor_text": "피보증인과의 관계",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_employer",
                    "layer": "variable",
                    "anchor_text": "근무처",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_position",
                    "layer": "variable",
                    "anchor_text": "직위",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_employer_address",
                    "layer": "variable",
                    "anchor_text": "근무처 주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_note",
                    "layer": "variable",
                    "anchor_text": "비고",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_guarantee_period",
                    "layer": "variable",
                    "anchor_text": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "guarantor_signature_date",
                    "layer": "variable",
                    "anchor_text": "년              월           일장",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "guarantor_signature",
                    "layer": "variable",
                    "anchor_text": "(서명 또는 인)",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 귀화허가신청서
# ======================================================================

NATURALIZATION_APPLICATION_MAPPING = {
    "template_file": "귀화허가신청서 (7).docx",
    "document_name": "귀화허가신청서",
    "type": "form",
    "sections": [
        # ============================================================
        # 섹션 1: 신청인 인적사항
        # ============================================================
        {
            "section_name": "신청인 인적사항",
            "section_name_en": "Applicant Personal Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "현재 국적",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "birth_place",
                    "layer": "variable",
                    "anchor_text": "출생지(국가 및 도시명)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "full_name",
                    "layer": "universal",
                    "anchor_text": "성명(한글)",
                    "strategy": "APPEND_TO_SAME_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "full_name_en",
                    "layer": "variable",
                    "anchor_text": "성명(영문)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "alien_registration_no",
                    "layer": "universal",
                    "anchor_text": "외국인등록번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "korea_phone",
                    "layer": "universal",
                    "anchor_text": "전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "email",
                    "layer": "universal",
                    "anchor_text": "전자우편(E-mail)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "korea_address",
                    "layer": "universal",
                    "anchor_text": "주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "intended_registered_domicile",
                    "layer": "variable",
                    "anchor_text": "예정 등록기준지",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        # ============================================================
        # 섹션 2: 귀화 유형 체크박스
        # ============================================================
        {
            "section_name": "귀화 유형",
            "section_name_en": "Naturalization Type",
            "target": "self",
            "target_prefix": "",
            "fields": [
                # -----------------------------------------------------
                # 일반귀화
                # -----------------------------------------------------
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["「민법」상 성년이며 영주자격(F5)을 가지고 있는 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "general",
                        "value": "general_permanent_resident",
                        "parent_anchor": "일반귀화"
                    }
                },
                # -----------------------------------------------------
                # 간이귀화
                # -----------------------------------------------------
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["부 또는 모가 대한민국의 국민이었던 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "simplified",
                        "value": "simplified_parent_korean",
                        "parent_anchor": "간이귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["대한민국에서 출생한 사람으로서 부 또는 모가 대한민국에서 출생한 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "simplified",
                        "value": "simplified_born_in_korea",
                        "parent_anchor": "간이귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["대한민국 국민의 양자(養子)로서 입양 당시 대한민국의 「민법」상 성년이었던 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "simplified",
                        "value": "simplified_adopted",
                        "parent_anchor": "간이귀화"
                    }
                },
                # -----------------------------------------------------
                # 혼인귀화
                # -----------------------------------------------------
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["배우자와 혼인한 상태로 대한민국에 2년 이상 거주한 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "marriage",
                        "value": "marriage_2years",
                        "parent_anchor": "혼인귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["배우자와 혼인한 후 3년이 지나고 혼인한 상태로 대한민국에 1년 이상 거주한 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "marriage",
                        "value": "marriage_3years_1year",
                        "parent_anchor": "혼인귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["배우자의 사망", "실종 그 밖에 자신에게 책임이 없는 사유로 혼인생활 유지가 불가한"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "marriage",
                        "value": "marriage_spouse_unavailable",
                        "parent_anchor": "혼인귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["배우자와의 혼인에 따라 출생한 미성년의 자녀를 양육하고 있거나 양육할 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "marriage",
                        "value": "marriage_raising_child",
                        "parent_anchor": "혼인귀화"
                    }
                },
                # -----------------------------------------------------
                # 특별귀화
                # -----------------------------------------------------
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["부 또는 모가 대한민국의 국민인 사람, 입양 당시 「민법」상 미성년이었던 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "value": "special_minor_adoptee",
                        "parent_anchor": "특별귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["대한민국에 특별한 공로가 있는 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "value": "special_merit",
                        "parent_anchor": "특별귀화",
                        "has_sub_options": True
                    }
                },
                # 특별귀화 - 공로자 하위 옵션
                {
                    "data_key": "special_merit_type",
                    "layer": "variable",
                    "anchor_text": ["독립유공자"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "parent_value": "special_merit",
                        "value": "special_merit_independence",
                        "is_nested": True
                    }
                },
                {
                    "data_key": "special_merit_type",
                    "layer": "variable",
                    "anchor_text": ["국가유공자"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "parent_value": "special_merit",
                        "value": "special_merit_national",
                        "is_nested": True
                    }
                },
                {
                    "data_key": "special_merit_type",
                    "layer": "variable",
                    "anchor_text": ["국익기여자"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "parent_value": "special_merit",
                        "value": "special_merit_national_interest",
                        "is_nested": True
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "layer": "variable",
                    "anchor_text": ["과학", "경제", "문화", "체육 등 특정 분야에서 매우 우수한 능력을 보유한 사람"],
                    "strategy": "HIERARCHICAL_CHECKBOX",
                    "checkbox_config": {
                        "category": "special",
                        "value": "special_excellence",
                        "parent_anchor": "특별귀화"
                    }
                },
            ]
        },
        # ============================================================
        # 섹션 3: 수반취득
        # ============================================================
        {
            "section_name": "수반취득",
            "section_name_en": "Accompanying Acquisition",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "accompanying_acquisition",
                    "layer": "variable",
                    "anchor_text": ["만 19세 미만의 자녀"],
                    "strategy": "CHECKBOX_WITH_VALUE",
                    "checkbox_config": {
                        "value_field": "accompanying_children_count",
                        "value_placeholder": "(   )",
                        "description": "명에 대하여 신청인과 함께 국적 취득을 신청합니다."
                    }
                }
            ]
        },
    ]
}



# ======================================================================
# 외국인배우자초청장
# ======================================================================

SPOUSE_INVITATION_MAPPING = {
    "template_file": "외국인 배우자 초청장 (7).docx",
    "document_name": "외국인배우자초청장",
    "type": "form",
    "sections": [
        {
            "section_name": "초청인 인적사항",
            "section_name_en": "Inviter Information",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "inviter_home_phone",
                    "layer": "variable",
                    "anchor_text": "1.6 집 전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_phone",
                    "layer": "variable",
                    "anchor_text": "1.7 휴대전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "inviter_email",
                    "layer": "variable",
                    "anchor_text": "1.8 전자우편 주소",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "소개인 정보",
            "section_name_en": "Introducer Information",
            "target": "other_introducer",
            "target_prefix": "introducer_",
            "fields": [
                {
                    "data_key": "introducer_name",
                    "layer": "variable",
                    "anchor_text": "2.3.1 소개인의 성명  (중개업체의 경우 상호명도 기재합니다)",
                    "strategy": "APPEND_TO_SAME_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "introducer_birth_date",
                    "layer": "variable",
                    "anchor_text": "2.3.2 소개인의 생년월일  (중개업체의 경우 사업자등록번호도 기재합니다)",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "introducer_nationality",
                    "layer": "variable",
                    "anchor_text": "2.3.3 소개인의 국적",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "introducer_phone",
                    "layer": "variable",
                    "anchor_text": "2.3.4 소개인의 전화번호",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "혼인 관련 참고인 명단",
            "section_name_en": "Marriage References",
            "target": "other_reference",
            "target_prefix": "reference_",
            "fields": [
                {
                    "data_key": "reference_name",
                    "layer": "variable",
                    "anchor_text": "성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "reference_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "reference_phone",
                    "layer": "variable",
                    "anchor_text": "연락처",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "reference_relationship",
                    "layer": "variable",
                    "anchor_text": "초청인과의 관계",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "가족 연락처 및 혼인 사실 인지 여부",
            "section_name_en": "Family Contacts and Marriage Awareness",
            "target": "other_family",
            "target_prefix": "family_",
            "fields": [
                {
                    "data_key": "family_name",
                    "layer": "variable",
                    "anchor_text": "성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "family_phone",
                    "layer": "variable",
                    "anchor_text": "연락처",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "family_knows_marriage",
                    "layer": "variable",
                    "anchor_text": "혼인사실을 알고 있는지 여부",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "배우자 정보",
            "section_name_en": "Spouse Information",
            "target": "other_spouse",
            "target_prefix": "spouse_",
            "fields": [
                {
                    "data_key": "spouse_name",
                    "layer": "variable",
                    "anchor_text": "배우자의 성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "spouse_birth_date",
                    "layer": "variable",
                    "anchor_text": "생년월일",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "spouse_nationality",
                    "layer": "variable",
                    "anchor_text": "배우자의 국적",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "marriage_period",
                    "layer": "variable",
                    "anchor_text": "혼인기간",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "가구 인원 현황",
            "section_name_en": "Household Members",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "household_lineal_count",
                    "layer": "variable",
                    "anchor_text": "초청인과 주민등록표상 세대를 같이 하는 직계가족 (부모, 조부모, 과거 혼인관계에서 출생한",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "household_total_count",
                    "layer": "variable",
                    "anchor_text": "합 계",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "초청인 직장 정보",
            "section_name_en": "Employer Information",
            "target": "other_employer",
            "target_prefix": "employer_",
            "fields": [
                {
                    "data_key": "employer_company_name",
                    "layer": "variable",
                    "anchor_text": "직장명",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_address",
                    "layer": "variable",
                    "anchor_text": "주소",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employer_name",
                    "layer": "variable",
                    "anchor_text": "고용주 성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "employer_phone",
                    "layer": "variable",
                    "anchor_text": "고용주(직장) 연락처",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "근무 경력 및 소득",
            "section_name_en": "Employment History and Income",
            "target": "other_employer",
            "target_prefix": "employment_",
            "fields": [
                {
                    "data_key": "employment_employer_name",
                    "layer": "variable",
                    "anchor_text": "직장명",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "employment_period",
                    "layer": "variable",
                    "anchor_text": "근무한 기간",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "employment_income_pre_tax",
                    "layer": "variable",
                    "anchor_text": "세전 소득",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "사업체(자영업) 정보",
            "section_name_en": "Business (Self-employed) Information",
            "target": "other_employer",
            "target_prefix": "business_",
            "fields": [
                {
                    "data_key": "business_name",
                    "layer": "variable",
                    "anchor_text": "명칭",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "business_address",
                    "layer": "variable",
                    "anchor_text": "주 소",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "business_phone",
                    "layer": "variable",
                    "anchor_text": "전화번호",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "기타 소득",
            "section_name_en": "Other Income",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "other_income_type",
                    "layer": "variable",
                    "anchor_text": "소득의 종류 (부동산 임대, 이자, 배당, 연금 중 택일)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "other_income_amount",
                    "layer": "variable",
                    "anchor_text": "세전 소득",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "재산 정보",
            "section_name_en": "Assets Information",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "asset_type_1",
                    "layer": "variable",
                    "anchor_text": "재산의 종류 (예금, 보험, 증권, 채권, 부동산 중 택일)",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "asset_amount_1",
                    "layer": "variable",
                    "anchor_text": "재산의 현금가액",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "asset_total_amount",
                    "layer": "variable",
                    "anchor_text": "합 계",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "소득/재산 합계",
            "section_name_en": "Income/Assets Summary",
            "target": "other_inviter",
            "target_prefix": "inviter_",
            "fields": [
                {
                    "data_key": "earned_income_total",
                    "layer": "variable",
                    "anchor_text": "근로소득",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "business_income_total",
                    "layer": "variable",
                    "anchor_text": "사업소득",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "other_income_total",
                    "layer": "variable",
                    "anchor_text": "그 밖의 소득",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "asset_converted_total",
                    "layer": "variable",
                    "anchor_text": "재산의 환산금액",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "income_assets_grand_total",
                    "layer": "variable",
                    "anchor_text": "합 계",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "참고인 명단",
            "section_name_en": "Reference List",
            "target": "other_reference",
            "target_prefix": "reference_",
            "fields": [
                {
                    "data_key": "reference_person_name",
                    "layer": "variable",
                    "anchor_text": "성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "reference_person_age",
                    "layer": "variable",
                    "anchor_text": "연령",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "reference_person_relationship",
                    "layer": "variable",
                    "anchor_text": "초청인과의 관계",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "reference_person_phone",
                    "layer": "variable",
                    "anchor_text": "연락처",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
        {
            "section_name": "추가 참고인",
            "section_name_en": "Additional References",
            "target": "other_reference",
            "target_prefix": "witness_",
            "fields": [
                {
                    "data_key": "witness_name",
                    "layer": "variable",
                    "anchor_text": "성명",
                    "strategy": "BELOW_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "witness_address",
                    "layer": "variable",
                    "anchor_text": "주소",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "witness_phone",
                    "layer": "variable",
                    "anchor_text": "연락처",
                    "strategy": "BELOW_CELL"
                },
                {
                    "data_key": "witness_relationship",
                    "layer": "variable",
                    "anchor_text": "초청인과의 관계",
                    "strategy": "BELOW_CELL"
                },
            ]
        },
    ]
}

TREATMENT_PLEDGE_MAPPING = {
    "template_file": "치료예정서약서.docx",
    "document_name": "치료예정서약서",
    "type": "form",
    "sections": [
        {
            "section_name": "인적사항",
            "section_name_en": "Personal Details",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "국 적",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "full_name",
                    "layer": "universal",
                    "anchor_text": "성 명",
                    "strategy": "NEXT_CELL",
                    "formatter": "FULL_NAME_KR"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "생년월일",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "성 별",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "korea_address",
                    "layer": "variable",
                    "anchor_text": "한국 내 주소",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "disease_name",
                    "layer": "variable",
                    "anchor_text": "질 병 명",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "보호자 정보",
            "section_name_en": "Guardian Information",
            "target": "other_guardian",
            "target_prefix": "guardian_",
            "fields": [
                {
                    "data_key": "guardian_name",
                    "layer": "variable",
                    "anchor_text": "보호자 (지인,친척 등)",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "guardian_phone",
                    "layer": "variable",
                    "anchor_text": "보호자연락처",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
        {
            "section_name": "병원 정보",
            "section_name_en": "Hospital Information",
            "target": "other_hospital",
            "target_prefix": "hospital_",
            "fields": [
                {
                    "data_key": "hospital_name",
                    "layer": "variable",
                    "anchor_text": "치료 예정병원",
                    "strategy": "NEXT_CELL"
                },
                {
                    "data_key": "hospital_address_contact",
                    "layer": "variable",
                    "anchor_text": "병원 주소  및 연락처",
                    "strategy": "NEXT_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 입국허가신청서
# ======================================================================

ENTRY_PERMIT_APPLICATION_MAPPING = {
    "template_file": "입국허가신청서.docx",
    "document_name": "입국허가신청서",
    "type": "form",
    "sections": [
        {
            "section_name": "신청인 정보",
            "section_name_en": "Applicant Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "surname",
                    "layer": "universal",
                    "anchor_text": "성 Surname",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "given_name",
                    "layer": "universal",
                    "anchor_text": "명 Given Names",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "chinese_name",
                    "layer": "universal",
                    "anchor_text": "한자성명",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "full_name_hanja",
                    "layer": "universal",
                    "anchor_text": "한자성명",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "birth_date",
                    "layer": "universal",
                    "anchor_text": "생년월일 Date of Birth",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "gender",
                    "layer": "universal",
                    "anchor_text": "성별 Sex",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "nationality",
                    "layer": "universal",
                    "anchor_text": "국적 Nationality",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "birth_place",
                    "layer": "variable",
                    "anchor_text": "출생지 Place of Birth",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "address",
                    "layer": "variable",
                    "anchor_text": "주소 Address",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "address_in_korea",
                    "layer": "variable",
                    "anchor_text": "국내체류지 Address in Korea",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "occupation_and_title",
                    "layer": "variable",
                    "anchor_text": "직장 직위 Occupation ＆ Title",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "여권 정보",
            "section_name_en": "Passport Information",
            "target": "self",
            "target_prefix": "passport_",
            "fields": [
                {
                    "data_key": "passport_no",
                    "layer": "universal",
                    "anchor_text": "번호 No.",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "issue_date",
                    "layer": "variable",
                    "anchor_text": "발급일 Issued date",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "expiration_date",
                    "layer": "variable",
                    "anchor_text": "만료일 Expiration date",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "place_of_issue",
                    "layer": "variable",
                    "anchor_text": "발급지 Place of issue",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
        {
            "section_name": "입국/체류 정보",
            "section_name_en": "Entry and Stay Information",
            "target": "self",
            "target_prefix": "",
            "fields": [
                {
                    "data_key": "purpose_of_entry",
                    "layer": "variable",
                    "anchor_text": "입국목적 Purpose of Entry",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "desired_length_of_stay",
                    "layer": "variable",
                    "anchor_text": "체류예정기간 Desired lengh of stay",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "reason_arriving_without_visa",
                    "layer": "narrative",
                    "anchor_text": "사증없이 도착한 이유  Reason for arriving without a visa",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
                {
                    "data_key": "application_date",
                    "layer": "variable",
                    "anchor_text": "신청일 Date of application",
                    "strategy": "APPEND_TO_SAME_CELL"
                },
            ]
        },
    ]
}

# ======================================================================
# 전체 매핑
# ======================================================================

ALL_DOCUMENT_MAPPINGS = {
    "통합신청서": UNIFIED_APPLICATION_MAPPING,
    "사증발급인정신청서": VISA_ISSUANCE_MAPPING,
    "고용사유서": EMPLOYMENT_REASON_MAPPING,
    "구직활동계획서": JOB_SEARCH_PLAN_MAPPING,
    "가족초청장": FAMILY_INVITATION_MAPPING,
    "치료예정서약서": TREATMENT_PLEDGE_MAPPING,
    "입국허가신청서": ENTRY_PERMIT_APPLICATION_MAPPING,
    "결혼배경진술서": MARRIAGE_STATEMENT_MAPPING,
    "시간제취업확인서": PART_TIME_WORK_MAPPING,
    "불법체류취업방지서약서": ILLEGAL_WORK_PREVENTION_MAPPING,
    "신원보증서": GUARANTEE_LETTER_MAPPING,
    "귀화허가신청서": NATURALIZATION_APPLICATION_MAPPING,
    "외국인배우자초청장": SPOUSE_INVITATION_MAPPING,
}

# 시나리오별 필요 문서
SCENARIO_DOCUMENTS = {
    "A": ['통합신청서', '구직활동계획서', '신원보증서'],
    "B": ['통합신청서', '시간제취업확인서', '신원보증서'],
    "C": ['통합신청서', '결혼배경진술서', '외국인배우자초청장', '신원보증서'],
    "D": ['가족초청장', '불법체류취업방지서약서', '신원보증서'],
    "E": ['사증발급인정신청서', '고용사유서', '신원보증서'],
    "G": ['치료예정서약서', '입국허가신청서', '신원보증서'],
    "F": ['귀화허가신청서', '신원보증서'],
}


# ======================================================================
# 유틸리티 함수
# ======================================================================

def get_document_mapping(doc_name: str) -> Dict:
    """문서명으로 매핑 정보 조회"""
    return ALL_DOCUMENT_MAPPINGS.get(doc_name, {})

def get_scenario_documents(scenario_id: str) -> List[str]:
    """시나리오별 필요 문서 목록 조회"""
    return SCENARIO_DOCUMENTS.get(scenario_id, [])

def get_fields_by_target(doc_name: str, target: str) -> List[Dict]:
    """특정 target의 필드만 조회 (self, other_guarantor 등)"""
    mapping = get_document_mapping(doc_name)
    result = []
    for section in mapping.get("sections", []):
        if section.get("target") == target:
            result.extend(section.get("fields", []))
    return result

def get_fields_by_layer(doc_name: str, layer: str) -> List[Dict]:
    """특정 layer의 필드만 조회"""
    mapping = get_document_mapping(doc_name)
    result = []
    for section in mapping.get("sections", []):
        for field in section.get("fields", []):
            if field.get("layer") == layer:
                result.append(field)
    return result

def get_all_layer2_fields_for_scenario(scenario_id: str) -> Dict[str, List[Dict]]:
    """시나리오에 필요한 모든 Layer 2 필드를 target별로 그룹화하여 반환"""
    docs = get_scenario_documents(scenario_id)
    result = {}
    for doc_name in docs:
        mapping = get_document_mapping(doc_name)
        for section in mapping.get("sections", []):
            target = section.get("target", "self")
            if target != "self":
                if target not in result:
                    result[target] = {
                        "section_name": section.get("section_name", ""),
                        "section_name_en": section.get("section_name_en", ""),
                        "fields": []
                    }
                # 중복 제거하며 추가
                existing_keys = [f["data_key"] for f in result[target]["fields"]]
                for field in section.get("fields", []):
                    if field["data_key"] not in existing_keys:
                        result[target]["fields"].append(field)
    return result