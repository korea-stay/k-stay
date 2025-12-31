"""
K-Stay Configuration Settings
Auto-generated at: 2025-12-30 01:00:49

이 파일은 자동 생성되었습니다.
- Layer 1: 사용자 기본 정보 (users 테이블)
- Layer 2: 시나리오별 추가 입력 필드 (타인 정보 포함)
- Layer 3: 서술형 필드 (AI 검토 대상)
"""

import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple

# ======================================================================
# 🔑 API KEYS
# ======================================================================

def get_secret(key: str, default: str = "") -> str:
    """Streamlit secrets에서 값 가져오기"""
    try:
        return st.secrets.get(key, default)
    except:
        return default

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

# ======================================================================
# 🏷️ data_key → Label 매핑 (UI 표시용)
# ======================================================================

DATA_KEY_LABEL_MAP = {
    # 기본 개인정보
    "name": ("성명", "Name"),
    "full_name": ("성명", "Full Name"),
    "surname": ("성", "Surname"),
    "given_name": ("이름", "Given Name"),
    "hanja": ("한자", "Chinese Characters"),
    "birth_date": ("생년월일", "Date of Birth"),
    "gender": ("성별", "Gender"),
    "nationality": ("국적", "Nationality"),
    "phone": ("전화번호", "Phone"),
    "address": ("주소", "Address"),
    "occupation": ("직업", "Occupation"),
    "workplace": ("근무처", "Workplace"),
    "position": ("직위", "Position"),
    "workplace_address": ("근무처 주소", "Workplace Address"),
    "workplace_phone": ("근무처 전화번호", "Workplace Phone"),
    "relationship": ("관계", "Relationship"),
    "email": ("이메일", "Email"),
    # 여권 관련
    "passport_no": ("여권번호", "Passport No."),
    "passport_issue_date": ("여권 발급일", "Passport Issue Date"),
    "passport_expiry_date": ("여권 만료일", "Passport Expiry Date"),
    # 외국인등록
    "alien_registration_no": ("외국인등록번호", "Alien Registration No."),
    # 보증 관련
    "guarantee_period": ("보증기간", "Guarantee Period"),
    "guarantee_amount": ("보증금액", "Guarantee Amount"),
    # 기타
    "remarks": ("비고", "Remarks"),
    "note": ("비고", "Note"),
}

# Target별 prefix와 그룹명
TARGET_INFO = {
    "other_guarantor": {
        "prefix": "guarantor_",
        "group_name": "신원보증인 정보",
        "group_name_en": "Guarantor Information"
    },
    "other_spouse": {
        "prefix": "spouse_",
        "group_name": "배우자 정보",
        "group_name_en": "Spouse Information"
    },
    "other_inviter": {
        "prefix": "inviter_",
        "group_name": "초청인 정보",
        "group_name_en": "Inviter Information"
    },
    "other_invitee": {
        "prefix": "invitee_",
        "group_name": "피초청인 정보",
        "group_name_en": "Invitee Information"
    },
    "other_employer": {
        "prefix": "employer_",
        "group_name": "고용주 정보",
        "group_name_en": "Employer Information"
    },
    "other_family": {
        "prefix": "family_",
        "group_name": "가족 정보",
        "group_name_en": "Family Information"
    },
}

def get_label_for_data_key(data_key: str, target: str = "self") -> Tuple[str, str]:
    """
    data_key에서 사용자 친화적 label 생성
    Returns: (label_kr, label_en)
    """
    base_key = data_key
    target_info = TARGET_INFO.get(target, {})
    prefix = target_info.get("prefix", "")
    
    if prefix and data_key.startswith(prefix):
        base_key = data_key[len(prefix):]
    
    if base_key in DATA_KEY_LABEL_MAP:
        label_kr, label_en = DATA_KEY_LABEL_MAP[base_key]
        if target != "self" and target in TARGET_INFO:
            group_kr = TARGET_INFO[target]["group_name"].replace(" 정보", "")
            group_en = TARGET_INFO[target]["group_name_en"].replace(" Information", "")
            return (f"{group_kr} {label_kr}", f"{group_en} {label_en}")
        return (label_kr, label_en)
    
    readable = base_key.replace("_", " ").title()
    return (readable, readable)

# ======================================================================
# 📊 LAYER 1: Universal Facts (본인 정보)
# ======================================================================

LAYER1_UNIVERSAL_FIELDS = [
    {
        "data_key": "email",
        "label": "이메일",
        "label_en": "Email",
        "type": "text",
        "category": "account"
    },
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
        "data_key": "full_name",
        "label": "성명",
        "label_en": "Full Name",
        "type": "text",
        "category": "personal"
    },
    {
        "data_key": "full_name_hanja",
        "label": "한자 성명",
        "label_en": "Name in Chinese Characters",
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
    {
        "data_key": "occupation",
        "label": "직업",
        "label_en": "Occupation",
        "type": "text",
        "category": "personal"
    },
    {
        "data_key": "stay_purpose",
        "label": "체류목적",
        "label_en": "Purpose of Stay",
        "type": "text",
        "category": "visa"
    },
]

LAYER1_KEYS = [f["data_key"] for f in LAYER1_UNIVERSAL_FIELDS]

# ======================================================================
# 📊 LAYER 2: Variable Facts (타인 정보, 시나리오별 추가 정보)
# ======================================================================

