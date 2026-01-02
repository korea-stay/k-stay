"""
K-Stay Scenario Form Page - Redesigned
서류 기반 Step-by-Step UI with Progress Tracking
TABLE_ROWS 동적 테이블 입력 지원

핵심 개선사항:
1. 서류 단위로 스텝 분리 (탭 네비게이션)
2. 전체/현재 서류 진행률 시각화
3. 중복 필드 자동 동기화
4. 카드 기반 깔끔한 섹션 UI
5. 서류별 설명 및 맥락 제공
6. TABLE_ROWS 동적 테이블 입력 (가족, 초청 이력 등)
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
    get_table_rows_fields,  # ★ TABLE_ROWS 필드 가져오기
)
from services.payment_service import PaymentService


# =============================================================================
# 서류-필드 매핑 정의 (시나리오별)
# =============================================================================
NATURALIZATION_TYPE_OPTIONS = {
    "general": {
        "label": "일반귀화",
        "label_en": "General Naturalization",
        "requirement": "※ 국내 5년 이상 체류",
        "color": "#3b82f6",
        "sub_options": [
            {
                "value": "general_permanent_resident",
                "label": "「민법」상 성년이며 영주자격(F5)을 가지고 있는 사람",
                "label_en": "Adult under Civil Act with permanent residence (F5)"
            }
        ]
    },
    "simplified": {
        "label": "간이귀화",
        "label_en": "Simplified Naturalization",
        "requirement": "※ 국내 3년 이상 체류",
        "color": "#10b981",
        "sub_options": [
            {
                "value": "simplified_parent_korean",
                "label": "부 또는 모가 대한민국의 국민이었던 사람",
                "label_en": "Person whose parent was a Korean national"
            },
            {
                "value": "simplified_born_in_korea",
                "label": "대한민국에서 출생한 사람으로서 부 또는 모가 대한민국에서 출생한 사람",
                "label_en": "Person born in Korea whose parent was also born in Korea"
            },
            {
                "value": "simplified_adopted",
                "label": "대한민국 국민의 양자(養子)로서 입양 당시 대한민국의 「민법」상 성년이었던 사람",
                "label_en": "Adult adoptee of Korean national at time of adoption"
            }
        ]
    },
    "marriage": {
        "label": "혼인귀화",
        "label_en": "Marriage Naturalization",
        "requirement": "※ 한국인과의 혼인에 한함",
        "color": "#ec4899",
        "sub_options": [
            {
                "value": "marriage_2years",
                "label": "배우자와 혼인한 상태로 대한민국에 2년 이상 거주한 사람",
                "label_en": "Person married and residing in Korea for 2+ years"
            },
            {
                "value": "marriage_3years_1year",
                "label": "배우자와 혼인한 후 3년이 지나고 혼인한 상태로 대한민국에 1년 이상 거주한 사람",
                "label_en": "Person married 3+ years and residing in Korea for 1+ year"
            },
            {
                "value": "marriage_spouse_unavailable",
                "label": "배우자의 사망ㆍ실종 그 밖에 자신에게 책임이 없는 사유로 혼인생활 유지가 불가한 사람",
                "label_en": "Person unable to maintain marriage due to spouse's death/disappearance"
            },
            {
                "value": "marriage_raising_child",
                "label": "배우자와의 혼인에 따라 출생한 미성년의 자녀를 양육하고 있거나 양육할 사람",
                "label_en": "Person raising minor child from the marriage"
            }
        ]
    },
    "special": {
        "label": "특별귀화",
        "label_en": "Special Naturalization",
        "requirement": "특별 귀화",
        "color": "#f59e0b",
        "sub_options": [
            {
                "value": "special_minor_adoptee",
                "label": "부 또는 모가 대한민국의 국민인 사람, 입양 당시 「민법」상 미성년이었던 사람",
                "label_en": "Person whose parent is Korean, or minor adoptee at time of adoption"
            },
            {
                "value": "special_merit",
                "label": "대한민국에 특별한 공로가 있는 사람",
                "label_en": "Person with special merit to Korea",
                "has_sub_options": True,
                "sub_options": [
                    {"value": "special_merit_independence", "label": "독립유공자", "label_en": "Independence activist"},
                    {"value": "special_merit_national", "label": "국가유공자", "label_en": "National merit"},
                    {"value": "special_merit_national_interest", "label": "국익기여자", "label_en": "National interest contributor"}
                ]
            },
            {
                "value": "special_excellence",
                "label": "과학ㆍ경제ㆍ문화ㆍ체육 등 특정 분야에서 매우 우수한 능력을 보유한 사람",
                "label_en": "Person with exceptional ability in science, economy, culture, sports, etc."
            }
        ]
    }
}


"""
K-Stay Scenario Form Page - Redesigned (Part 1)
DOCUMENT_FIELD_MAPPING 및 기본 헬퍼 함수

