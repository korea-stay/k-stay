"""
K-Stay Document Service
Word 문서 생성 및 매핑
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import io
import zipfile
import os
import json

# python-docx (실제 배포 시 활성화)
# from docx import Document
# from docx.shared import Pt, Inches, Cm
# from docx.enum.text import WD_ALIGN_PARAGRAPH


class DocumentService:
    """문서 서비스 클래스"""
    
    def __init__(self):
        """초기화"""
        self.templates_dir = "templates"
    
    def parse_document_structure(self, template_path: str) -> Dict:
        """Word 템플릿의 구조를 파싱"""
        try:
            # 개발용 목업
            return {
                "paragraphs": [
                    {"index": 0, "text": "통합신청서", "style": "Title"}
                ],
                "tables": [
                    {
                        "index": 0,
                        "rows": [
                            [{"cell_index": 0, "text": "성명"}, {"cell_index": 1, "text": ""}],
                            [{"cell_index": 0, "text": "생년월일"}, {"cell_index": 1, "text": ""}]
                        ]
                    }
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_mapping_plan(self, structure: Dict, user_data: Dict) -> List[Dict]:
        """AI 기반 문서 매핑 계획 생성"""
        mappings = []
        
        field_mapping = {
            "surname": ["성", "Surname"],
            "given_name": ["이름", "Given Name"],
            "birth_date": ["생년월일", "Date of Birth"],
            "gender": ["성별", "Gender"],
            "nationality": ["국적", "Nationality"],
            "passport_no": ["여권번호", "Passport No"],
            "alien_registration_no": ["외국인등록번호", "Alien Registration"],
            "korea_address": ["주소", "Address"],
            "korea_phone": ["전화번호", "Phone"],
            "email": ["이메일", "Email"]
        }
        
        for table in structure.get("tables", []):
            for row_idx, row in enumerate(table.get("rows", [])):
                if len(row) >= 2:
                    label_text = row[0].get("text", "").strip()
                    for data_key, label_variants in field_mapping.items():
                        if any(v in label_text for v in label_variants):
                            if data_key in user_data and user_data[data_key]:
                                mappings.append({
                                    "target_type": "table",
                                    "table_index": table["index"],
                                    "row": row_idx,
                                    "cell": 1,
                                    "value": str(user_data[data_key]),
                                    "mode": "REPLACE"
                                })
        
        return mappings
    
    def apply_mappings(self, template_path: str, mappings: List[Dict]) -> bytes:
        """매핑을 적용하여 문서 생성"""
        try:
            # 실제 배포 시 python-docx 사용
            # 개발용 목업: 빈 바이트 반환
            return self._create_mock_document(mappings)
        except Exception as e:
            st.error(f"문서 생성 오류: {str(e)}")
            return b""
    
    def _create_mock_document(self, mappings: List[Dict]) -> bytes:
        """개발용 목업 문서 생성"""
        content = "K-Stay Generated Document\n"
        content += "=" * 40 + "\n\n"
        
        for mapping in mappings:
            content += f"[{mapping.get('target_type', 'field')}] "
            content += f"{mapping.get('value', 'N/A')}\n"
        
        content += "\n" + "=" * 40
        content += "\nGenerated at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return content.encode('utf-8')
    
    def generate_document(self, doc_name: str, user_data: Dict, 
                         form_data: Dict, narrative_data: Dict) -> bytes:
        """
        단일 문서 생성
        
        Args:
            doc_name: 문서 이름
            user_data: 사용자 기본 정보
            form_data: 시나리오별 폼 데이터
            narrative_data: AI 검토된 사연 데이터
            
        Returns:
            생성된 문서 바이트
        """
        from config.settings import DOCUMENT_TEMPLATES
        
        template_file = DOCUMENT_TEMPLATES.get(doc_name)
        if not template_file:
            return self._create_fallback_document(doc_name, user_data, form_data, narrative_data)
        
        template_path = os.path.join(self.templates_dir, template_file)
        
        combined_data = {**user_data, **form_data, **narrative_data}
        
        structure = self.parse_document_structure(template_path)
        mappings = self.create_mapping_plan(structure, combined_data)
        
        return self.apply_mappings(template_path, mappings)
    
    def _create_fallback_document(self, doc_name: str, user_data: Dict,
                                  form_data: Dict, narrative_data: Dict) -> bytes:
        """템플릿이 없을 경우 기본 문서 생성"""
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"  {doc_name}")
        lines.append(f"{'='*60}")
        lines.append("")
        
        lines.append("[신청인 정보]")
        lines.append(f"  성명: {user_data.get('surname', '')} {user_data.get('given_name', '')}")
        lines.append(f"  생년월일: {user_data.get('birth_date', '')}")
        lines.append(f"  국적: {user_data.get('nationality', '')}")
        lines.append(f"  여권번호: {user_data.get('passport_no', '')}")
        lines.append(f"  외국인등록번호: {user_data.get('alien_registration_no', '미소지')}")
        lines.append(f"  한국 주소: {user_data.get('korea_address', '')}")
        lines.append(f"  연락처: {user_data.get('korea_phone', '')}")
        lines.append(f"  이메일: {user_data.get('email', '')}")
        lines.append("")
        
        if form_data:
            lines.append("[시나리오별 정보]")
            for key, value in form_data.items():
                if value:
                    label = key.replace('_', ' ').title()
                    lines.append(f"  {label}: {value}")
            lines.append("")
        
        if narrative_data:
            lines.append("[사연 내용]")
            for key, value in narrative_data.items():
                if value:
                    lines.append(f"  {value}")
            lines.append("")
        
        lines.append(f"{'='*60}")
        lines.append(f"  생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}")
        lines.append(f"  K-Stay - Korea Stay Assistant")
        lines.append(f"{'='*60}")
        
        return "\n".join(lines).encode('utf-8')
    
    def generate_full_package(self, scenario_id: str, user_data: Dict,
                             form_data: Dict, narrative_data: Dict) -> bytes:
        """
        시나리오별 전체 문서 패키지 생성 (ZIP)
        
        Args:
            scenario_id: 시나리오 ID
            user_data: 사용자 기본 정보
            form_data: 시나리오별 폼 데이터
            narrative_data: AI 검토된 사연 데이터
            
        Returns:
            ZIP 파일 바이트
        """
        from config.settings import SCENARIOS
        
        scenario = SCENARIOS.get(scenario_id)
        if not scenario:
            st.error("유효하지 않은 시나리오입니다.")
            return b""
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc_name in scenario.required_docs:
                try:
                    doc_bytes = self.generate_document(
                        doc_name, user_data, form_data, narrative_data
                    )
                    
                    safe_name = doc_name.replace(' ', '_').replace('/', '_')
                    filename = f"{safe_name}.txt"
                    
                    zip_file.writestr(filename, doc_bytes)
                    
                except Exception as e:
                    error_content = f"문서 생성 오류: {str(e)}"
                    zip_file.writestr(f"ERROR_{doc_name}.txt", error_content.encode('utf-8'))
            
            readme_content = self._create_readme(scenario, datetime.now())
            zip_file.writestr("README.txt", readme_content.encode('utf-8'))
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _create_readme(self, scenario, generated_at: datetime) -> str:
        """README 파일 생성"""
        lines = [
            "=" * 60,
            "K-Stay Document Package",
            "=" * 60,
            "",
            f"시나리오: {scenario.name} ({scenario.visa_type})",
            f"생성일시: {generated_at.strftime('%Y년 %m월 %d일 %H:%M:%S')}",
            "",
            "포함된 문서:",
            "-" * 40,
        ]
        
        for i, doc in enumerate(scenario.required_docs, 1):
            lines.append(f"  {i}. {doc}")
        
        lines.extend([
            "",
            "-" * 40,
            "",
            "주의사항:",
            "  1. 본 문서는 AI가 생성한 초안입니다.",
            "  2. 제출 전 반드시 내용을 확인하세요.",
            "  3. 최신 요건은 하이코리아(www.hikorea.go.kr)에서 확인하세요.",
            "  4. 문의: 출입국외국인청 1345",
            "",
            "=" * 60,
            "Powered by K-Stay",
            "=" * 60,
        ])
        
        return "\n".join(lines)


class DocumentPreviewService:
    """문서 미리보기 서비스"""
    
    @staticmethod
    def preview_document(doc_bytes: bytes, doc_name: str):
        """문서 미리보기 렌더링"""
        try:
            content = doc_bytes.decode('utf-8')
            
            st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(201,162,39,0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9rem;
                    white-space: pre-wrap;
                    max-height: 500px;
                    overflow-y: auto;
                    color: #e0e0e0;
                ">
{content}
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"미리보기 오류: {str(e)}")
    
    @staticmethod
    def render_download_section(zip_bytes: bytes, scenario_name: str):
        """다운로드 섹션 렌더링"""
        
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(201,162,39,0.1) 0%, rgba(201,162,39,0.05) 100%);
                border: 2px solid #C9A227;
                border-radius: 20px;
                padding: 3rem;
                text-align: center;
                margin: 2rem 0;
            ">
                <h2 style="color: #C9A227; margin-bottom: 1rem;">
                    📦 문서 패키지 준비 완료!
                </h2>
                <p style="color: #a0aec0; margin-bottom: 2rem;">
                    모든 문서가 성공적으로 생성되었습니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"KStay_{scenario_name}_{timestamp}.zip"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 ZIP 패키지 다운로드",
                data=zip_bytes,
                file_name=filename,
                mime="application/zip",
                use_container_width=True
            )