LAYER2_VARIABLE_FIELDS = {
    "A": {
        "scenario_name": "구직 준비",
        "scenario_name_en": "Job Seeking",
        "visa_type": "D-10",
        "field_groups": [
            {
                "target": "self",
                "group_name": "신청인 추가 정보",
                "group_name_en": "Applicant Additional Info",
                "fields": [
                    {
                        "data_key": "address_korea",
                        "label": "대한민국 내 주소 Address In Korea",
                        "label_en": "Address Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "home_country_address",
                        "label": "본국 주소 Address In Home Country",
                        "label_en": "Home Country Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_status",
                        "label": "미취학[],  초[ ],     중[ ],   고[ ]",
                        "label_en": "School Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_name",
                        "label": "학교 이름 Name of School",
                        "label_en": "School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_type",
                        "label": "교육청 인가[], 교육청 비인가, 대안학교[] Accr",
                        "label_en": "School Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "current_workplace_name",
                        "label": "원 근무처 Current Workplace",
                        "label_en": "Current Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "new_workplace_name",
                        "label": "예정 근무처 New Workplace",
                        "label_en": "New Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "annual_income_amount",
                        "label": "연 소득금액 Annual Income Amount",
                        "label_en": "Annual Income Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation",
                        "label": "직업 Occupation",
                        "label_en": "Occupation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_reentry_period",
                        "label": "재입국 신청 기간 Intended Period Of R",
                        "label_en": "Intended Reentry Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "refund_bank_account_no",
                        "label": "반환용 계좌번호(외국인등록 및 외국인등록증 재발급 신청",
                        "label_en": "Refund Bank Account No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "application_date",
                        "label": "신청일 Date of application",
                        "label_en": "Application Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "applicant_signature",
                        "label": "신청인 서명 또는 인 Signature/Seal",
                        "label_en": "Applicant Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_applicant_signature",
                        "label": "신청인 Applicant",
                        "label_en": "Consent Applicant Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_spouse_signature",
                        "label": "신청인의 배우자 Spouse of applicant",
                        "label_en": "Consent Spouse Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_parent_signature",
                        "label": "신청인의 부 또는 모 Father/Mother of a",
                        "label_en": "Consent Parent Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "university_name",
                        "label": "毕业学校 Name of University or Col",
                        "label_en": "University Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "major_degree",
                        "label": "专业 & 学位 (预毕业) Major & Degree (",
                        "label_en": "Major Degree",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "work_experience",
                        "label": "工作经验 Work Experience",
                        "label_en": "Work Experience",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupational_category",
                        "label": "业种 Occupational Category",
                        "label_en": "Occupational Category",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "company_name",
                        "label": "单位名称 Name of company",
                        "label_en": "Company Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "expected_salary",
                        "label": "期望薪资 Salary",
                        "label_en": "Expected Salary",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "living_cost_cash",
                        "label": "现金 Cash",
                        "label_en": "Living Cost Cash",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "living_cost_deposit",
                        "label": "存款 Deposit",
                        "label_en": "Living Cost Deposit",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "living_cost_credit_card",
                        "label": "信用卡 Credit card",
                        "label_en": "Living Cost Credit Card",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "living_cost_remittance",
                        "label": "汇款 Remittance",
                        "label_en": "Living Cost Remittance",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
    "B": {
        "scenario_name": "아르바이트",
        "scenario_name_en": "Part-time Work",
        "visa_type": "시간제 취업",
        "field_groups": [
            {
                "target": "self",
                "group_name": "신청인 추가 정보",
                "group_name_en": "Applicant Additional Info",
                "fields": [
                    {
                        "data_key": "address_korea",
                        "label": "대한민국 내 주소 Address In Korea",
                        "label_en": "Address Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "home_country_address",
                        "label": "본국 주소 Address In Home Country",
                        "label_en": "Home Country Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_status",
                        "label": "미취학[],  초[ ],     중[ ],   고[ ]",
                        "label_en": "School Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_name",
                        "label": "학교 이름 Name of School",
                        "label_en": "School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_type",
                        "label": "교육청 인가[], 교육청 비인가, 대안학교[] Accr",
                        "label_en": "School Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "current_workplace_name",
                        "label": "원 근무처 Current Workplace",
                        "label_en": "Current Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "new_workplace_name",
                        "label": "예정 근무처 New Workplace",
                        "label_en": "New Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "annual_income_amount",
                        "label": "연 소득금액 Annual Income Amount",
                        "label_en": "Annual Income Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation",
                        "label": "직업 Occupation",
                        "label_en": "Occupation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_reentry_period",
                        "label": "재입국 신청 기간 Intended Period Of R",
                        "label_en": "Intended Reentry Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "refund_bank_account_no",
                        "label": "반환용 계좌번호(외국인등록 및 외국인등록증 재발급 신청",
                        "label_en": "Refund Bank Account No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "application_date",
                        "label": "신청일 Date of application",
                        "label_en": "Application Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "applicant_signature",
                        "label": "신청인 서명 또는 인 Signature/Seal",
                        "label_en": "Applicant Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_applicant_signature",
                        "label": "신청인 Applicant",
                        "label_en": "Consent Applicant Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_spouse_signature",
                        "label": "신청인의 배우자 Spouse of applicant",
                        "label_en": "Consent Spouse Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "consent_parent_signature",
                        "label": "신청인의 부 또는 모 Father/Mother of a",
                        "label_en": "Consent Parent Signature",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "department_major",
                        "label": "학과(전 공 )",
                        "label_en": "Department Major",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "semester",
                        "label": "이수학기",
                        "label_en": "Semester",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "phone",
                        "label": "전 화번 호",
                        "label_en": "Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_employer",
                "group_name": "취업 예정 근무처",
                "group_name_en": "Expected Workplace",
                "fields": [
                    {
                        "data_key": "employer_company_name",
                        "label": "업	체	명",
                        "label_en": "Employer Company Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_business_registration_no",
                        "label": "사 업	자 등 록 번 호",
                        "label_en": "Employer Business Registration No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_industry",
                        "label": "업 종",
                        "label_en": "Employer Industry",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_address",
                        "label": "주	소",
                        "label_en": "Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_phone",
                        "label": "전 화 번 호",
                        "label_en": "Employer Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employment_period",
                        "label": "취 업 기 간",
                        "label_en": "Employment Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_wage_hourly",
                        "label": "급 여 ( 시 급 )",
                        "label_en": "Wage Hourly",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_weekday_total_hours",
                        "label": "평  일 : 총	시간",
                        "label_en": "Weekday Total Hours",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_weekend_total_hours",
                        "label": "주말 : 총	시간",
                        "label_en": "Weekend Total Hours",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_mon",
                        "label": "월",
                        "label_en": "Working Hours Mon",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_tue",
                        "label": "화",
                        "label_en": "Working Hours Tue",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_wed",
                        "label": "수",
                        "label_en": "Working Hours Wed",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_thu",
                        "label": "목",
                        "label_en": "Working Hours Thu",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_fri",
                        "label": "금",
                        "label_en": "Working Hours Fri",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_sat",
                        "label": "토",
                        "label_en": "Working Hours Sat",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_working_hours_sun",
                        "label": "일",
                        "label_en": "Working Hours Sun",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_university_officer",
                "group_name": "유학생 담당자 확인란",
                "group_name_en": "Confirmation by University Officer",
                "fields": [
                    {
                        "data_key": "university_officer_ieqas",
                        "label": "인증대 학 여부",
                        "label_en": "University Officer Ieqas",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "university_officer_position_phone",
                        "label": "직위 (연락처)",
                        "label_en": "University Officer Position Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
    "C": {
        "scenario_name": "결혼 이민",
        "scenario_name_en": "Marriage Immigration",
        "visa_type": "F-6",
        "field_groups": [
            {
                "target": "self",
                "group_name": "신청인 추가 정보",
                "group_name_en": "Applicant Additional Info",
                "fields": [
                    {
                        "data_key": "address_korea",
                        "label": "대한민국 내 주소 Address In Korea",
                        "label_en": "Address Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "home_country_address",
                        "label": "본국 주소 Address In Home Country",
                        "label_en": "Home Country Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_name",
                        "label": "학교 이름 Name of School",
                        "label_en": "School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "current_workplace_name",
                        "label": "원 근무처 Current Workplace",
                        "label_en": "Current Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "new_workplace_name",
                        "label": "예정 근무처 New Workplace",
                        "label_en": "New Workplace Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "annual_income_amount",
                        "label": "연 소득금액 Annual Income Amount",
                        "label_en": "Annual Income Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation",
                        "label": "직업 Occupation",
                        "label_en": "Occupation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_reentry_period",
                        "label": "재입국 신청 기간 Intended Period Of R",
                        "label_en": "Intended Reentry Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "refund_bank_account_no",
                        "label": "반환용 계좌번호(외국인등록 및 외국인등록증 재발급 신청",
                        "label_en": "Refund Bank Account No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "application_date",
                        "label": "신청일 Date of application",
                        "label_en": "Application Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "surname_native",
                        "label": "1.3 현지 언어로 성명을 기재하시오 / Your fu",
                        "label_en": "Surname Native",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "given_name_native",
                        "label": "1.3 현지 언어로 성명을 기재하시오 / Your fu",
                        "label_en": "Given Name Native",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "used_other_names",
                        "label": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                        "label_en": "Used Other Names",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_knows_marriage",
                        "label": "2.1 신청인의 부모, 형제, 자매가 혼인에 대해 알고",
                        "label_en": "Family Knows Marriage",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "ever_been_married",
                        "label": "2.2 신청인은 과거에 혼인한 적이 있습니까?",
                        "label_en": "Ever Been Married",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_other_spouse_currently",
                        "label": "2.3 현재 배우자 이외에 혼인관계를 유지하고 있는 다",
                        "label_en": "Has Other Spouse Currently",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_children_from_previous_marriage",
                        "label": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니",
                        "label_en": "Has Children From Previous Marriage",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "visited_korea_before",
                        "label": "3.1 신청인은 과거 한국에 방문한 적이 있습니까?",
                        "label_en": "Visited Korea Before",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "immigration_issues_history",
                        "label": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 ",
                        "label_en": "Immigration Issues History",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "received_assistance",
                        "label": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았",
                        "label_en": "Received Assistance",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_inviter",
                "group_name": "초청인 인적사항",
                "group_name_en": "Inviter Information",
                "fields": [
                    {
                        "data_key": "inviter_home_phone",
                        "label": "1.6 집 전화번호",
                        "label_en": "Inviter Home Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_phone",
                        "label": "1.7 휴대전화번호",
                        "label_en": "Inviter Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_email",
                        "label": "1.8 전자우편 주소",
                        "label_en": "Inviter Email",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "household_lineal_count",
                        "label": "초청인과 주민등록표상 세대를 같이 하는 직계가족 (부모",
                        "label_en": "Household Lineal Count",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "household_total_count",
                        "label": "합 계",
                        "label_en": "Household Total Count",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_income_type",
                        "label": "소득의 종류 (부동산 임대, 이자, 배당, 연금 중 택",
                        "label_en": "Other Income Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_income_amount",
                        "label": "세전 소득",
                        "label_en": "Other Income Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "asset_type_1",
                        "label": "재산의 종류 (예금, 보험, 증권, 채권, 부동산 중 ",
                        "label_en": "Asset Type 1",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "asset_amount_1",
                        "label": "재산의 현금가액",
                        "label_en": "Asset Amount 1",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "asset_total_amount",
                        "label": "합 계",
                        "label_en": "Asset Total Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "earned_income_total",
                        "label": "근로소득",
                        "label_en": "Earned Income Total",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "business_income_total",
                        "label": "사업소득",
                        "label_en": "Business Income Total",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_income_total",
                        "label": "그 밖의 소득",
                        "label_en": "Other Income Total",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "asset_converted_total",
                        "label": "재산의 환산금액",
                        "label_en": "Asset Converted Total",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "income_assets_grand_total",
                        "label": "합 계",
                        "label_en": "Income Assets Grand Total",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_introducer",
                "group_name": "소개인 정보",
                "group_name_en": "Introducer Information",
                "fields": [
                    {
                        "data_key": "introducer_name",
                        "label": "2.3.1 소개인의 성명  (중개업체의 경우 상호명도 ",
                        "label_en": "Introducer Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "introducer_birth_date",
                        "label": "2.3.2 소개인의 생년월일  (중개업체의 경우 사업자",
                        "label_en": "Introducer Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "introducer_nationality",
                        "label": "2.3.3 소개인의 국적",
                        "label_en": "Introducer Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "introducer_phone",
                        "label": "2.3.4 소개인의 전화번호",
                        "label_en": "Introducer Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_reference",
                "group_name": "혼인 관련 참고인 명단",
                "group_name_en": "Marriage References",
                "fields": [
                    {
                        "data_key": "reference_name",
                        "label": "성명",
                        "label_en": "Reference Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_birth_date",
                        "label": "생년월일",
                        "label_en": "Reference Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_phone",
                        "label": "연락처",
                        "label_en": "Reference Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_relationship",
                        "label": "초청인과의 관계",
                        "label_en": "Reference Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_person_name",
                        "label": "성명",
                        "label_en": "Reference Person Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_person_age",
                        "label": "연령",
                        "label_en": "Reference Person Age",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_person_relationship",
                        "label": "초청인과의 관계",
                        "label_en": "Reference Person Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "reference_person_phone",
                        "label": "연락처",
                        "label_en": "Reference Person Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "witness_name",
                        "label": "성명",
                        "label_en": "Witness Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "witness_address",
                        "label": "주소",
                        "label_en": "Witness Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "witness_phone",
                        "label": "연락처",
                        "label_en": "Witness Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "witness_relationship",
                        "label": "초청인과의 관계",
                        "label_en": "Witness Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_family",
                "group_name": "가족 연락처 및 혼인 사실 인지 여부",
                "group_name_en": "Family Contacts and Marriage Awareness",
                "fields": [
                    {
                        "data_key": "family_name",
                        "label": "성명",
                        "label_en": "Family Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_phone",
                        "label": "연락처",
                        "label_en": "Family Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_knows_marriage",
                        "label": "혼인사실을 알고 있는지 여부",
                        "label_en": "Family Knows Marriage",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_spouse",
                "group_name": "배우자 정보",
                "group_name_en": "Spouse Information",
                "fields": [
                    {
                        "data_key": "spouse_name",
                        "label": "배우자의 성명",
                        "label_en": "Spouse Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_birth_date",
                        "label": "생년월일",
                        "label_en": "Spouse Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_nationality",
                        "label": "배우자의 국적",
                        "label_en": "Spouse Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "marriage_period",
                        "label": "혼인기간",
                        "label_en": "Marriage Period",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_employer",
                "group_name": "초청인 직장 정보",
                "group_name_en": "Employer Information",
                "fields": [
                    {
                        "data_key": "employer_company_name",
                        "label": "직장명",
                        "label_en": "Employer Company Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_address",
                        "label": "주소",
                        "label_en": "Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_name",
                        "label": "고용주 성명",
                        "label_en": "Employer Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_phone",
                        "label": "고용주(직장) 연락처",
                        "label_en": "Employer Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employment_employer_name",
                        "label": "직장명",
                        "label_en": "Employment Employer Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employment_period",
                        "label": "근무한 기간",
                        "label_en": "Employment Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employment_income_pre_tax",
                        "label": "세전 소득",
                        "label_en": "Employment Income Pre Tax",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "business_name",
                        "label": "명칭",
                        "label_en": "Business Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "business_address",
                        "label": "주 소",
                        "label_en": "Business Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "business_phone",
                        "label": "전화번호",
                        "label_en": "Business Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
    "D": {
        "scenario_name": "가족 초청",
        "scenario_name_en": "Family Invitation",
        "visa_type": "F-1-5",
        "field_groups": [
            {
                "target": "other_inviter",
                "group_name": "초청인의 인적사항",
                "group_name_en": "Inviter's Personal Information",
                "fields": [
                    {
                        "data_key": "inviter_name",
                        "label": "1.1 성명",
                        "label_en": "Inviter Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_gender",
                        "label": "1.2 성별",
                        "label_en": "Inviter Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_nationality",
                        "label": "1.3 국적(외국인인 경우 체류자격도 함께 기재)",
                        "label_en": "Inviter Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_birth_date",
                        "label": "1.4 생년월일 년 월 일",
                        "label_en": "Inviter Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_address",
                        "label": "1.5 주소",
                        "label_en": "Inviter Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_home_phone",
                        "label": "1.6 집 전화번호",
                        "label_en": "Inviter Home Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_mobile_phone",
                        "label": "1.7 휴대전화번호",
                        "label_en": "Inviter Mobile Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_email",
                        "label": "1.8 전자우편(e-mail) 주소",
                        "label_en": "Inviter Email",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_household_members",
                        "label": "2.1 초청인의 동거 가족(외국인 포함)과 관련된 정보",
                        "label_en": "Inviter Household Members",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "invitation_reason",
                        "label": "3.1아래 초청 사유 중 해당하는 곳에 √표를 하시기 ",
                        "label_en": "Invitation Reason",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "prior_invitation_history",
                        "label": "4.1 초청인은 과거 결혼이민자(초청인 본인 또는 배우",
                        "label_en": "Prior Invitation History",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "prior_invited_person_details",
                        "label": "4.2 위 “4.1” 항목에 “예”라고 답하였다면, 초",
                        "label_en": "Prior Invited Person Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_law_violation_record",
                        "label": "5.1 초청인은 과거 ｢출입국관리법｣ 제7조의2, 제1",
                        "label_en": "Inviter Law Violation Record",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "invited_foreigner_violation_record",
                        "label": "5.2 과거 초청인의 초청을 받고 입국한 외국인 중, ",
                        "label_en": "Invited Foreigner Violation Record",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "help_received",
                        "label": "9.1 이 신청서를 작성하는데 다른 사람의 도움을 받았",
                        "label_en": "Help Received",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_phone",
                        "label": "연락처",
                        "label_en": "Inviter Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_exists",
                        "label": "9.1 초청인/초청회사 Is there anyone i",
                        "label_en": "Inviter Exists",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_birth_or_business_no",
                        "label": "b) 생년월일/사업자등록번호 Date of Birth ",
                        "label_en": "Inviter Birth Or Business No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_relationship",
                        "label": "c) 관계 Relationship to the",
                        "label_en": "Inviter Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "application_date",
                        "label": "신청일자 (년. 월. 일) DATE OF APPLICA",
                        "label_en": "Application Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_applicant_name",
                        "label": "신청인(초청인) 성명 NAME OF APPLICANT(",
                        "label_en": "Inviter Applicant Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_signature",
                        "label": "신청인(초청인) 서명(인) SIGNATURE(SEAL)",
                        "label_en": "Inviter Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "self",
                "group_name": "피초청인 인적사항 및 가족관계",
                "group_name_en": "Invitee's Information and Family Relationship",
                "fields": [
                    {
                        "data_key": "relationship_to_inviter",
                        "label": "6.1 초청인과 피초청(사증발급 신청인)의 중 해당하는",
                        "label_en": "Relationship To Inviter",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_members_info",
                        "label": "6.2 피초청인과 그의 배우자, 부모, 자녀, 형제자매",
                        "label_en": "Family Members Info",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "previous_visit_korea",
                        "label": "6.3 피초청인은 과거 한국에 방문한 적이 있습니까(해",
                        "label_en": "Previous Visit Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "previous_violation_korea",
                        "label": "6.4 위 “6.3” 항목에 “예”라고 답하였다면, 피",
                        "label_en": "Previous Violation Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_used_other_names",
                        "label": "1.8 이전에 한국에 출입국하였을 때 다른 성명을 사용",
                        "label_en": "Has Used Other Names",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_multiple_nationalities",
                        "label": "1.9 복수 국적 여부 Is the the applia",
                        "label_en": "Has Multiple Nationalities",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "passport_type_other",
                        "label": "→ ‘기타’상세내용 If‘Other’, please p",
                        "label_en": "Passport Type Other",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "passport_place_of_issue",
                        "label": "2.4 발급지 Place of Issue",
                        "label_en": "Passport Place Of Issue",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_other_passport",
                        "label": "2.7 다른 여권 소지 여부 Does the the a",
                        "label_en": "Has Other Passport",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_type",
                        "label": "a) 여권종류 Passport Type",
                        "label_en": "Other Passport Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_no",
                        "label": "b) 여권번호 Passport No.",
                        "label_en": "Other Passport No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_country",
                        "label": "c) 발급국가 Country of Passport",
                        "label_en": "Other Passport Country",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_expiry",
                        "label": "d) 기간만료일 Date of Expiry",
                        "label_en": "Other Passport Expiry",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "home_country_address",
                        "label": "3.1 본국 주소 Home Country Address",
                        "label_en": "Home Country Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "phone_alt",
                        "label": "3.4 일반전화 Telephone No.",
                        "label_en": "Phone Alt",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "marital_status",
                        "label": "4.1 현재 혼인사항 Current Marital St",
                        "label_en": "Marital Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_children",
                        "label": "4.3 자녀 유무 Does the applicant h",
                        "label_en": "Has Children",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "children_count",
                        "label": "자녀수 Number of children",
                        "label_en": "Children Count",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_level",
                        "label": "5.1 최종학력 What is the highest d",
                        "label_en": "Education Level",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, ",
                        "label_en": "Education Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_name",
                        "label": "5.2 학교명 Name of School",
                        "label_en": "School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_location",
                        "label": "5.3 학교 소재지 Location of School(",
                        "label_en": "School Location",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation_status",
                        "label": "6.1 직업  Current personal circu",
                        "label_en": "Occupation Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, ",
                        "label_en": "Occupation Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "purpose_of_visit",
                        "label": "7.1 입국목적 Purpose of Visit to K",
                        "label_en": "Purpose Of Visit",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "purpose_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If ‘Other’ ",
                        "label_en": "Purpose Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_stay_period",
                        "label": "7.2 체류예정기간 Intended Period of ",
                        "label_en": "Intended Stay Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_entry_date",
                        "label": "7.3 입국예정일 Intended Date of Ent",
                        "label_en": "Intended Entry Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "address_in_korea",
                        "label": "7.4 체류예정지(호텔 포함) Address in Ko",
                        "label_en": "Address In Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_in_korea_phone",
                        "label": "7.5 한국 내 연락처 Contact No. in Ko",
                        "label_en": "Contact In Korea Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_korea_visits",
                        "label": "7.6 과거 5년간 한국을 방문한 경력",
                        "label_en": "Past Korea Visits",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_country",
                        "label": "국가명 Name of Country (in Englis",
                        "label_en": "Past Travel Country",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_purpose",
                        "label": "방문목적 Purpose of Visit",
                        "label_en": "Past Travel Purpose",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_period",
                        "label": "방문기간 Period of Stay  (yyyy/mm/",
                        "label_en": "Past Travel Period",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_emergency_contact",
                "group_name": "비상시 연락처",
                "group_name_en": "Emergency Contact",
                "fields": [
                    {
                        "data_key": "emergency_name",
                        "label": "a) 성명 Full Name in English",
                        "label_en": "Emergency Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_country_of_residence",
                        "label": "b) 거주국가 Country of Residence",
                        "label_en": "Emergency Country Of Residence",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_phone",
                        "label": "c) 전화번호 Telephone No.",
                        "label_en": "Emergency Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_relationship",
                        "label": "d) 관계 Relationship to the appl",
                        "label_en": "Emergency Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_spouse",
                "group_name": "배우자 인적사항",
                "group_name_en": "Spouse Information",
                "fields": [
                    {
                        "data_key": "spouse_surname",
                        "label": "a) 성 Family Name (in English)",
                        "label_en": "Spouse Surname",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_given_name",
                        "label": "b) 명 Given Names (in English)",
                        "label_en": "Spouse Given Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_birth_date",
                        "label": "c) 생년월일 Date of Birth (yyyy/mm",
                        "label_en": "Spouse Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_nationality",
                        "label": "d) 국적 Nationality",
                        "label_en": "Spouse Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_address",
                        "label": "e) 거주지 Residential Address",
                        "label_en": "Spouse Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_phone",
                        "label": "f) 연락처 Contact No.",
                        "label_en": "Spouse Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_employer",
                "group_name": "고용주/회사 정보",
                "group_name_en": "Employer/Company Details",
                "fields": [
                    {
                        "data_key": "employer_name",
                        "label": "a) 회사/기관/학교명 Name of Company/I",
                        "label_en": "Employer Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_position",
                        "label": "b) 직위/과정 Position/Course",
                        "label_en": "Employer Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_address",
                        "label": "c) 회사/기관/학교 주소 Address of Comp",
                        "label_en": "Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_phone",
                        "label": "d) 전화번호 Telephone No.",
                        "label_en": "Employer Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_family",
                "group_name": "국내 체류 가족",
                "group_name_en": "Family Staying in Korea",
                "fields": [
                    {
                        "data_key": "family_korea_name",
                        "label": "성명 Full name in English",
                        "label_en": "Family Korea Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Family Korea Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_nationality",
                        "label": "국적 Nationality",
                        "label_en": "Family Korea Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_relationship",
                        "label": "관계 Relationship to the applica",
                        "label_en": "Family Korea Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_name",
                        "label": "성명 Full name in English",
                        "label_en": "Companion Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Companion Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_nationality",
                        "label": "국적 Nationality",
                        "label_en": "Companion Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_relationship",
                        "label": "관계 Relationship to the invitee",
                        "label_en": "Companion Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_assistant",
                "group_name": "서류 작성 도움 여부",
                "group_name_en": "Assistance With This Form",
                "fields": [
                    {
                        "data_key": "assistant_name",
                        "label": "8.1 이 신청서를 작성하는데 다른 사람의 도움을 받았",
                        "label_en": "Assistant Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Assistant Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_phone",
                        "label": "연락처 Phone No.",
                        "label_en": "Assistant Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_relationship",
                        "label": "관계 Relationship to  the applic",
                        "label_en": "Assistant Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
    "E": {
        "scenario_name": "전문 인력",
        "scenario_name_en": "Professional Worker",
        "visa_type": "E-7",
        "field_groups": [
            {
                "target": "self",
                "group_name": "신청인 추가 정보",
                "group_name_en": "Applicant Additional Info",
                "fields": [
                    {
                        "data_key": "has_used_other_names",
                        "label": "1.8 이전에 한국에 출입국하였을 때 다른 성명을 사용",
                        "label_en": "Has Used Other Names",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_multiple_nationalities",
                        "label": "1.9 복수 국적 여부 Is the the applia",
                        "label_en": "Has Multiple Nationalities",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "passport_type_other",
                        "label": "→ ‘기타’상세내용 If‘Other’, please p",
                        "label_en": "Passport Type Other",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "passport_place_of_issue",
                        "label": "2.4 발급지 Place of Issue",
                        "label_en": "Passport Place Of Issue",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_other_passport",
                        "label": "2.7 다른 여권 소지 여부 Does the the a",
                        "label_en": "Has Other Passport",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_type",
                        "label": "a) 여권종류 Passport Type",
                        "label_en": "Other Passport Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_no",
                        "label": "b) 여권번호 Passport No.",
                        "label_en": "Other Passport No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_country",
                        "label": "c) 발급국가 Country of Passport",
                        "label_en": "Other Passport Country",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "other_passport_expiry",
                        "label": "d) 기간만료일 Date of Expiry",
                        "label_en": "Other Passport Expiry",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "home_country_address",
                        "label": "3.1 본국 주소 Home Country Address",
                        "label_en": "Home Country Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "phone_alt",
                        "label": "3.4 일반전화 Telephone No.",
                        "label_en": "Phone Alt",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "marital_status",
                        "label": "4.1 현재 혼인사항 Current Marital St",
                        "label_en": "Marital Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "has_children",
                        "label": "4.3 자녀 유무 Does the applicant h",
                        "label_en": "Has Children",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "children_count",
                        "label": "자녀수 Number of children",
                        "label_en": "Children Count",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_level",
                        "label": "5.1 최종학력 What is the highest d",
                        "label_en": "Education Level",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, ",
                        "label_en": "Education Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_name",
                        "label": "5.2 학교명 Name of School",
                        "label_en": "School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "school_location",
                        "label": "5.3 학교 소재지 Location of School(",
                        "label_en": "School Location",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation_status",
                        "label": "6.1 직업  Current personal circu",
                        "label_en": "Occupation Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If‘Other’, ",
                        "label_en": "Occupation Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "purpose_of_visit",
                        "label": "7.1 입국목적 Purpose of Visit to K",
                        "label_en": "Purpose Of Visit",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "purpose_other_details",
                        "label": "→ ‘기타’선택 시 상세내용 기재 If ‘Other’ ",
                        "label_en": "Purpose Other Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_stay_period",
                        "label": "7.2 체류예정기간 Intended Period of ",
                        "label_en": "Intended Stay Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_entry_date",
                        "label": "7.3 입국예정일 Intended Date of Ent",
                        "label_en": "Intended Entry Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "address_in_korea",
                        "label": "7.4 체류예정지(호텔 포함) Address in Ko",
                        "label_en": "Address In Korea",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_in_korea_phone",
                        "label": "7.5 한국 내 연락처 Contact No. in Ko",
                        "label_en": "Contact In Korea Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_korea_visits",
                        "label": "7.6 과거 5년간 한국을 방문한 경력",
                        "label_en": "Past Korea Visits",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_country",
                        "label": "국가명 Name of Country (in Englis",
                        "label_en": "Past Travel Country",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_purpose",
                        "label": "방문목적 Purpose of Visit",
                        "label_en": "Past Travel Purpose",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "past_travel_period",
                        "label": "방문기간 Period of Stay  (yyyy/mm/",
                        "label_en": "Past Travel Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_school_name",
                        "label": "학 교 명",
                        "label_en": "Education School Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_degree",
                        "label": "학 위",
                        "label_en": "Education Degree",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_major",
                        "label": "전 공",
                        "label_en": "Education Major",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "education_graduation_year",
                        "label": "졸업년도",
                        "label_en": "Education Graduation Year",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "experience_company",
                        "label": "업 체 명",
                        "label_en": "Experience Company",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "experience_period",
                        "label": "재직기간",
                        "label_en": "Experience Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "experience_field",
                        "label": "근무분야",
                        "label_en": "Experience Field",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "experience_position",
                        "label": "직 위",
                        "label_en": "Experience Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employment_period",
                        "label": "고용(예정)기간",
                        "label_en": "Employment Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "sojourn_status",
                        "label": "체류자격 (직종코드)",
                        "label_en": "Sojourn Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "job_field",
                        "label": "근무(예정)분야",
                        "label_en": "Job Field",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "job_title",
                        "label": "직 위",
                        "label_en": "Job Title",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "workplace",
                        "label": "근무(예정)지",
                        "label_en": "Workplace",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "salary_and_benefits",
                        "label": "급여 및 처우",
                        "label_en": "Salary And Benefits",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_emergency_contact",
                "group_name": "비상시 연락처",
                "group_name_en": "Emergency Contact",
                "fields": [
                    {
                        "data_key": "emergency_name",
                        "label": "a) 성명 Full Name in English",
                        "label_en": "Emergency Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_country_of_residence",
                        "label": "b) 거주국가 Country of Residence",
                        "label_en": "Emergency Country Of Residence",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_phone",
                        "label": "c) 전화번호 Telephone No.",
                        "label_en": "Emergency Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "emergency_relationship",
                        "label": "d) 관계 Relationship to the appl",
                        "label_en": "Emergency Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_spouse",
                "group_name": "배우자 인적사항",
                "group_name_en": "Spouse Information",
                "fields": [
                    {
                        "data_key": "spouse_surname",
                        "label": "a) 성 Family Name (in English)",
                        "label_en": "Spouse Surname",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_given_name",
                        "label": "b) 명 Given Names (in English)",
                        "label_en": "Spouse Given Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_birth_date",
                        "label": "c) 생년월일 Date of Birth (yyyy/mm",
                        "label_en": "Spouse Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_nationality",
                        "label": "d) 국적 Nationality",
                        "label_en": "Spouse Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_address",
                        "label": "e) 거주지 Residential Address",
                        "label_en": "Spouse Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "spouse_phone",
                        "label": "f) 연락처 Contact No.",
                        "label_en": "Spouse Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_employer",
                "group_name": "고용주/회사 정보",
                "group_name_en": "Employer/Company Details",
                "fields": [
                    {
                        "data_key": "employer_name",
                        "label": "a) 회사/기관/학교명 Name of Company/I",
                        "label_en": "Employer Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_position",
                        "label": "b) 직위/과정 Position/Course",
                        "label_en": "Employer Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_address",
                        "label": "c) 회사/기관/학교 주소 Address of Comp",
                        "label_en": "Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_phone",
                        "label": "d) 전화번호 Telephone No.",
                        "label_en": "Employer Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_company_name",
                        "label": "회사명",
                        "label_en": "Employer Company Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_business_registration_no",
                        "label": "사업자등록번호 (법인등록번호)",
                        "label_en": "Employer Business Registration No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_representative_name",
                        "label": "대표자명",
                        "label_en": "Employer Representative Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_capital_amount",
                        "label": "자본금",
                        "label_en": "Employer Capital Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_total_sales",
                        "label": "총매출액",
                        "label_en": "Employer Total Sales",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_total_liabilities",
                        "label": "부채총액",
                        "label_en": "Employer Total Liabilities",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_operating_profit",
                        "label": "영업이익",
                        "label_en": "Employer Operating Profit",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_num_employees",
                        "label": "상시종업원수",
                        "label_en": "Employer Num Employees",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "employer_num_foreign_professionals",
                        "label": "외국전문인력수",
                        "label_en": "Employer Num Foreign Professionals",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_family",
                "group_name": "국내 체류 가족",
                "group_name_en": "Family Staying in Korea",
                "fields": [
                    {
                        "data_key": "family_korea_name",
                        "label": "성명 Full name in English",
                        "label_en": "Family Korea Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Family Korea Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_nationality",
                        "label": "국적 Nationality",
                        "label_en": "Family Korea Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_korea_relationship",
                        "label": "관계 Relationship to the applica",
                        "label_en": "Family Korea Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_name",
                        "label": "성명 Full name in English",
                        "label_en": "Companion Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Companion Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_nationality",
                        "label": "국적 Nationality",
                        "label_en": "Companion Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "companion_relationship",
                        "label": "관계 Relationship to the invitee",
                        "label_en": "Companion Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_assistant",
                "group_name": "서류 작성 도움 여부",
                "group_name_en": "Assistance With This Form",
                "fields": [
                    {
                        "data_key": "assistant_name",
                        "label": "8.1 이 신청서를 작성하는데 다른 사람의 도움을 받았",
                        "label_en": "Assistant Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_birth_date",
                        "label": "생년월일 Date of Birth  (yyyy/mm/d",
                        "label_en": "Assistant Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_phone",
                        "label": "연락처 Phone No.",
                        "label_en": "Assistant Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "assistant_relationship",
                        "label": "관계 Relationship to  the applic",
                        "label_en": "Assistant Relationship",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_inviter",
                "group_name": "초청 정보",
                "group_name_en": "Details of Invitation",
                "fields": [
                    {
                        "data_key": "inviter_exists",
                        "label": "9.1 초청인/초청회사 Is there anyone i",
                        "label_en": "Inviter Exists",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_name",
                        "label": "a) 초청인/초청회사명 Name of inviting ",
                        "label_en": "Inviter Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_birth_or_business_no",
                        "label": "b) 생년월일/사업자등록번호 Date of Birth ",
                        "label_en": "Inviter Birth Or Business No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_relationship",
                        "label": "c) 관계 Relationship to the",
                        "label_en": "Inviter Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_address",
                        "label": "d) 주소 Address",
                        "label_en": "Inviter Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_phone",
                        "label": "e) 전화번호 Phone No.",
                        "label_en": "Inviter Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "application_date",
                        "label": "신청일자 (년. 월. 일) DATE OF APPLICA",
                        "label_en": "Application Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_applicant_name",
                        "label": "신청인(초청인) 성명 NAME OF APPLICANT(",
                        "label_en": "Inviter Applicant Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "inviter_signature",
                        "label": "신청인(초청인) 서명(인) SIGNATURE(SEAL)",
                        "label_en": "Inviter Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
    "F": {
        "scenario_name": "국적 귀화",
        "scenario_name_en": "Naturalization",
        "visa_type": "귀화",
        "field_groups": [
            {
                "target": "self",
                "group_name": "신청인 인적사항",
                "group_name_en": "Applicant Personal Information",
                "fields": [
                    {
                        "data_key": "birth_place",
                        "label": "출생지(국가 및 도시명)",
                        "label_en": "Birth Place",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "full_name_en",
                        "label": "성명(영문)",
                        "label_en": "Full Name En",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "phone_home",
                        "label": "(자택)",
                        "label_en": "Phone Home",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "intended_registered_domicile",
                        "label": "예정 등록기준지",
                        "label_en": "Intended Registered Domicile",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "occupation",
                        "label": "직업",
                        "label_en": "Occupation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "monthly_income",
                        "label": "월 평균 소득액(최근 6개월간)",
                        "label_en": "Monthly Income",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "last_year_income",
                        "label": "전년도 소득액(세무서장 발행 소득금액증명원상 소득)",
                        "label_en": "Last Year Income",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "real_estate_assets_amount",
                        "label": "부동산(보증금 등) 만원",
                        "label_en": "Real Estate Assets Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "financial_assets_amount",
                        "label": "금융재산 만원",
                        "label_en": "Financial Assets Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "offense_date",
                        "label": "일자",
                        "label_en": "Offense Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "offense_details",
                        "label": "위반내용(죄명)",
                        "label_en": "Offense Details",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "disposition_result",
                        "label": "처분결과",
                        "label_en": "Disposition Result",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "tax_arrears_amount",
                        "label": "국세",
                        "label_en": "Tax Arrears Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "health_insurance_arrears_amount",
                        "label": "건강보험료",
                        "label_en": "Health Insurance Arrears Amount",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "oath_participation",
                        "label": "국민선서의 내용을 확인하였으며, 국적증서수여식에 참석하",
                        "label_en": "Oath Participation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "law_compliance_agree",
                        "label": "대한민국 국적 취득 후 대한민국의 헌법과 법률을 준수하",
                        "label_en": "Law Compliance Agree",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "four_duties_ack",
                        "label": "국민의 4대 의무",
                        "label_en": "Four Duties Ack",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "disability_type",
                        "label": "장애 종류",
                        "label_en": "Disability Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "disability_grade",
                        "label": "장애 구분",
                        "label_en": "Disability Grade",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "disease_type",
                        "label": "질병 종류",
                        "label_en": "Disease Type",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "disease_status",
                        "label": "질병 구분",
                        "label_en": "Disease Status",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "award_name",
                        "label": "수상명",
                        "label_en": "Award Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "award_issuer",
                        "label": "수여자",
                        "label_en": "Award Issuer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "license_name",
                        "label": "자격(면허)명",
                        "label_en": "License Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "license_grade",
                        "label": "등급",
                        "label_en": "License Grade",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "volunteer_activity",
                        "label": "봉사활동",
                        "label_en": "Volunteer Activity",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "community_activity",
                        "label": "지역사회활동",
                        "label_en": "Community Activity",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "organization_name",
                        "label": "단체명",
                        "label_en": "Organization Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "activity_period",
                        "label": "활동기간",
                        "label_en": "Activity Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "commendation_for_good_deed",
                        "label": "선행으로 인한 훈장ㆍ표창 수여",
                        "label_en": "Commendation For Good Deed",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "blood_donation_times",
                        "label": "횟수",
                        "label_en": "Blood Donation Times",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "signature_name",
                        "label": "신청인 Applicant’s Name",
                        "label_en": "Signature Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "stay_purpose",
                        "label": "체류목적",
                        "label_en": "Stay Purpose",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_family",
                "group_name": "가족사항",
                "group_name_en": "Family Members",
                "fields": [
                    {
                        "data_key": "family_name",
                        "label": "성명",
                        "label_en": "Family Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_birth_date",
                        "label": "생년월일",
                        "label_en": "Family Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_gender",
                        "label": "성별",
                        "label_en": "Family Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_nationality",
                        "label": "국적 (거주지)",
                        "label_en": "Family Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_phone",
                        "label": "연락처",
                        "label_en": "Family Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_former_korean_national",
                        "label": "과거 한국국적 보유자",
                        "label_en": "Family Former Korean National",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "family_dependent_application",
                        "label": "수반취득 신청자",
                        "label_en": "Family Dependent Application",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_nationality",
                        "label": "현재 국적",
                        "label_en": "Child Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_birth_place",
                        "label": "출생지(국가 및 도시명)",
                        "label_en": "Child Birth Place",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_name_kr",
                        "label": "성명(한글)",
                        "label_en": "Child Name Kr",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_gender",
                        "label": "성별",
                        "label_en": "Child Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_name_en",
                        "label": "성명(영문)",
                        "label_en": "Child Name En",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_alien_registration_no",
                        "label": "외국인등록번호",
                        "label_en": "Child Alien Registration No",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "child_intended_registered_domicile",
                        "label": "예정 등록기준지",
                        "label_en": "Child Intended Registered Domicile",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_spouse",
                "group_name": "배우자",
                "group_name_en": "Spouse",
                "fields": [
                    {
                        "data_key": "spouse_name",
                        "label": "배우자",
                        "label_en": "Spouse Name",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_contact",
                "group_name": "국내 연고자 또는 동거인",
                "group_name_en": "Domestic Relative or Cohabitant",
                "fields": [
                    {
                        "data_key": "contact_relation",
                        "label": "관계",
                        "label_en": "Contact Relation",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_name",
                        "label": "성명",
                        "label_en": "Contact Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_birth_date",
                        "label": "생년월일",
                        "label_en": "Contact Birth Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_nationality",
                        "label": "국적 (거주지)",
                        "label_en": "Contact Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "contact_phone",
                        "label": "연락처",
                        "label_en": "Contact Phone",
                        "type": "text",
                        "required": True
                    },
                ]
            },
            {
                "target": "other_guarantor",
                "group_name": "신원보증인",
                "group_name_en": "Guarantor",
                "fields": [
                    {
                        "data_key": "guarantor_name",
                        "label": "성명",
                        "label_en": "Guarantor Name",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_name_hanja",
                        "label": "漢字",
                        "label_en": "Guarantor Name Hanja",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_nationality",
                        "label": "국적",
                        "label_en": "Guarantor Nationality",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_gender",
                        "label": "성별",
                        "label_en": "Guarantor Gender",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_passport_or_birth",
                        "label": "여권번호 또는 생년월일",
                        "label_en": "Guarantor Passport Or Birth",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_phone",
                        "label": "전화번호",
                        "label_en": "Guarantor Phone",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_address",
                        "label": "주소",
                        "label_en": "Guarantor Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_relationship",
                        "label": "피보증인과의 관계",
                        "label_en": "Guarantor Relationship",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer",
                        "label": "근무처",
                        "label_en": "Guarantor Employer",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_position",
                        "label": "직위",
                        "label_en": "Guarantor Position",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_employer_address",
                        "label": "근무처 주소",
                        "label_en": "Guarantor Employer Address",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_note",
                        "label": "비고",
                        "label_en": "Guarantor Note",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_guarantee_period",
                        "label": "나. 보증기간(보증기간의 최장기간은 4년으로 한다)",
                        "label_en": "Guarantor Guarantee Period",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature_date",
                        "label": "년              월           일장",
                        "label_en": "Guarantor Signature Date",
                        "type": "text",
                        "required": True
                    },
                    {
                        "data_key": "guarantor_signature",
                        "label": "(서명 또는 인)",
                        "label_en": "Guarantor Signature",
                        "type": "text",
                        "required": True
                    },
                ]
            },
        ]
    },
}

# ======================================================================
# 📊 LAYER 3: Narrative Fields (서술형, AI 검토)
# ======================================================================

LAYER3_NARRATIVE_FIELDS = {
    "A": {
        "scenario_name": "구직 준비",
        "scenario_name_en": "Job Seeking",
        "visa_type": "D-10",
        "narrative_label": "월별 구직 활동 계획",
        "narrative_label_en": "Monthly Job Search Plan",
        "fields": [
            {
                "data_key": "job_search_plan_month1",
                "label": "1개월차 계획",
                "label_en": "1st Month Plan",
                "hint": "1번째 달의 구직 활동 계획을 상세히 작성해주세요.",
                "hint_en": "1번째 달의 구직 활동 계획을 상세히 작성해주세요.",
                "placeholder": "예: 이력서 작성, 기업 분석 및 지원 리스트업",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第一月 / 1st month"
            },
            {
                "data_key": "job_search_plan_month2",
                "label": "2개월차 계획",
                "label_en": "第二月 / 2nd month",
                "hint": "2번째 달의 활동 계획을 작성해주세요.",
                "hint_en": "2번째 달의 활동 계획을 작성해주세요.",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第二月 / 2nd month"
            },
            {
                "data_key": "job_search_plan_month3",
                "label": "3개월차 계획",
                "label_en": "第三月 / 3rd month",
                "hint": "3번째 달의 활동 계획을 작성해주세요.",
                "hint_en": "3번째 달의 활동 계획을 작성해주세요.",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第三月 / 3rd month"
            },
            {
                "data_key": "job_search_plan_month4",
                "label": "4개월차 계획",
                "label_en": "第四月 / 4th month",
                "hint": "4번째 달의 활동 계획을 작성해주세요.",
                "hint_en": "4번째 달의 활동 계획을 작성해주세요.",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第四月 / 4th month"
            },
            {
                "data_key": "job_search_plan_month5",
                "label": "5개월차 계획",
                "label_en": "第五月 / 5th month",
                "hint": "5번째 달의 활동 계획을 작성해주세요.",
                "hint_en": "5번째 달의 활동 계획을 작성해주세요.",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第五月 / 5th month"
            },
            {
                "data_key": "job_search_plan_month6",
                "label": "6개월차 계획",
                "label_en": "第六月 /6th month",
                "hint": "6번째 달의 활동 계획을 작성해주세요.",
                "hint_en": "6번째 달의 활동 계획을 작성해주세요.",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "第六月 /6th month"
            },
        ],
        "validation_prompt": """구체적인 월별 계획과 실현 가능성을 중점적으로 검토하세요.""",
        "danger_patterns": ['취업 확정', '내정', '채용 확정']
    },
    "C": {
        "scenario_name": "결혼 이민",
        "scenario_name_en": "Marriage Immigration",
        "visa_type": "F-6",
        "narrative_label": "결혼 배경 진술",
        "narrative_label_en": "Marriage Background",
        "fields": [
            {
                "data_key": "other_names_explanation",
                "label": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                "label_en": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                "hint": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                "hint_en": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "1.4 과거에 다른 이름을 사용하였던 적이 있습니까?"
            },
            {
                "data_key": "children_from_previous_marriage_details",
                "label": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                "label_en": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                "hint": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                "hint_en": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "2.4 신청인은 과거 혼인관계에서 출생한 자녀가 있습니까?"
            },
            {
                "data_key": "immigration_issues_details",
                "label": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                "label_en": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                "hint": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                "hint_en": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3.2 과거 한국 정부로부터 입국거부, 입국금지되거나 강제퇴거 또는 출국명령을 받은 적이"
            },
            {
                "data_key": "assistance_details",
                "label": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                "label_en": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                "hint": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                "hint_en": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "4.1 이 초청장을 작성하는데 다른 사람의 도움을 받았습니까?"
            },
        ],
        "validation_prompt": """내용의 사실 관계와 논리적 흐름을 검토하세요.""",
        "danger_patterns": ['허위', '거짓', '불법']
    },
    "D": {
        "scenario_name": "가족 초청",
        "scenario_name_en": "Family Invitation",
        "visa_type": "F-1-5",
        "narrative_label": "초청 사유",
        "narrative_label_en": "Narrative Input",
        "fields": [
            {
                "data_key": "inviter_activity_status",
                "label": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부",
                "label_en": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부",
                "hint": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부",
                "hint_en": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3.2.1. 초청인과 배우자가 직장생활 등 외부활동을 하고 있는지 기재하시기 바랍니다(외부"
            },
            {
                "data_key": "current_caregiving_status",
                "label": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는",
                "label_en": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는",
                "hint": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는",
                "hint_en": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3.2.2. 현재 누가 어떤 방식으로 자녀를 양육(중증질환 등이 있는 가족 간병)하고 있는"
            },
            {
                "data_key": "invitee_expected_role",
                "label": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니",
                "label_en": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니",
                "hint": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니",
                "hint_en": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3.2.3. 피초청인이 입국하면 가정 내에서 어떤 역할을 맡게 될 것인지 기재하시기 바랍니"
            },
            {
                "data_key": "invitee_support_plan",
                "label": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해",
                "label_en": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해",
                "hint": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해",
                "hint_en": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3.3 위 초청 목적(사유)와 관련하여 피초청인(사증발급 신청인)이 입국하여 국내에 체류해"
            },
            {
                "data_key": "additional_info",
                "label": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시",
                "label_en": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시",
                "hint": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시",
                "hint_en": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "‣ 이번 초청 건과 관련하여 사증발급 심사에 고려할 그 밖의 정보가 있다면 아래에 기재하시"
            },
        ],
        "validation_prompt": """내용의 사실 관계와 논리적 흐름을 검토하세요.""",
        "danger_patterns": ['허위', '거짓', '불법']
    },
    "E": {
        "scenario_name": "전문 인력",
        "scenario_name_en": "Professional Worker",
        "visa_type": "E-7",
        "narrative_label": "서술형 작성",
        "narrative_label_en": "Narrative Input",
        "fields": [
            {
                "data_key": "employer_company_intro",
                "label": "회사 및 사업(업무) 소개",
                "label_en": "회사 및 사업(업무) 소개",
                "hint": "회사 및 사업(업무) 소개",
                "hint_en": "회사 및 사업(업무) 소개",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "회사 및 사업(업무) 소개"
            },
            {
                "data_key": "employer_employment_reason",
                "label": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 ",
                "label_en": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 ",
                "hint": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 ",
                "hint_en": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 ",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "1) 고용사유 (※ 외국인력 도입 업무와 관련한 전문인력부족 현황, 국내인력 채용노력 및 "
            },
            {
                "data_key": "employer_tech_import_effect",
                "label": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성",
                "label_en": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성",
                "hint": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성",
                "hint_en": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "2) 기술도입 및 전문외국인력고용 효과  (※ 도입기술 분야, 기술 내용, 희소성, 전문성"
            },
            {
                "data_key": "employer_utilization_plan",
                "label": "3) 활용계획",
                "label_en": "3) 활용계획",
                "hint": "3) 활용계획",
                "hint_en": "3) 활용계획",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "3) 활용계획"
            },
            {
                "data_key": "employer_other_notes",
                "label": "4) 기타사항",
                "label_en": "4) 기타사항",
                "hint": "4) 기타사항",
                "hint_en": "4) 기타사항",
                "placeholder": "",
                "placeholder_en": "",
                "min_chars": 50,
                "required": True,
                "anchor_text": "4) 기타사항"
            },
        ],
        "validation_prompt": """내용의 사실 관계와 논리적 흐름을 검토하세요.""",
        "danger_patterns": ['허위', '거짓', '불법']
    },
}


# ======================================================================
# 📊 시나리오 정의
# ======================================================================

@dataclass
class Scenario:
    """시나리오 정의 클래스"""
    id: str
    name: str
    name_en: str
    visa_type: str
    icon: str
    description: str
    description_en: str
    track: str
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
        description_en="Visa extension and status change for job seeking activities",
        track="high_volume",
        required_docs=['통합신청서', '구직활동계획서', '신원보증서'],
        price=9.99
    ),
    "B": Scenario(
        id="B",
        name="아르바이트",
        name_en="Part-time Work",
        visa_type="시간제 취업",
        icon="⏰",
        description="유학생/연수생 시간제 취업 허가 신청",
        description_en="Part-time work permit application for students",
        track="high_volume",
        required_docs=['통합신청서', '시간제취업확인서', '신원보증서'],
        price=9.99
    ),
    "C": Scenario(
        id="C",
        name="결혼 이민",
        name_en="Marriage Immigration",
        visa_type="F-6",
        icon="💍",
        description="한국인 배우자와의 결혼을 통한 비자 신청",
        description_en="Visa application through marriage with Korean spouse",
        track="high_margin",
        required_docs=['통합신청서', '결혼배경진술서', '외국인배우자초청장', '신원보증서'],
        price=19.99
    ),
    "D": Scenario(
        id="D",
        name="가족 초청",
        name_en="Family Invitation",
        visa_type="F-1-5",
        icon="👨‍👩‍👧",
        description="부모님 또는 가족을 한국으로 초청",
        description_en="Inviting parents or family members to Korea",
        track="high_margin",
        required_docs=['가족초청장', '불법체류취업방지서약서', '신원보증서', '사증발급인정신청서'],
        price=19.99
    ),
    "E": Scenario(
        id="E",
        name="전문 인력",
        name_en="Professional Worker",
        visa_type="E-7",
        icon="🎓",
        description="특정 분야 전문 인력 채용을 위한 비자 신청",
        description_en="Visa application for hiring professional workers",
        track="recurring",
        required_docs=['사증발급인정신청서', '고용사유서', '신원보증서'],
        price=29.99
    ),
    "F": Scenario(
        id="F",
        name="국적 귀화",
        name_en="Naturalization",
        visa_type="귀화",
        icon="🏛️",
        description="대한민국 국적 취득을 위한 귀화 신청",
        description_en="Naturalization application for Korean citizenship",
        track="recurring",
        required_docs=['귀화허가신청서', '신원보증서'],
        price=49.99
    ),
}

# ======================================================================
# 유틸리티 함수
# ======================================================================

def get_layer1_fields() -> List[Dict]:
    """Layer 1 (본인 정보) 필드 목록 반환"""
    return LAYER1_UNIVERSAL_FIELDS


def get_layer2_field_groups(scenario_id: str) -> List[Dict]:
    """시나리오별 Layer 2 필드 그룹 반환 (타인 정보 등)"""
    return LAYER2_VARIABLE_FIELDS.get(scenario_id, {}).get("field_groups", [])


def get_layer2_fields(scenario_id: str) -> List[Dict]:
    """
    Layer 2 필드를 flat하게 반환 (하위 호환 + section 정보 포함)
    scenario_form.py에서 사용
    """
    field_groups = get_layer2_field_groups(scenario_id)
    all_fields = []
    
    for group in field_groups:
        target = group.get("target", "self")
        group_name = group.get("group_name", "기타")
        group_name_en = group.get("group_name_en", "Other")
        
        for field in group.get("fields", []):
            # 원본 필드 복사 후 section 정보 추가
            field_with_section = field.copy()
            field_with_section["section"] = group_name
            field_with_section["section_en"] = group_name_en
            field_with_section["target"] = target
            all_fields.append(field_with_section)
    
    return all_fields

# ======================================================================
# 📄 문서 템플릿 매핑 (실제 파일명)
# ======================================================================

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
    "외국인배우자초청장": "외국인 배우자 초청장.docx",  # 주의: SCENARIOS의 required_docs 키와 일치해야 함
    
    # 시나리오 D: 가족 초청 (F-1-5)
    "가족초청장": "결혼이민자의 부모 등 가족 초청장(F-1-5 비자 신청용).docx",
    "불법체류취업방지서약서": "불법체류 취업 방지 서약서(F-1-5).docx",
    
    # 시나리오 E: 전문 인력 (E-7)
    "고용사유서": "고용사유서.docx",
    "고용활용계획서": "고용사유서.docx", # E-7 필수 문서 매핑 추가
    
    # 시나리오 F: 국적 귀화
    "귀화허가신청서": "귀화허가신청서.docx",
    "귀화추천서": "귀화추천서.docx",
    "가족관계통보서": "가족관계통보서.docx",
    
    # 기타
    "거주숙소제공사실확인서": "거주숙소제공사실확인서(영문병기).docx",
}

def get_layer3_config(scenario_id: str) -> Dict:
    """시나리오별 Layer 3 설정 반환 (서술형 필드)"""
    return LAYER3_NARRATIVE_FIELDS.get(scenario_id, {})


def get_layer3_fields(scenario_id: str) -> List[Dict]:
    """시나리오별 Layer 3 필드 목록 반환"""
    return LAYER3_NARRATIVE_FIELDS.get(scenario_id, {}).get("fields", [])


def get_narrative_config(scenario_id: str) -> Dict:
    """시나리오별 서술형 설정 전체 반환 (get_layer3_config 별칭)"""
    return get_layer3_config(scenario_id)


def get_danger_patterns(scenario_id: str) -> List[str]:
    """시나리오별 위험 패턴 반환"""
    return LAYER3_NARRATIVE_FIELDS.get(scenario_id, {}).get("danger_patterns", [])


def is_layer1_field(key: str) -> bool:
    """해당 키가 Layer 1 필드인지 확인"""
    return key in LAYER1_KEYS


def get_scenario(scenario_id: str) -> Optional[Scenario]:
    """시나리오 정보 반환"""
    return SCENARIOS.get(scenario_id)


def get_all_scenarios() -> Dict[str, Scenario]:
    """모든 시나리오 반환"""
    return SCENARIOS


def get_target_info(target: str) -> Dict:
    """Target 정보 반환 (prefix, group_name 등)"""
    return TARGET_INFO.get(target, TARGET_INFO.get("self", {}))
    # ======================================================================
# 🔧 앱 초기화 함수 (이 부분을 파일 맨 끝에 추가하세요)
# ======================================================================

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