수정사항:
- 결혼이민(C), 전문인력(E) 제거
- 의료관광(G) 추가
"""

# =============================================================================
# 서류-필드 매핑 정의 (시나리오별) - 결혼이민(C), 전문인력(E) 제거, 의료관광(G) 추가
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
                    "fields": ["employment_period", "employer_wage_hourly", "employer_weekday_total_hours", "employer_weekend_total_hours"]
                },
                {
                    "name": "요일별 근무시간",
                    "name_en": "Daily Work Hours",
                    "icon": "🕐",
                    "fields": [
                        "employer_working_hours_mon",
                        "employer_working_hours_tue",
                        "employer_working_hours_wed",
                        "employer_working_hours_thu",
                        "employer_working_hours_fri",
                        "employer_working_hours_sat",
                        "employer_working_hours_sun"
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
    # 결혼이민(C) 제거됨
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
                }
            ]
        },
        "불법체류취업방지서약서": {
            "icon": "📜",
            "description": "불법체류 및 취업 방지 서약",
            "description_en": "Illegal Stay and Work Prevention Pledge",
            "sections": [
                {
                    "name": "초청인 정보",
                    "name_en": "Inviter Information",
                    "icon": "👤",
                    "fields": ["inviter_name", "inviter_birth_date", "inviter_address", "inviter_phone"],
                    "description": "서비스 이용자(초청인)의 정보가 자동으로 입력됩니다."
                },
                {
                    "name": "피초청인 정보",
                    "name_en": "Invitee Information", 
                    "icon": "👥",
                    "fields": ["invitee_name", "invitee_birth_date", "invitee_address", "invitee_phone"],
                    "description": "초청받는 분의 정보를 입력해주세요."
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
    # 전문인력(E) 제거됨
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
                    "name": "귀화 유형",
                    "name_en": "Naturalization Type",
                    "icon": "📋",
                    "fields": ["naturalization_type", "naturalization_sub_type", "special_merit_type"],
                    "custom_renderer": "render_naturalization_type_selector"
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
    "G": {  # 의료 관광 (C-3-3/G-1-10) - 새로 추가
        "치료예정서약서": {
            "icon": "🏥",
            "description": "치료 예정 및 서약 내용",
            "description_en": "Treatment plan and pledge",
            "sections": [
                {
                    "name": "인적사항",
                    "name_en": "Personal Details",
                    "icon": "👤",
                    "fields": ["korea_address", "disease_name"]
                },
                {
                    "name": "보호자 정보",
                    "name_en": "Guardian Information",
                    "icon": "👨‍👩‍👧",
                    "fields": ["guardian_name", "guardian_phone", "guardian_email"]
                },
                {
                    "name": "병원 정보",
                    "name_en": "Hospital Information",
                    "icon": "🏨",
                    "fields": ["hospital_name", "hospital_address_contact"]
                }
            ]
        },
        "입국허가신청서": {
            "icon": "📄",
            "description": "입국 허가 신청서",
            "description_en": "Entry permit application",
            "sections": [
                {
                    "name": "신청인 정보",
                    "name_en": "Applicant Information",
                    "icon": "👤",
                    "fields": ["birth_place", "address", "address_in_korea", "occupation_and_title"]
                },
                {
                    "name": "여권 정보",
                    "name_en": "Passport Information",
                    "icon": "🛂",
                    "fields": ["passport_issue_date", "passport_expiration_date", "passport_place_of_issue"]
                },
                {
                    "name": "입국/체류 정보",
                    "name_en": "Entry and Stay Information",
                    "icon": "✈️",
                    "fields": ["purpose_of_entry", "desired_length_of_stay", "application_date"]
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
# ★★★ TABLE_ROWS 동적 테이블 입력 UI ★★★
# =============================================================================

def render_table_input_section(table_key: str, table_config: dict, section_title: str = None):
    """
    동적 테이블 입력 UI 렌더링
    
    Args:
        table_key: form_data에서 사용할 키 (예: "household_members")
        table_config: 테이블 설정 (columns, min_rows, max_rows 등)
        section_title: 섹션 제목 (옵션)
    """
    
    columns = table_config.get("columns", [])
    max_rows = table_config.get("max_rows", 10)
    min_rows = table_config.get("min_rows", 0)
    
    # 세션 상태 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    if table_key not in st.session_state.form_data:
        st.session_state.form_data[table_key] = [{}] if min_rows > 0 else []
    
    rows_data = st.session_state.form_data[table_key]
    
    # 최소 행 보장
    while len(rows_data) < min_rows:
        rows_data.append({})
    
    # 빈 배열이면 최소 1행 추가
    if not rows_data:
        rows_data = [{}]
        st.session_state.form_data[table_key] = rows_data
    
    # 섹션 제목
    if section_title:
        st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #fef3c7, #fde68a);
                padding: 12px 16px;
                border-radius: 8px;
                margin-bottom: 12px;
                border-left: 4px solid #f59e0b;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <span style="font-size: 1.2rem;">📋</span>
                <span style="font-weight: 600; color: #92400e;">{section_title}</span>
                <span style="
                    margin-left: auto;
                    background: #fbbf24;
                    color: #78350f;
                    font-size: 0.7rem;
                    padding: 2px 8px;
                    border-radius: 10px;
                ">{len(rows_data)}행</span>
            </div>
        """, unsafe_allow_html=True)
    
    # 테이블 헤더
    num_cols = len(columns)
    header_cols = st.columns([3] * num_cols + [1])
    
    for idx, col_config in enumerate(columns):
        required_mark = " *" if col_config.get("required", False) else ""
        header_cols[idx].markdown(f"**{col_config.get('label', '')}{required_mark}**")
    header_cols[-1].markdown("**삭제**")
    
    # 행 렌더링
    rows_to_delete = []
    
    for row_idx, row_data in enumerate(rows_data):
        row_cols = st.columns([3] * num_cols + [1])
        
        for col_idx, col_config in enumerate(columns):
            col_key = col_config.get("key")
            col_type = col_config.get("type", "text")
            col_options = col_config.get("options", [])
            widget_key = f"{table_key}_{row_idx}_{col_key}"
            current_value = row_data.get(col_key, "")
            
            with row_cols[col_idx]:
                if col_type == "select" and col_options:
                    options_list = [""] + col_options
                    idx_val = options_list.index(current_value) if current_value in options_list else 0
                    new_value = st.selectbox(
                        f"{col_key}_{row_idx}",
                        options_list,
                        index=idx_val,
                        key=widget_key,
                        label_visibility="collapsed"
                    )
                elif col_type == "date":
                    date_val = None
                    if current_value:
                        try:
                            date_val = datetime.strptime(current_value, "%Y-%m-%d").date()
                        except:
                            pass
                    new_value = st.date_input(
                        f"{col_key}_{row_idx}",
                        value=date_val,
                        key=widget_key,
                        label_visibility="collapsed"
                    )
                    new_value = new_value.strftime("%Y-%m-%d") if new_value else ""
                else:
                    new_value = st.text_input(
                        f"{col_key}_{row_idx}",
                        value=current_value,
                        key=widget_key,
                        label_visibility="collapsed"
                    )
                
                rows_data[row_idx][col_key] = new_value
        
        # 삭제 버튼
        with row_cols[-1]:
            if len(rows_data) > min_rows:
                if st.button("🗑️", key=f"del_{table_key}_{row_idx}", help="이 행 삭제"):
                    rows_to_delete.append(row_idx)
            else:
                st.write("")  # 빈 공간
    
    # 삭제 처리
    if rows_to_delete:
        for idx in sorted(rows_to_delete, reverse=True):
            rows_data.pop(idx)
        st.session_state.form_data[table_key] = rows_data
        st.rerun()
    
    # 행 추가 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if len(rows_data) < max_rows:
            if st.button(f"➕ 행 추가 ({len(rows_data)}/{max_rows})", key=f"add_{table_key}", use_container_width=True):
                rows_data.append({})
                st.session_state.form_data[table_key] = rows_data
                st.rerun()
        else:
            st.info(f"최대 {max_rows}개 행까지 입력 가능합니다.")
    
    st.markdown("---")


