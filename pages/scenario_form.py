"""
K-Stay Scenario Form Page - Redesigned
서류 기반 Step-by-Step UI with Progress Tracking

핵심 개선사항:
1. 서류 단위로 스텝 분리 (탭 네비게이션)
2. 전체/현재 서류 진행률 시각화
3. 중복 필드 자동 동기화
4. 카드 기반 깔끔한 섹션 UI
5. 서류별 설명 및 맥락 제공
"""

import streamlit as st
from datetime import date, datetime
from typing import Dict, List, Any, Optional, Tuple

# 설정 파일에서 Layer 정의 임포트
from config.settings import (
    SCENARIOS,
    LAYER1_UNIVERSAL_FIELDS,
    LAYER2_VARIABLE_FIELDS,
    LAYER3_NARRATIVE_FIELDS,
    TARGET_INFO,
    DOCUMENT_TEMPLATES,
    get_layer2_fields,
    get_layer2_field_groups,
    get_layer3_fields,
    get_danger_patterns,
    get_narrative_config,
)
from services.payment_service import PaymentService


# =============================================================================
# 서류-필드 매핑 정의 (시나리오별)
# =============================================================================

DOCUMENT_FIELD_MAPPING = {
    "A": {  # 구직 준비 (D-10)
        "통합신청서": {
            "icon": "📋",
            "description": "체류자격 변경/연장 기본 신청서",
            "description_en": "Basic application form for status change/extension",
            "sections": [
                {
                    "name": "신청인 기본정보",
                    "name_en": "Applicant Basic Info",
                    "icon": "👤",
                    "fields": ["address_korea", "home_country_address", "occupation", "annual_income_amount"]
                },
                {
                    "name": "체류 정보",
                    "name_en": "Stay Information", 
                    "icon": "🏠",
                    "fields": ["stay_purpose", "intended_reentry_period", "refund_bank_account_no"]
                },
                {
                    "name": "서명/날인",
                    "name_en": "Signature",
                    "icon": "✍️",
                    "fields": ["application_date", "applicant_signature", "consent_applicant_signature", "consent_spouse_signature", "consent_parent_signature"]
                }
            ]
        },
        "구직활동계획서": {
            "icon": "💼",
            "description": "구직 활동 계획 및 준비 현황",
            "description_en": "Job search activity plan and preparation status",
            "sections": [
                {
                    "name": "학력/경력 정보",
                    "name_en": "Education & Experience",
                    "icon": "🎓",
                    "fields": ["university_name", "major_degree", "work_experience"]
                },
                {
                    "name": "구직 희망 정보",
                    "name_en": "Job Preferences",
                    "icon": "🎯",
                    "fields": ["occupational_category", "company_name", "expected_salary"]
                },
                {
                    "name": "생활비 조달 계획",
                    "name_en": "Living Cost Plan",
                    "icon": "💰",
                    "fields": ["living_cost_cash", "living_cost_deposit", "living_cost_credit_card", "living_cost_remittance"]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 인적사항",
                    "name_en": "Guarantor Personal Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth"]
                },
                {
                    "name": "보증인 연락처",
                    "name_en": "Guarantor Contact",
                    "icon": "📞",
                    "fields": ["guarantor_phone", "guarantor_address"]
                },
                {
                    "name": "보증인 직장정보",
                    "name_en": "Guarantor Employment",
                    "icon": "🏢",
                    "fields": ["guarantor_employer", "guarantor_position", "guarantor_employer_address"]
                },
                {
                    "name": "보증 내용",
                    "name_en": "Guarantee Details",
                    "icon": "📝",
                    "fields": ["guarantor_relationship", "guarantor_guarantee_period", "guarantor_note", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    },
    "B": {  # 아르바이트 (시간제 취업)
        "통합신청서": {
            "icon": "📋",
            "description": "시간제 취업허가 기본 신청서",
            "description_en": "Basic application for part-time work permit",
            "sections": [
                {
                    "name": "신청인 기본정보",
                    "name_en": "Applicant Basic Info",
                    "icon": "👤",
                    "fields": ["address_korea", "home_country_address", "phone", "occupation"]
                },
                {
                    "name": "학교 정보",
                    "name_en": "School Information",
                    "icon": "🎓",
                    "fields": ["school_status", "school_name", "school_type", "department_major", "semester"]
                },
                {
                    "name": "서명/날인",
                    "name_en": "Signature",
                    "icon": "✍️",
                    "fields": ["application_date", "applicant_signature"]
                }
            ]
        },
        "시간제취업확인서": {
            "icon": "⏰",
            "description": "취업 예정 근무처 정보",
            "description_en": "Expected workplace information",
            "sections": [
                {
                    "name": "근무처 기본정보",
                    "name_en": "Workplace Basic Info",
                    "icon": "🏪",
                    "fields": ["employer_company_name", "employer_business_registration_no", "employer_industry"]
                },
                {
                    "name": "근무처 연락처",
                    "name_en": "Workplace Contact",
                    "icon": "📍",
                    "fields": ["employer_address", "employer_phone"]
                },
                {
                    "name": "근무 조건",
                    "name_en": "Work Conditions",
                    "icon": "📅",
                    "fields": ["employment_period",                     "employer_wage_hourly",           # wage_hourly → employer_wage_hourly
                    "employer_weekday_total_hours",   # 수정!
                    "employer_weekend_total_hours"    # 수정!
                    ]
                },
                {
                    "name": "요일별 근무시간",
                    "name_en": "Daily Work Hours",
                    "icon": "🕐",
                    "fields": [
                        "employer_working_hours_mon",     # 수정!
                        "employer_working_hours_tue",     # 수정!
                        "employer_working_hours_wed",     # 수정!
                        "employer_working_hours_thu",     # 수정!
                        "employer_working_hours_fri",     # 수정!
                        "employer_working_hours_sat",     # 수정!
                        "employer_working_hours_sun"      # 수정!
                    ]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 인적사항",
                    "name_en": "Guarantor Personal Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth"]
                },
                {
                    "name": "보증인 연락처/직장",
                    "name_en": "Guarantor Contact & Work",
                    "icon": "📞",
                    "fields": ["guarantor_phone", "guarantor_address", "guarantor_employer", "guarantor_position", "guarantor_employer_address"]
                },
                {
                    "name": "보증 내용",
                    "name_en": "Guarantee Details",
                    "icon": "📝",
                    "fields": ["guarantor_relationship", "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    },
    "C": {  # 결혼 이민 (F-6)
        "통합신청서": {
            "icon": "📋",
            "description": "결혼이민 비자 기본 신청서",
            "description_en": "Basic application for marriage immigration visa",
            "sections": [
                {
                    "name": "신청인 기본정보",
                    "name_en": "Applicant Basic Info",
                    "icon": "👤",
                    "fields": ["address_korea", "home_country_address", "surname_native", "given_name_native"]
                },
                {
                    "name": "과거 이름 사용",
                    "name_en": "Previous Names",
                    "icon": "📝",
                    "fields": ["used_other_names"]
                },
                {
                    "name": "서명/날인",
                    "name_en": "Signature",
                    "icon": "✍️",
                    "fields": ["application_date", "applicant_signature", "consent_applicant_signature", "consent_spouse_signature", "consent_parent_signature"]
                }
            ]
        },
        "결혼배경진술서": {
            "icon": "💍",
            "description": "결혼 경위 및 배경 진술",
            "description_en": "Marriage background statement",
            "sections": [
                {
                    "name": "혼인 관련 사항",
                    "name_en": "Marriage Related",
                    "icon": "💒",
                    "fields": ["family_knows_marriage", "ever_been_married", "has_other_spouse_currently", "has_children_from_previous_marriage"]
                },
                {
                    "name": "출입국 이력",
                    "name_en": "Immigration History",
                    "icon": "✈️",
                    "fields": ["visited_korea_before", "immigration_issues_history"]
                },
                {
                    "name": "작성 도움 여부",
                    "name_en": "Assistance",
                    "icon": "🤝",
                    "fields": ["received_assistance"]
                }
            ]
        },
        "외국인배우자초청장": {
            "icon": "📨",
            "description": "배우자 초청 관련 정보",
            "description_en": "Spouse invitation details",
            "sections": [
                {
                    "name": "초청인 연락처",
                    "name_en": "Inviter Contact",
                    "icon": "📞",
                    "fields": ["inviter_home_phone", "inviter_phone", "inviter_email"]
                },
                {
                    "name": "세대 구성",
                    "name_en": "Household",
                    "icon": "👨‍👩‍👧",
                    "fields": ["household_lineal_count", "household_total_count"]
                },
                {
                    "name": "소득/재산 정보",
                    "name_en": "Income & Assets",
                    "icon": "💰",
                    "fields": ["earned_income_total", "business_income_total", "other_income_type", "other_income_amount", "other_income_total", "asset_type_1", "asset_amount_1", "asset_total_amount", "asset_converted_total", "income_assets_grand_total"]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 인적사항",
                    "name_en": "Guarantor Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth", "guarantor_phone", "guarantor_address"]
                },
                {
                    "name": "보증 내용",
                    "name_en": "Guarantee Details",
                    "icon": "📝",
                    "fields": ["guarantor_relationship", "guarantor_employer", "guarantor_position", "guarantor_employer_address", "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    },
    "D": {  # 가족 초청 (F-1-5)
        "가족초청장": {
            "icon": "👨‍👩‍👧",
            "description": "가족 초청 사유 및 정보",
            "description_en": "Family invitation reason and details",
            "sections": [
                {
                    "name": "초청인 인적사항",
                    "name_en": "Inviter Personal Info",
                    "icon": "👤",
                    "fields": ["inviter_name", "inviter_gender", "inviter_nationality", "inviter_birth_date", "inviter_address"]
                },
                {
                    "name": "초청인 연락처",
                    "name_en": "Inviter Contact",
                    "icon": "📞",
                    "fields": ["inviter_home_phone", "inviter_mobile_phone", "inviter_email", "inviter_phone"]
                },
                {
                    "name": "초청 사유",
                    "name_en": "Invitation Reason",
                    "icon": "📝",
                    "fields": ["invitation_reason", "inviter_household_members", "prior_invitation_history", "prior_invited_person_details"]
                },
                {
                    "name": "법규 위반 이력",
                    "name_en": "Violation History",
                    "icon": "⚖️",
                    "fields": ["inviter_law_violation_record", "invited_foreigner_violation_record"]
                }
            ]
        },
        "사증발급인정신청서": {
            "icon": "📄",
            "description": "피초청인 사증 발급 신청",
            "description_en": "Invitee visa issuance application",
            "sections": [
                {
                    "name": "피초청인 기본정보",
                    "name_en": "Invitee Basic Info",
                    "icon": "👤",
                    "fields": ["has_used_other_names", "has_multiple_nationalities", "home_country_address", "phone_alt"]
                },
                {
                    "name": "여권 정보",
                    "name_en": "Passport Info",
                    "icon": "🛂",
                    "fields": ["passport_type_other", "passport_place_of_issue", "has_other_passport", "other_passport_type", "other_passport_no", "other_passport_country", "other_passport_expiry"]
                },
                {
                    "name": "혼인/가족 사항",
                    "name_en": "Marriage/Family",
                    "icon": "💒",
                    "fields": ["marital_status", "has_children", "children_count"]
                },
                {
                    "name": "학력/직업",
                    "name_en": "Education/Occupation",
                    "icon": "🎓",
                    "fields": ["education_level", "education_other_details", "school_name", "school_location", "occupation_status", "occupation_other_details"]
                },
                {
                    "name": "방문 정보",
                    "name_en": "Visit Info",
                    "icon": "✈️",
                    "fields": ["purpose_of_visit", "purpose_other_details", "intended_stay_period", "intended_entry_date", "address_in_korea", "contact_in_korea_phone"]
                },
                {
                    "name": "과거 방문 이력",
                    "name_en": "Visit History",
                    "icon": "📅",
                    "fields": ["past_korea_visits", "past_travel_country", "past_travel_purpose", "past_travel_period", "relationship_to_inviter", "family_members_info", "previous_visit_korea", "previous_violation_korea"]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 정보",
                    "name_en": "Guarantor Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth", "guarantor_phone", "guarantor_address", "guarantor_relationship", "guarantor_employer", "guarantor_position", "guarantor_employer_address", "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    },
    "E": {  # 전문 인력 (E-7)
        "사증발급인정신청서": {
            "icon": "📄",
            "description": "전문인력 사증 발급 신청",
            "description_en": "Professional worker visa application",
            "sections": [
                {
                    "name": "신청인 기본정보",
                    "name_en": "Applicant Basic Info",
                    "icon": "👤",
                    "fields": ["has_used_other_names", "has_multiple_nationalities", "home_country_address", "phone_alt", "marital_status", "has_children", "children_count"]
                },
                {
                    "name": "여권 정보",
                    "name_en": "Passport Info",
                    "icon": "🛂",
                    "fields": ["passport_type_other", "passport_place_of_issue", "has_other_passport", "other_passport_type", "other_passport_no", "other_passport_country", "other_passport_expiry"]
                },
                {
                    "name": "학력 정보",
                    "name_en": "Education",
                    "icon": "🎓",
                    "fields": ["education_level", "education_other_details", "school_name", "school_location", "education_school_name", "education_degree", "education_major", "education_graduation_year"]
                },
                {
                    "name": "경력 정보",
                    "name_en": "Work Experience",
                    "icon": "💼",
                    "fields": ["occupation_status", "occupation_other_details", "experience_company", "experience_period", "experience_field", "experience_position"]
                },
                {
                    "name": "방문 정보",
                    "name_en": "Visit Info",
                    "icon": "✈️",
                    "fields": ["purpose_of_visit", "purpose_other_details", "intended_stay_period", "intended_entry_date", "address_in_korea", "contact_in_korea_phone", "past_korea_visits", "past_travel_country", "past_travel_purpose", "past_travel_period"]
                }
            ]
        },
        "고용사유서": {
            "icon": "📝",
            "description": "고용 사유 및 활용 계획",
            "description_en": "Employment reason and utilization plan",
            "sections": [
                {
                    "name": "고용 예정 정보",
                    "name_en": "Employment Plan",
                    "icon": "📋",
                    "fields": ["employment_period", "sojourn_status", "job_field", "job_title", "workplace", "salary_and_benefits"]
                },
                {
                    "name": "고용 회사 정보",
                    "name_en": "Employer Company Info",
                    "icon": "🏢",
                    "fields": ["employer_company_name", "employer_business_registration_no", "employer_representative_name", "employer_address", "employer_phone"]
                },
                {
                    "name": "회사 재무 정보",
                    "name_en": "Company Financials",
                    "icon": "💰",
                    "fields": ["employer_capital_amount", "employer_total_sales", "employer_total_liabilities", "employer_operating_profit", "employer_num_employees", "employer_num_foreign_professionals"]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 정보",
                    "name_en": "Guarantor Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth", "guarantor_phone", "guarantor_address", "guarantor_relationship", "guarantor_employer", "guarantor_position", "guarantor_employer_address", "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    },
    "F": {  # 국적 귀화
        "귀화허가신청서": {
            "icon": "🏛️",
            "description": "귀화 허가 신청 기본 정보",
            "description_en": "Naturalization application basic info",
            "sections": [
                {
                    "name": "신청인 인적사항",
                    "name_en": "Applicant Personal Info",
                    "icon": "👤",
                    "fields": ["birth_place", "full_name_en", "phone_home", "intended_registered_domicile", "occupation"]
                },
                {
                    "name": "소득/재산 정보",
                    "name_en": "Income & Assets",
                    "icon": "💰",
                    "fields": ["monthly_income", "last_year_income", "real_estate_assets_amount", "financial_assets_amount"]
                },
                {
                    "name": "위반 이력",
                    "name_en": "Violation History",
                    "icon": "⚖️",
                    "fields": ["offense_date", "offense_details", "disposition_result", "tax_arrears_amount", "health_insurance_arrears_amount"]
                },
                {
                    "name": "국민 의무 동의",
                    "name_en": "Citizen Duties Agreement",
                    "icon": "🇰🇷",
                    "fields": ["oath_participation", "law_compliance_agree", "four_duties_ack"]
                },
                {
                    "name": "건강/장애 사항",
                    "name_en": "Health/Disability",
                    "icon": "🏥",
                    "fields": ["disability_type", "disability_grade", "disease_type", "disease_status"]
                },
                {
                    "name": "자격/수상/활동",
                    "name_en": "Qualifications & Activities",
                    "icon": "🏆",
                    "fields": ["award_name", "award_issuer", "license_name", "license_grade", "volunteer_activity", "community_activity", "organization_name", "activity_period", "commendation_for_good_deed", "blood_donation_times"]
                },
                {
                    "name": "서명",
                    "name_en": "Signature",
                    "icon": "✍️",
                    "fields": ["signature_name"]
                }
            ]
        },
        "신원보증서": {
            "icon": "🤝",
            "description": "신원보증인의 보증 내용",
            "description_en": "Guarantor's guarantee details",
            "sections": [
                {
                    "name": "보증인 정보",
                    "name_en": "Guarantor Info",
                    "icon": "👤",
                    "fields": ["guarantor_name", "guarantor_name_hanja", "guarantor_nationality", "guarantor_gender", "guarantor_passport_or_birth", "guarantor_phone", "guarantor_address", "guarantor_relationship", "guarantor_employer", "guarantor_position", "guarantor_employer_address", "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"]
                }
            ]
        }
    }
}


# =============================================================================
# 필드 정의 조회 헬퍼
# =============================================================================

def get_field_definition(scenario_id: str, field_key: str) -> Optional[Dict]:
    """scenario_id의 Layer2 필드 정의에서 field_key에 해당하는 필드 찾기"""
    field_groups = get_layer2_field_groups(scenario_id)
    for group in field_groups:
        for field in group.get('fields', []):
            if field.get('data_key') == field_key:
                return field
    return None


def get_all_field_definitions(scenario_id: str) -> Dict[str, Dict]:
    """scenario_id의 모든 Layer2 필드를 딕셔너리로 반환"""
    field_groups = get_layer2_field_groups(scenario_id)
    all_fields = {}
    for group in field_groups:
        for field in group.get('fields', []):
            all_fields[field.get('data_key')] = field
    return all_fields


# =============================================================================
# 메인 렌더 함수
# =============================================================================

def render():
    """시나리오 폼 페이지 렌더링"""
    
    scenario_id = st.session_state.get('selected_scenario')
    
    if not scenario_id:
        st.warning("시나리오를 먼저 선택해주세요.")
        if st.button("← 대시보드로 돌아가기"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        return
    
    scenario = SCENARIOS.get(scenario_id)
    if not scenario:
        st.error("유효하지 않은 시나리오입니다.")
        return
    
    current_step = st.session_state.get('form_step', 1)
    
    # 새로고침 경고 (Phase 2, 3에서만)
    if current_step in [2, 3]:
        st.warning("⚠️ 주의: 새로고침 또는 페이지 이탈 시 작성 중인 내용이 저장되지 않을 수 있습니다.")
    
    # 상단 Phase 진행 표시
    render_phase_indicator(current_step)
    
    if current_step == 1:
        render_phase1_universal_fact(scenario)
    elif current_step == 2:
        render_phase2_document_based(scenario)  # 새로운 Phase 2
    elif current_step == 3:
        render_phase3_narrative(scenario)
    elif current_step == 4:
        render_phase4_payment(scenario)


# =============================================================================
# Phase Indicator
# =============================================================================

def render_phase_indicator(current_step: int):
    """4-Phase 진행 상태 표시"""
    
    phases = [
        {"name": "기본정보 확인", "desc": "Universal Fact", "color": "#22c55e"},
        {"name": "서류별 정보 입력", "desc": "Variable Fact", "color": "#3b82f6"},
        {"name": "서술형 작성", "desc": "Narrative", "color": "#a855f7"},
        {"name": "결제 & 생성", "desc": "Payment", "color": "#f59e0b"},
    ]
    
    cols = st.columns(4)
    
    for i, (col, phase) in enumerate(zip(cols, phases)):
        step_num = i + 1
        is_active = current_step == step_num
        is_done = current_step > step_num
        
        with col:
            if is_active:
                bg_color = phase['color'] + "20"
                border_color = phase['color']
                badge_bg = phase['color']
                opacity = "1"
            elif is_done:
                bg_color = "#f0fdf4"
                border_color = "#86efac"
                badge_bg = "#22c55e"
                opacity = "1"
            else:
                bg_color = "#f8fafc"
                border_color = "#e2e8f0"
                badge_bg = "#94a3b8"
                opacity = "0.6"
            
            st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 12px;
                    text-align: center;
                    opacity: {opacity};
                    transition: all 0.3s;
                ">
                    <div style="
                        background: {badge_bg};
                        color: white;
                        font-size: 11px;
                        font-weight: 700;
                        padding: 2px 8px;
                        border-radius: 20px;
                        display: inline-block;
                        margin-bottom: 6px;
                    ">{'✓ ' if is_done else '● ' if is_active else ''}STEP {step_num}</div>
                    <div style="font-weight: 600; font-size: 13px; color: #1e293b;">{phase['name']}</div>
                    <div style="font-size: 11px; color: #64748b;">{phase['desc']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)


# =============================================================================
# Phase 1: Universal Fact
# =============================================================================

def render_phase1_universal_fact(scenario):
    """Phase 1: 회원가입 시 입력된 불변 정보 확인"""
    
    user_data = st.session_state.get('user_data', {})
    
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h2 style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0 0 0.5rem 0;">
                {scenario.icon} {scenario.name} <span style="color: #64748b; font-weight: 400;">({scenario.visa_type})</span>
            </h2>
            <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
                회원가입 시 입력한 기본 정보를 확인해주세요. 이 정보는 모든 서류에 자동으로 반영됩니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← 다른 시나리오 선택", use_container_width=True):
            st.session_state.selected_scenario = None
            st.session_state.form_step = 1
            st.session_state.form_data = {}
            st.session_state.narrative_data = {}
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 카테고리별 카드
    categories = {
        "personal": {"title": "인적사항", "icon": "👤", "color": "#3b82f6"},
        "passport": {"title": "여권 정보", "icon": "🛂", "color": "#8b5cf6"},
        "contact": {"title": "연락처", "icon": "📞", "color": "#10b981"},
    }
    
    fields_by_category = {}
    for field in LAYER1_UNIVERSAL_FIELDS:
        cat = field.get('category', 'other')
        if cat not in fields_by_category:
            fields_by_category[cat] = []
        fields_by_category[cat].append(field)
    
    cols = st.columns(3)
    
    for idx, (cat_key, cat_info) in enumerate(list(categories.items())[:3]):
        with cols[idx]:
            fields = fields_by_category.get(cat_key, [])
            
            st.markdown(f"""
                <div style="
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 1rem;
                    height: 100%;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        margin-bottom: 12px;
                        padding-bottom: 8px;
                        border-bottom: 2px solid {cat_info['color']}20;
                    ">
                        <span style="font-size: 1.2rem;">{cat_info['icon']}</span>
                        <span style="font-weight: 600; color: #1e293b;">{cat_info['title']}</span>
                    </div>
            """, unsafe_allow_html=True)
            
            for field in fields:
                data_key = field['data_key']
                label = field['label']
                value = user_data.get(data_key, '-')
                
                if field['type'] == 'date' and value and value != '-':
                    try:
                        if hasattr(value, 'strftime'):
                            value = value.strftime('%Y-%m-%d')
                    except:
                        pass
                
                st.markdown(f"""
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        padding: 6px 0;
                        border-bottom: 1px solid #f1f5f9;
                    ">
                        <span style="color: #64748b; font-size: 0.8rem;">{label}</span>
                        <span style="color: #1e293b; font-weight: 500; font-size: 0.8rem;">{value or '-'}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 생성될 서류 미리보기
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #eff6ff, #dbeafe);
            border: 1px solid #93c5fd;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        ">
            <div style="font-weight: 600; color: #1e40af; margin-bottom: 8px;">
                📄 이번 신청에서 작성할 서류
            </div>
    """, unsafe_allow_html=True)
    
    doc_cols = st.columns(len(scenario.required_docs))
    for idx, doc_name in enumerate(scenario.required_docs):
        doc_info = DOCUMENT_FIELD_MAPPING.get(scenario.id, {}).get(doc_name, {})
        icon = doc_info.get('icon', '📄')
        with doc_cols[idx]:
            st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                    border: 1px solid #bfdbfe;
                ">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="font-size: 0.75rem; color: #1e40af; font-weight: 500;">{doc_name}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✓ 정보 확인 완료 → 서류 작성 시작", type="primary", use_container_width=True):
        # Phase 2 초기화
        st.session_state.form_step = 2
        st.session_state.current_doc_index = 0
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {}
        st.rerun()


# =============================================================================
# Phase 2: Document-Based Form (새로운 UI)
# =============================================================================

def render_phase2_document_based(scenario):
    """Phase 2: 서류 기반 스텝 폼"""
    
    scenario_id = scenario.id
    doc_mapping = DOCUMENT_FIELD_MAPPING.get(scenario_id, {})
    required_docs = scenario.required_docs
    
    # 매핑에 있는 서류만 필터링
    available_docs = [doc for doc in required_docs if doc in doc_mapping]
    
    if not available_docs:
        st.warning("이 시나리오에 대한 서류 설정이 없습니다.")
        if st.button("다음 단계로 →"):
            st.session_state.form_step = 3
            st.rerun()
        return
    
    # 현재 서류 인덱스
    if 'current_doc_index' not in st.session_state:
        st.session_state.current_doc_index = 0
    
    current_idx = st.session_state.current_doc_index
    total_docs = len(available_docs)
    
    # 범위 체크
    if current_idx >= total_docs:
        current_idx = total_docs - 1
        st.session_state.current_doc_index = current_idx
    
    current_doc_name = available_docs[current_idx]
    current_doc_info = doc_mapping[current_doc_name]
    
    # 폼 데이터 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # 전체 필드 정의 가져오기
    all_field_defs = get_all_field_definitions(scenario_id)
    
    # ==========================================================================
    # 상단: 서류 탭 네비게이션
    # ==========================================================================
    
    render_document_tabs(available_docs, current_idx, doc_mapping, all_field_defs)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================================================
    # 현재 서류 헤더
    # ==========================================================================
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            color: white;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.5rem;">{current_doc_info.get('icon', '📄')}</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.4rem; font-weight: 700;">{current_doc_name}</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                        {current_doc_info.get('description', '')}
                    </p>
                    <p style="margin: 2px 0 0 0; opacity: 0.7; font-size: 0.8rem;">
                        {current_doc_info.get('description_en', '')}
                    </p>
                </div>
            </div>
            <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                margin-top: 12px;
                padding-top: 12px;
                border-top: 1px solid rgba(255,255,255,0.2);
            ">
                <span style="font-size: 0.85rem; opacity: 0.9;">서류 {current_idx + 1} / {total_docs}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ==========================================================================
    # 섹션별 폼 렌더링
    # ==========================================================================
    
    sections = current_doc_info.get('sections', [])
    
    with st.form(f"doc_form_{current_doc_name}"):
        for section in sections:
            render_section_card(section, all_field_defs, scenario_id)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 네비게이션 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_idx > 0:
                prev_btn = st.form_submit_button("← 이전 서류", use_container_width=True)
            else:
                prev_btn = st.form_submit_button("← Phase 1로", use_container_width=True)
        
        with col2:
            save_btn = st.form_submit_button("💾 임시 저장", use_container_width=True)
        
        with col3:
            if current_idx < total_docs - 1:
                next_btn = st.form_submit_button("다음 서류 →", type="primary", use_container_width=True)
            else:
                next_btn = st.form_submit_button("서술형 작성 →", type="primary", use_container_width=True)
        
        # 버튼 액션 처리
        if prev_btn:
            save_current_form_data(sections, all_field_defs)
            if current_idx > 0:
                st.session_state.current_doc_index = current_idx - 1
            else:
                st.session_state.form_step = 1
            st.rerun()
        
        if save_btn:
            save_current_form_data(sections, all_field_defs)
            st.success("✓ 임시 저장되었습니다!")
        
        if next_btn:
            save_current_form_data(sections, all_field_defs)
            if current_idx < total_docs - 1:
                st.session_state.current_doc_index = current_idx + 1
            else:
                st.session_state.form_step = 3
            st.rerun()


def render_document_tabs(docs: List[str], current_idx: int, doc_mapping: Dict, all_field_defs: Dict):
    """서류 탭 네비게이션 렌더링 - Streamlit columns 사용"""
    
    # 전체 진행률 계산
    total_filled = 0
    total_fields = 0
    doc_progress_list = []
    
    for doc_name in docs:
        doc_info = doc_mapping.get(doc_name, {})
        sections = doc_info.get('sections', [])
        f, t = calculate_section_progress(sections, all_field_defs)
        total_filled += f
        total_fields += t
        doc_progress_list.append((f, t))
    
    overall_progress = int((total_filled / total_fields) * 100) if total_fields > 0 else 0
    
    # 서류 탭을 Streamlit columns로 표시
    cols = st.columns(len(docs))
    
    for idx, (col, doc_name) in enumerate(zip(cols, docs)):
        doc_info = doc_mapping.get(doc_name, {})
        icon = doc_info.get('icon', '📄')
        filled, total = doc_progress_list[idx]
        is_complete = filled == total and total > 0
        
        with col:
            # 스타일 결정
            if idx == current_idx:
                bg_color = "white"
                border_style = "2px solid #3b82f6"
                shadow = "box-shadow: 0 2px 8px rgba(59,130,246,0.3);"
                opacity = "1"
            elif is_complete:
                bg_color = "#f0fdf4"
                border_style = "1px solid #86efac"
                shadow = ""
                opacity = "1"
            else:
                bg_color = "#f8fafc"
                border_style = "1px solid #e2e8f0"
                shadow = ""
                opacity = "0.7"
            
            progress_text = f"{filled}/{total}" if total > 0 else "0/0"
            check_mark = "✓ " if is_complete else ""
            
            # 서류명 줄이기
            short_name = doc_name if len(doc_name) <= 6 else doc_name[:5] + "..."
            
            st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border: {border_style};
                    border-radius: 12px;
                    padding: 12px 8px;
                    text-align: center;
                    opacity: {opacity};
                    {shadow}
                ">
                    <div style="font-size: 1.5rem; margin-bottom: 4px;">{icon}</div>
                    <div style="font-size: 0.7rem; font-weight: 600; color: #1e293b;">
                        {check_mark}{short_name}
                    </div>
                    <div style="font-size: 0.65rem; color: #64748b; margin-top: 2px;">{progress_text}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # 전체 진행률 바
    progress_color = '#22c55e' if overall_progress == 100 else '#3b82f6'
    
    st.markdown(f"""
        <div style="margin-top: 12px; padding: 0 4px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-bottom: 6px;">
                <span>전체 진행률</span>
                <span style="font-weight: 600; color: {progress_color};">{overall_progress}%</span>
            </div>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; overflow: hidden;">
                <div style="
                    background: linear-gradient(90deg, #3b82f6, #1d4ed8);
                    height: 100%;
                    width: {overall_progress}%;
                    border-radius: 10px;
                "></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def calculate_section_progress(sections: List[Dict], all_field_defs: Dict) -> Tuple[int, int]:
    """섹션의 필드 채움 진행률 계산"""
    filled = 0
    total = 0
    
    form_data = st.session_state.get('form_data', {})
    
    for section in sections:
        for field_key in section.get('fields', []):
            if field_key in all_field_defs:
                total += 1
                value = form_data.get(field_key, '')
                if value and str(value).strip():
                    filled += 1
    
    return filled, total


def render_section_card(section: Dict, all_field_defs: Dict, scenario_id: str):
    """섹션 카드 렌더링"""
    
    section_name = section.get('name', '')
    section_name_en = section.get('name_en', '')
    section_icon = section.get('icon', '📋')
    field_keys = section.get('fields', [])
    
    # 섹션 헤더
    st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            margin-bottom: 1rem;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #f1f5f9, #e2e8f0);
                padding: 12px 16px;
                border-bottom: 1px solid #e2e8f0;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <span style="font-size: 1.2rem;">{section_icon}</span>
                <div>
                    <span style="font-weight: 600; color: #1e293b; font-size: 0.95rem;">{section_name}</span>
                    <span style="color: #64748b; font-size: 0.8rem; margin-left: 8px;">{section_name_en}</span>
                </div>
                <span style="
                    margin-left: auto;
                    background: #dbeafe;
                    color: #1d4ed8;
                    font-size: 0.7rem;
                    padding: 2px 8px;
                    border-radius: 10px;
                ">{len(field_keys)}개 항목</span>
            </div>
            <div style="padding: 16px;">
    """, unsafe_allow_html=True)
    
    # 필드들을 2열로 배치
    valid_fields = [k for k in field_keys if k in all_field_defs]
    
    if len(valid_fields) > 0:
        # 2열 레이아웃
        col1, col2 = st.columns(2)
        
        for idx, field_key in enumerate(valid_fields):
            field_def = all_field_defs[field_key]
            col = col1 if idx % 2 == 0 else col2
            
            with col:
                render_styled_field(field_key, field_def)
    else:
        st.info("이 섹션에 해당하는 필드가 없습니다.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_styled_field(field_key: str, field_def: Dict):
    """스타일링된 개별 필드 렌더링"""
    
    label = field_def.get('label', field_key)
    label_en = field_def.get('label_en', '')
    field_type = field_def.get('type', 'text')
    required = field_def.get('required', False)
    options = field_def.get('options', [])
    placeholder = field_def.get('placeholder', '')
    
    # 현재 값
    current_value = st.session_state.form_data.get(field_key, '')
    
    # 라벨 조합
    display_label = label
    if label_en and label_en != label:
        # 라벨이 너무 길면 줄임
        if len(label) > 20:
            display_label = label[:20] + "..."
        if len(label_en) > 20:
            label_en = label_en[:20] + "..."
        display_label = f"{display_label}"
    
    if required:
        display_label += " *"
    
    # 필드 렌더링
    if field_type == 'text':
        st.text_input(
            display_label,
            value=current_value,
            key=f"field_{field_key}",
            placeholder=placeholder or label_en,
            help=label_en if label_en else None
        )
    
    elif field_type == 'textarea':
        st.text_area(
            display_label,
            value=current_value,
            key=f"field_{field_key}",
            placeholder=placeholder,
            height=100,
            help=label_en if label_en else None
        )
    
    elif field_type == 'select':
        if not options:
            options = ['']
        default_idx = 0
        if current_value and current_value in options:
            default_idx = options.index(current_value)
        st.selectbox(
            display_label,
            options=options,
            index=default_idx,
            key=f"field_{field_key}",
            help=label_en if label_en else None
        )
    
    elif field_type == 'date':
        default_date = date.today()
        if current_value:
            try:
                if isinstance(current_value, str):
                    default_date = datetime.strptime(current_value, '%Y-%m-%d').date()
                elif isinstance(current_value, date):
                    default_date = current_value
            except:
                pass
        st.date_input(
            display_label,
            value=default_date,
            key=f"field_{field_key}",
            help=label_en if label_en else None
        )
    
    elif field_type == 'number':
        min_val = field_def.get('min_value', 0)
        st.number_input(
            display_label,
            value=int(current_value) if current_value else min_val,
            min_value=min_val,
            key=f"field_{field_key}",
            help=label_en if label_en else None
        )
    
    else:
        st.text_input(
            display_label,
            value=current_value,
            key=f"field_{field_key}",
            placeholder=placeholder,
            help=label_en if label_en else None
        )


def save_current_form_data(sections: List[Dict], all_field_defs: Dict):
    """현재 폼 데이터 저장"""
    
    for section in sections:
        for field_key in section.get('fields', []):
            widget_key = f"field_{field_key}"
            if widget_key in st.session_state:
                value = st.session_state[widget_key]
                
                # 날짜 변환
                if hasattr(value, 'strftime'):
                    value = value.strftime('%Y-%m-%d')
                
                st.session_state.form_data[field_key] = value


# =============================================================================
# Phase 3: Narrative (서술형)
# =============================================================================

def render_phase3_narrative(scenario):
    """Phase 3: 서술형 데이터 입력 + AI 검토"""
    
    scenario_id = scenario.id
    narrative_config = get_narrative_config(scenario_id)
    layer3_fields = get_layer3_fields(scenario_id)
    danger_patterns = get_danger_patterns(scenario_id)
    
    if 'narrative_data' not in st.session_state:
        st.session_state.narrative_data = {}
    
    if 'ai_feedbacks' not in st.session_state:
        st.session_state.ai_feedbacks = []
    
    narrative_label = narrative_config.get('narrative_label', '서술형 작성')
    
    # 서술형이 없는 시나리오 처리
    if not layer3_fields:
        st.markdown(f"""
            <div style="
                background: #f0fdf4;
                border: 2px solid #86efac;
                border-radius: 16px;
                padding: 2rem;
                text-align: center;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
                <h3 style="color: #166534; margin: 0 0 0.5rem 0;">서술형 항목이 없습니다</h3>
                <p style="color: #15803d; margin: 0;">이 시나리오는 서술형 작성이 필요하지 않습니다.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Phase 2로 돌아가기", use_container_width=True):
                st.session_state.form_step = 2
                st.rerun()
        with col2:
            if st.button("결제하기 →", type="primary", use_container_width=True):
                st.session_state.form_step = 4
                st.rerun()
        return
    
    # 헤더
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            color: white;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.5rem;">✍️</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.4rem; font-weight: 700;">{narrative_label}</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                        각 항목에 대해 상세히 작성해주세요. AI가 실시간으로 검토합니다.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2컬럼 레이아웃: 폼 | 피드백
    form_col, feedback_col = st.columns([2, 1])
    
    with form_col:
        for i, field in enumerate(layer3_fields):
            render_narrative_field(i, field, danger_patterns)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_validate, _ = st.columns([1, 1])
        with col_validate:
            if st.button("🤖 AI 검토 요청", use_container_width=True):
                run_ai_validation(layer3_fields, danger_patterns)
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_back, col_next = st.columns(2)
        
        with col_back:
            if st.button("← Phase 2로 돌아가기", use_container_width=True):
                st.session_state.form_step = 2
                st.rerun()
        
        with col_next:
            if st.button("✓ 작성 완료 → 결제하기", use_container_width=True, type="primary"):
                missing = validate_narrative_fields(layer3_fields)
                if missing:
                    st.error(f"필수 항목을 작성해주세요: {', '.join(missing)}")
                else:
                    st.session_state.form_step = 4
                    st.rerun()
    
    with feedback_col:
        render_ai_feedback_panel(layer3_fields)


def render_narrative_field(index: int, field: Dict, danger_patterns: List[str]):
    """서술형 필드 렌더링"""
    
    data_key = field['data_key']
    label = field.get('label', data_key)
    label_en = field.get('label_en', '')
    hint = field.get('hint', '')
    placeholder = field.get('placeholder', '')
    min_chars = field.get('min_chars', 50)
    required = field.get('required', False)
    
    current_value = st.session_state.narrative_data.get(data_key, '')
    
    # 카드 스타일
    st.markdown(f"""
        <div style="
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        ">
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 10px;
                margin-bottom: 8px;
            ">
                <span style="
                    background: #7c3aed;
                    color: white;
                    font-size: 0.75rem;
                    font-weight: 700;
                    padding: 2px 8px;
                    border-radius: 6px;
                ">Q{index + 1}</span>
                <div>
                    <div style="font-weight: 600; color: #1e293b; font-size: 0.9rem;">
                        {label} {'*' if required else ''}
                    </div>
                    <div style="color: #64748b; font-size: 0.75rem;">{label_en}</div>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    if hint:
        st.caption(f"💡 {hint}")
    
    answer = st.text_area(
        f"답변 입력",
        value=current_value,
        height=120,
        key=f"narrative_{data_key}",
        placeholder=placeholder,
        label_visibility="collapsed"
    )
    
    st.session_state.narrative_data[data_key] = answer
    
    # 글자수 표시
    char_count = len(answer)
    color = "#22c55e" if char_count >= min_chars else "#f59e0b" if char_count > 0 else "#ef4444"
    
    st.markdown(f"""
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 8px;
            ">
                <div style="font-size: 0.7rem; color: #94a3b8;">최소 {min_chars}자 이상 작성</div>
                <div style="
                    font-size: 0.75rem;
                    font-weight: 600;
                    color: {color};
                ">{char_count} / {min_chars}자</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def run_ai_validation(fields: List[Dict], danger_patterns: List[str]):
    """AI 검토 실행"""
    import re
    
    feedbacks = []
    
    for field in fields:
        data_key = field['data_key']
        answer = st.session_state.narrative_data.get(data_key, '')
        label = field.get('label', data_key)
        min_chars = field.get('min_chars', 50)
        
        if len(answer) == 0:
            feedbacks.append({
                'field': label[:15] + '...' if len(label) > 15 else label,
                'type': 'error',
                'message': '아직 작성되지 않았습니다.'
            })
            continue
        
        if len(answer) < min_chars:
            feedbacks.append({
                'field': label[:15] + '...' if len(label) > 15 else label,
                'type': 'warning',
                'message': f'내용이 부족합니다. ({len(answer)}/{min_chars}자)'
            })
            continue
        
        found_dangers = [p for p in danger_patterns if p in answer]
        if found_dangers:
            feedbacks.append({
                'field': label[:15] + '...' if len(label) > 15 else label,
                'type': 'error',
                'message': f'위험 표현: "{found_dangers[0]}"'
            })
            continue
        
        feedbacks.append({
            'field': label[:15] + '...' if len(label) > 15 else label,
            'type': 'success',
            'message': '잘 작성되었습니다 ✓'
        })
    
    st.session_state.ai_feedbacks = feedbacks


def render_ai_feedback_panel(fields: List[Dict]):
    """AI 피드백 패널 - Streamlit 네이티브 컴포넌트 사용"""
    
    feedbacks = st.session_state.get('ai_feedbacks', [])
    
    # 진행률
    total = len(fields)
    completed = sum(
        1 for f in fields 
        if len(st.session_state.narrative_data.get(f['data_key'], '')) >= f.get('min_chars', 50)
    )
    progress = int((completed / total) * 100) if total > 0 else 0
    progress_color = '#22c55e' if progress == 100 else '#3b82f6'
    
    # 컨테이너로 감싸기
    with st.container():
        st.markdown("#### 📊 작성 진행률")
        
        # 진행률 바
        st.markdown(f"""
            <div style="
                background: #e2e8f0;
                border-radius: 10px;
                height: 10px;
                overflow: hidden;
                margin-bottom: 8px;
            ">
                <div style="
                    background: linear-gradient(90deg, #22c55e, #16a34a);
                    height: 100%;
                    width: {progress}%;
                    border-radius: 10px;
                "></div>
            </div>
            <div style="
                display: flex;
                justify-content: space-between;
                font-size: 0.85rem;
                color: #64748b;
                margin-bottom: 16px;
            ">
                <span>{completed}/{total} 완료</span>
                <span style="font-weight: 600; color: {progress_color};">{progress}%</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🤖 AI 피드백")
        
        if feedbacks:
            for fb in feedbacks:
                fb_type = fb.get('type', 'info')
                
                if fb_type == 'error':
                    st.error(f"**{fb.get('field', '')}**: {fb.get('message', '')}")
                elif fb_type == 'warning':
                    st.warning(f"**{fb.get('field', '')}**: {fb.get('message', '')}")
                elif fb_type == 'success':
                    st.success(f"**{fb.get('field', '')}**: {fb.get('message', '')}")
                else:
                    st.info(f"**{fb.get('field', '')}**: {fb.get('message', '')}")
        else:
            st.info("'AI 검토 요청' 버튼을 클릭해주세요")


def validate_narrative_fields(fields: List[Dict]) -> List[str]:
    """필수 서술형 필드 검증"""
    missing = []
    for field in fields:
        if field.get('required', False):
            data_key = field['data_key']
            min_chars = field.get('min_chars', 50)
            answer = st.session_state.narrative_data.get(data_key, '')
            if len(answer) < min_chars:
                missing.append(field.get('label', data_key)[:20])
    return missing


# =============================================================================
# Phase 4: Payment
# =============================================================================

def render_phase4_payment(scenario):
    """Phase 4: 결제 & 문서 생성"""
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            color: white;
        ">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2.5rem;">💳</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.4rem; font-weight: 700;">결제 & 문서 생성</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                        결제 완료 후 {len(scenario.required_docs)}개의 문서가 자동으로 생성됩니다.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    is_paid = st.session_state.get('is_paid', False)
    is_admin = st.session_state.get('is_admin', False)
    
    if is_paid or is_admin:
        st.success("✅ Premium 활성화 상태입니다!")
        
        # 생성될 서류 표시
        st.markdown("### 📄 생성될 서류")
        
        cols = st.columns(min(len(scenario.required_docs), 4))
        for idx, doc_name in enumerate(scenario.required_docs):
            doc_info = DOCUMENT_FIELD_MAPPING.get(scenario.id, {}).get(doc_name, {})
            icon = doc_info.get('icon', '📄')
            with cols[idx % len(cols)]:
                st.markdown(f"""
                    <div style="
                        background: #f0fdf4;
                        border: 1px solid #86efac;
                        border-radius: 10px;
                        padding: 1rem;
                        text-align: center;
                    ">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div style="font-size: 0.8rem; color: #166534; font-weight: 500; margin-top: 4px;">
                            {doc_name}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📄 문서 생성하기", type="primary", use_container_width=True):
            generate_documents(scenario)
    
    else:
        render_payment_ui(scenario)
    
    st.markdown("---")
    
    if st.button("← Phase 3로 돌아가기", use_container_width=True):
        st.session_state.form_step = 3
        st.rerun()


def render_payment_ui(scenario):
    """결제 UI"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e40af, #3b82f6);
                border-radius: 16px;
                padding: 2rem;
                text-align: center;
                color: white;
            ">
                <div style="font-size: 1rem; opacity: 0.9;">Premium Plan</div>
                <div style="font-size: 3rem; font-weight: 700; margin: 0.5rem 0;">${scenario.price}</div>
                <div style="opacity: 0.8;">일회성 결제 · 평생 이용</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            ### ✨ Premium 혜택
            
            - ✅ **AI 문서 자동 생성**
            - ✅ **전문가 수준 서류 작성**
            - ✅ **ZIP 패키지 다운로드**
            - ✅ **무제한 수정 & 재생성**
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    payment_service = PaymentService()
    
    if payment_service.is_stripe_connected():
        if st.button("💳 카드 결제하기", type="primary", use_container_width=True):
            user_id = st.session_state.get('user_id', '')
            user_email = st.session_state.get('user_email', '')
            
            with st.spinner("결제 페이지 생성 중..."):
                checkout_url, session_id = payment_service.create_checkout_session(user_id, user_email)
            
            if checkout_url:
                st.session_state.checkout_url = checkout_url
                st.session_state.checkout_session_id = session_id
                st.markdown(f"[**👉 결제 페이지로 이동**]({checkout_url})")
    else:
        st.warning("⚠️ 테스트 모드")
        if st.button("🧪 테스트 결제 (무료)", type="primary", use_container_width=True):
            st.session_state.is_paid = True
            st.success("🎉 테스트 결제 완료!")
            st.rerun()


def generate_documents(scenario):
    """문서 생성"""
    from services.document_service import DocumentService
    
    user_data = st.session_state.get('user_data', {})
    form_data = st.session_state.get('form_data', {})
    narrative_data = st.session_state.get('narrative_data', {})
    
    required_docs = scenario.required_docs
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    doc_service = DocumentService()
    
    import io
    import zipfile
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, doc_name in enumerate(required_docs):
            progress = int(((idx + 1) / len(required_docs)) * 100)
            progress_bar.progress(progress)
            status_text.text(f"📝 {doc_name} 생성 중... ({idx + 1}/{len(required_docs)})")
            
            try:
                doc_bytes = doc_service.generate_document(doc_name, user_data, form_data, narrative_data)
                safe_name = doc_name.replace(' ', '_')
                zip_file.writestr(f"{safe_name}.docx", doc_bytes)
            except Exception as e:
                zip_file.writestr(f"ERROR_{doc_name}.txt", f"오류: {str(e)}".encode('utf-8'))
    
    progress_bar.progress(100)
    status_text.text("✅ 모든 문서 생성 완료!")
    
    zip_buffer.seek(0)
    st.session_state.generated_zip = zip_buffer.getvalue()
    st.session_state.current_page = 'document_preview'
    
    import time
    time.sleep(0.5)
    st.rerun()