# pages/scenario_form.py

def render_phase2_table_rows_section(scenario_id: str, current_doc_name: str):  # <--- current_doc_name 인자 추가
    """
    Phase 2에서 TABLE_ROWS 섹션 렌더링
    현재 문서(current_doc_name)에 해당하는 테이블만 필터링하여 표시
    """
    
    # TABLE_ROWS 필드 가져오기
    table_fields = get_table_rows_fields(scenario_id)
    
    if not table_fields:
        return
    
    # 현재 문서에 해당하는 테이블이 있는지 확인 및 필터링
    relevant_tables = {}
    for key, config in table_fields.items():
        # 설정에서 target_doc을 가져옴 (없으면 모든 문서에 표시될 위험이 있으므로 체크 필요)
        target_doc = config.get('target_doc')
        
        # target_doc이 설정되어 있고, 현재 문서와 일치하는 경우에만 추가
        if target_doc and target_doc == current_doc_name:
            relevant_tables[key] = config
            
    if not relevant_tables:
        return  # 이 문서에 표시할 테이블이 없으면 종료

    # 테이블 섹션 헤더 (해당 문서에 테이블이 있을 때만 표시)
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 1px solid #f59e0b;
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        ">
            <div style="font-weight: 600; color: #92400e; margin-bottom: 4px;">
                📊 추가 정보 (테이블 형식)
            </div>
            <div style="font-size: 0.8rem; color: #a16207;">
                아래 테이블에 필요한 정보를 입력해주세요.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 필터링된 테이블만 렌더링
    for table_key, table_config in relevant_tables.items():
        render_table_input_section(
            table_key=table_key,
            table_config=table_config,
            section_title=table_config.get('label', table_key)
        )


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
        render_phase2_document_based(scenario)
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
# Phase 2: Document-Based Form (★ TABLE_ROWS 포함 ★)
# =============================================================================

def render_phase2_document_based(scenario):
    """Phase 2: 서류 기반 스텝 폼 + TABLE_ROWS 테이블"""
    
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
    
    # 1. 일반 필드 섹션 (for 문과 같은 레벨로 들여쓰기 주의)
    
    for section in sections:
        # 1. 일단 기본 카드(제목, 아이콘 등)를 그립니다.
        # 주의: fields에 있는 항목들이 텍스트 입력창으로 중복 표시될 수 있으니
        # 매핑에서 fields 리스트를 비워두거나 조정이 필요할 수 있습니다.
        render_section_card(section, all_field_defs, scenario_id)
        
        # 2. 커스텀 렌더러가 있다면 그 아래에 추가로 그립니다.
        custom_renderer = section.get('custom_renderer')
        if custom_renderer == "render_naturalization_type_selector":
            render_naturalization_type_selector()
    
    # 2. ★★★ TABLE_ROWS 테이블 렌더링 ★★★
    # (이 줄이 for문 바깥으로 나와야 하며, def render... 바로 아래 레벨이어야 합니다)
    render_phase2_table_rows_section(scenario_id, current_doc_name)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. 네비게이션 버튼
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # 버튼 변수 초기화
    btn_prev = False
    btn_save = False
    btn_next = False
    
    with col1:
        if current_idx > 0:
            btn_prev = st.button("← 이전 서류", use_container_width=True)
        else:
            btn_prev = st.button("← Phase 1로", use_container_width=True)
    
    with col2:
        btn_save = st.button("💾 임시 저장", use_container_width=True)
    
    with col3:
        if current_idx < total_docs - 1:
            btn_next = st.button("다음 서류 →", type="primary", use_container_width=True)
        else:
            btn_next = st.button("서술형 작성 →", type="primary", use_container_width=True)
    
    # 버튼 액션 처리
    if btn_prev:
        save_current_form_data(sections, all_field_defs)
        if current_idx > 0:
            st.session_state.current_doc_index = current_idx - 1
        else:
            st.session_state.form_step = 1
        st.rerun()
    
    if btn_save:
        save_current_form_data(sections, all_field_defs)
        st.success("✓ 임시 저장되었습니다!")
    
    if btn_next:
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
    """섹션 카드 렌더링 (영문 제목 제거)"""
    
    section_name = section.get('name', '')
    # section_name_en = section.get('name_en', '')  <-- 이 부분은 더 이상 사용하지 않습니다.
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
    
    # (이하 필드 배치 로직은 동일)
    valid_fields = [k for k in field_keys if k in all_field_defs]
    
    if len(valid_fields) > 0:
        col1, col2 = st.columns(2)
        for idx, field_key in enumerate(valid_fields):
            field_def = all_field_defs[field_key]
            col = col1 if idx % 2 == 0 else col2
            with col:
                render_styled_field(field_key, field_def)
    
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
    # if label_en and label_en != label:
    #     # 라벨이 너무 길면 줄임
    #     if len(label) > 50:
    #         display_label = label[:50] + "..."
    #     if len(label_en) > 50:
    #         label_en = label_en[:20] + "..."
    #     display_label = f"{display_label}"
    
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

    

def render_naturalization_type_selector():
    """
    귀화 유형 선택 UI 렌더링
    
    이 함수는 시나리오 F(국적 귀화)의 Phase 2에서 호출됩니다.
    """
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="font-size: 2rem;">🏛️</span>
                <div>
                    <h3 style="margin: 0; color: #92400e; font-size: 1.2rem;">귀화 유형 선택</h3>
                    <p style="margin: 4px 0 0 0; color: #a16207; font-size: 0.85rem;">
                        해당하는 귀화 유형과 세부 조건을 선택해주세요.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Step 1: 대분류 선택
    st.markdown("### 1️⃣ 귀화 유형 선택")
    
    selected_category = st.session_state.form_data.get('naturalization_type', None)
    
    cols = st.columns(4)
    
    for idx, (category_key, category) in enumerate(NATURALIZATION_TYPE_OPTIONS.items()):
        with cols[idx]:
            is_selected = selected_category == category_key
            
            # 카드 스타일
            bg_color = f"{category['color']}20" if is_selected else "#f8fafc"
            border_color = category['color'] if is_selected else "#e2e8f0"
            
            st.markdown(f"""
                <div style="
                    background: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.2s;
                    min-height: 120px;
                ">
                    <div style="font-weight: 700; color: {category['color']}; font-size: 1rem;">
                        {category['label']}
                    </div>
                    <div style="font-size: 0.7rem; color: #64748b; margin-top: 4px;">
                        {category['label_en']}
                    </div>
                    <div style="
                        font-size: 0.65rem; 
                        color: #94a3b8; 
                        margin-top: 8px;
                        background: white;
                        padding: 4px 8px;
                        border-radius: 6px;
                    ">
                        {category.get('requirement', '')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(
                "✓ 선택" if is_selected else "선택",
                key=f"nat_cat_{category_key}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.form_data['naturalization_type'] = category_key
                st.session_state.form_data['naturalization_sub_type'] = None  # 하위 선택 초기화
                st.session_state.form_data['special_merit_type'] = None
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step 2: 세부 조건 선택
    if selected_category:
        category_data = NATURALIZATION_TYPE_OPTIONS.get(selected_category, {})
        sub_options = category_data.get('sub_options', [])
        
        st.markdown(f"### 2️⃣ 세부 조건 선택 ({category_data['label']})")
        
        selected_sub = st.session_state.form_data.get('naturalization_sub_type', None)
        
        for sub_option in sub_options:
            value = sub_option['value']
            is_selected = selected_sub == value
            has_nested = sub_option.get('has_sub_options', False)
            
            # 라디오 버튼 스타일의 선택 카드
            border_color = category_data['color'] if is_selected else "#e2e8f0"
            bg_color = f"{category_data['color']}10" if is_selected else "white"
            
            col1, col2 = st.columns([0.05, 0.95])
            
            with col1:
                # 체크마크 또는 빈 원
                if is_selected:
                    st.markdown(f"""
                        <div style="
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            background: {category_data['color']};
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 14px;
                            margin-top: 10px;
                        ">✓</div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            border: 2px solid #d1d5db;
                            margin-top: 10px;
                        "></div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="
                        background: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 10px;
                        padding: 12px 16px;
                        margin-bottom: 8px;
                    ">
                        <div style="font-size: 0.9rem; color: #1e293b;">
                            {sub_option['label']}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">
                            {sub_option['label_en']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(
                    "선택",
                    key=f"nat_sub_{value}",
                    use_container_width=True
                ):
                    st.session_state.form_data['naturalization_sub_type'] = value
                    if not has_nested:
                        st.session_state.form_data['special_merit_type'] = None
                    st.rerun()
            
            # 중첩 옵션 (특별귀화 - 공로자)
            if is_selected and has_nested:
                nested_options = sub_option.get('sub_options', [])
                selected_nested = st.session_state.form_data.get('special_merit_type', None)
                
                st.markdown("""
                    <div style="margin-left: 40px; margin-bottom: 16px;">
                        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 8px;">
                            ▸ 공로 유형을 선택하세요:
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                nested_cols = st.columns(3)
                
                for n_idx, nested_opt in enumerate(nested_options):
                    with nested_cols[n_idx]:
                        n_value = nested_opt['value']
                        n_selected = selected_nested == n_value
                        
                        st.markdown(f"""
                            <div style="
                                background: {'#fef3c7' if n_selected else 'white'};
                                border: 2px solid {'#f59e0b' if n_selected else '#e2e8f0'};
                                border-radius: 8px;
                                padding: 10px;
                                text-align: center;
                                margin-left: 40px;
                            ">
                                <div style="font-size: 0.85rem; font-weight: 600; color: #1e293b;">
                                    {nested_opt['label']}
                                </div>
                                <div style="font-size: 0.7rem; color: #64748b;">
                                    {nested_opt['label_en']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(
                            "✓" if n_selected else "선택",
                            key=f"nat_nested_{n_value}",
                            use_container_width=True
                        ):
                            st.session_state.form_data['special_merit_type'] = n_value
                            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Step 3: 수반취득 (선택사항)
    st.markdown("### 3️⃣ 수반취득 (선택사항)")
    
    st.markdown("""
        <div style="
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 12px;
        ">
            <div style="font-size: 0.85rem; color: #0369a1;">
                ℹ️ 만 19세 미만의 자녀가 있는 경우, 신청인과 함께 국적 취득을 신청할 수 있습니다.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        accompanying = st.checkbox(
            "수반취득 신청",
            value=st.session_state.form_data.get('accompanying_acquisition', False),
            key="accompanying_checkbox"
        )
        st.session_state.form_data['accompanying_acquisition'] = accompanying
    
    with col2:
        if accompanying:
            count = st.number_input(
                "자녀 수",
                min_value=1,
                max_value=10,
                value=st.session_state.form_data.get('accompanying_children_count', 1),
                key="accompanying_count"
            )
            st.session_state.form_data['accompanying_children_count'] = count
    
    st.markdown("---")
    
    # 선택 요약
    render_naturalization_selection_summary()


def render_naturalization_selection_summary():
    """귀화 유형 선택 요약 표시"""
    
    form_data = st.session_state.get('form_data', {})
    
    nat_type = form_data.get('naturalization_type')
    nat_sub = form_data.get('naturalization_sub_type')
    merit_type = form_data.get('special_merit_type')
    accompanying = form_data.get('accompanying_acquisition', False)
    child_count = form_data.get('accompanying_children_count', 0)
    
    if not nat_type or not nat_sub:
        st.warning("⚠️ 귀화 유형과 세부 조건을 모두 선택해주세요.")
        return
    
    # 선택된 정보 가져오기
    category = NATURALIZATION_TYPE_OPTIONS.get(nat_type, {})
    sub_option = None
    for opt in category.get('sub_options', []):
        if opt['value'] == nat_sub:
            sub_option = opt
            break
    
    if not sub_option:
        return
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ecfdf5, #d1fae5);
            border: 2px solid #34d399;
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <div style="font-weight: 700; color: #065f46; font-size: 1rem; margin-bottom: 12px;">
                ✅ 선택 완료
            </div>
            <div style="display: grid; gap: 8px;">
                <div>
                    <span style="color: #6b7280; font-size: 0.8rem;">귀화 유형:</span>
                    <span style="color: #1e293b; font-weight: 600; margin-left: 8px;">
                        {category['label']}
                    </span>
                </div>
                <div>
                    <span style="color: #6b7280; font-size: 0.8rem;">세부 조건:</span>
                    <span style="color: #1e293b; font-weight: 500; margin-left: 8px; font-size: 0.9rem;">
                        {sub_option['label'][:60]}...
                    </span>
                </div>
    """, unsafe_allow_html=True)
    
    # 공로 유형 (해당 시)
    if merit_type:
        merit_label = ""
        for opt in sub_option.get('sub_options', []):
            if opt['value'] == merit_type:
                merit_label = opt['label']
                break
        
        st.markdown(f"""
                <div>
                    <span style="color: #6b7280; font-size: 0.8rem;">공로 유형:</span>
                    <span style="color: #f59e0b; font-weight: 600; margin-left: 8px;">
                        {merit_label}
                    </span>
                </div>
        """, unsafe_allow_html=True)
    
    # 수반취득 (해당 시)
    if accompanying and child_count > 0:
        st.markdown(f"""
                <div>
                    <span style="color: #6b7280; font-size: 0.8rem;">수반취득:</span>
                    <span style="color: #3b82f6; font-weight: 600; margin-left: 8px;">
                        만 19세 미만 자녀 {child_count}명
                    </span>
                </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)


# =============================================================================
# Phase 2 렌더링에 귀화 유형 선택 통합
# =============================================================================

def render_phase2_naturalization_section(scenario_id: str, current_doc_name: str):
    """
    Phase 2에서 귀화 유형 선택 섹션 렌더링
    
    이 함수는 시나리오 F의 '귀화허가신청서' 문서를 작성할 때 호출됩니다.
    """
    
    if scenario_id != "F":
        return
    
    if current_doc_name != "귀화허가신청서":
        return
    
    # 귀화 유형 선택 UI 렌더링
    render_naturalization_type_selector()


# =============================================================================
# DOCUMENT_FIELD_MAPPING["F"] 업데이트 - scenario_form.py용
# =============================================================================

NATURALIZATION_DOCUMENT_FIELD_MAPPING = {
    "귀화허가신청서": {
        "icon": "🏛️",
        "description": "귀화 허가 신청 기본 정보",
        "description_en": "Naturalization application basic info",
        "sections": [
            {
                "name": "신청인 인적사항",
                "name_en": "Applicant Personal Info",
                "icon": "👤",
                "fields": ["birth_place", "full_name_en", "intended_registered_domicile"]
            },
            {
                "name": "귀화 유형",
                "name_en": "Naturalization Type",
                "icon": "📋",
                "fields": ["naturalization_type", "naturalization_sub_type", "special_merit_type"],
                "custom_renderer": "render_naturalization_type_selector"
            },
            {
                "name": "수반취득",
                "name_en": "Accompanying Acquisition",
                "icon": "👨‍👩‍👧",
                "fields": ["accompanying_acquisition", "accompanying_children_count"]
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
                "fields": [
                    "guarantor_name", "guarantor_name_hanja", "guarantor_nationality",
                    "guarantor_gender", "guarantor_passport_or_birth", "guarantor_phone",
                    "guarantor_address", "guarantor_relationship", "guarantor_employer",
                    "guarantor_position", "guarantor_employer_address",
                    "guarantor_guarantee_period", "guarantor_signature_date", "guarantor_signature"
                ]
            }
        ]
    }
}


# =============================================================================
# LAYER2_VARIABLE_FIELDS["F"] 업데이트 - settings.py용
# =============================================================================

NATURALIZATION_LAYER2_FIELDS = {
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
                    "label_en": "Birth Place (Country and City)",
                    "type": "text",
                    "required": True,
                    "placeholder": "예: 중국 베이징"
                },
                {
                    "data_key": "full_name_en",
                    "label": "성명(영문)",
                    "label_en": "Full Name (English)",
                    "type": "text",
                    "required": True,
                    "placeholder": "HONG GILDONG"
                },
                {
                    "data_key": "intended_registered_domicile",
                    "label": "예정 등록기준지",
                    "label_en": "Intended Registered Domicile",
                    "type": "text",
                    "required": True,
                    "placeholder": "서울특별시 강남구"
                },
                # 귀화 유형 (계층적 선택)
                {
                    "data_key": "naturalization_type",
                    "label": "귀화 유형",
                    "label_en": "Naturalization Type",
                    "type": "hierarchical_select",
                    "required": True,
                    "options": ["general", "simplified", "marriage", "special"],
                    "option_labels": {
                        "general": "일반귀화 (국내 5년 이상 체류)",
                        "simplified": "간이귀화 (국내 3년 이상 체류)",
                        "marriage": "혼인귀화 (한국인과의 혼인에 한함)",
                        "special": "특별귀화"
                    }
                },
                {
                    "data_key": "naturalization_sub_type",
                    "label": "귀화 세부 조건",
                    "label_en": "Naturalization Sub-condition",
                    "type": "dependent_select",
                    "depends_on": "naturalization_type",
                    "required": True
                },
                {
                    "data_key": "special_merit_type",
                    "label": "공로 유형",
                    "label_en": "Merit Type",
                    "type": "dependent_select",
                    "depends_on": "naturalization_sub_type",
                    "condition_value": "special_merit",
                    "required": False,
                    "options": ["special_merit_independence", "special_merit_national", "special_merit_national_interest"],
                    "option_labels": {
                        "special_merit_independence": "독립유공자",
                        "special_merit_national": "국가유공자",
                        "special_merit_national_interest": "국익기여자"
                    }
                },
                {
                    "data_key": "accompanying_acquisition",
                    "label": "수반취득 여부",
                    "label_en": "Accompanying Acquisition",
                    "type": "checkbox",
                    "required": False,
                    "hint": "만 19세 미만의 자녀와 함께 국적 취득을 신청하는 경우 선택"
                },
                {
                    "data_key": "accompanying_children_count",
                    "label": "수반취득 자녀 수",
                    "label_en": "Number of Accompanying Children",
                    "type": "number",
                    "min_value": 0,
                    "max_value": 10,
                    "depends_on": "accompanying_acquisition",
                    "required": False
                }
            ]
        },
        {
            "target": "other_guarantor",
            "group_name": "신원보증인",
            "group_name_en": "Guarantor",
            "fields": [
                {"data_key": "guarantor_name", "label": "성명", "label_en": "Guarantor Name", "type": "text", "required": True},
                {"data_key": "guarantor_name_hanja", "label": "한자 성명", "label_en": "Name in Chinese", "type": "text", "required": False},
                {"data_key": "guarantor_nationality", "label": "국적", "label_en": "Nationality", "type": "text", "required": True},
                {"data_key": "guarantor_gender", "label": "성별", "label_en": "Gender", "type": "select", "options": ["Male", "Female"], "required": True},
                {"data_key": "guarantor_passport_or_birth", "label": "여권번호 또는 생년월일", "label_en": "Passport No. or DOB", "type": "text", "required": True},
                {"data_key": "guarantor_phone", "label": "전화번호", "label_en": "Phone", "type": "text", "required": True},
                {"data_key": "guarantor_address", "label": "주소", "label_en": "Address", "type": "text", "required": True},
                {"data_key": "guarantor_relationship", "label": "피보증인과의 관계", "label_en": "Relationship", "type": "text", "required": True},
                {"data_key": "guarantor_employer", "label": "근무처", "label_en": "Employer", "type": "text", "required": False},
                {"data_key": "guarantor_position", "label": "직위", "label_en": "Position", "type": "text", "required": False},
                {"data_key": "guarantor_employer_address", "label": "근무처 주소", "label_en": "Employer Address", "type": "text", "required": False},
                {"data_key": "guarantor_guarantee_period", "label": "보증기간", "label_en": "Guarantee Period", "type": "text", "required": True, "placeholder": "예: 4년"},
                {"data_key": "guarantor_signature_date", "label": "서명일", "label_en": "Signature Date", "type": "date", "required": True},
                {"data_key": "guarantor_signature", "label": "서명", "label_en": "Signature", "type": "text", "required": True}
            ]
        }
    ]
}