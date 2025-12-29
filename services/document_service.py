"""
K-Stay Document Service
Word 문서 생성 및 매핑 - DocumentProcessor 엔진 적용
(.docx 파일만 지원 - LibreOffice 불필요)
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import io
import zipfile
import os
import re
import tempfile

# python-docx
try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
    print("✅ python-docx 로드 성공")
except ImportError as e:
    DOCX_AVAILABLE = False
    print(f"⚠️ python-docx 미설치 - pip install python-docx 실행 필요")
    print(f"   오류 상세: {e}")
except Exception as e:
    DOCX_AVAILABLE = False
    print(f"⚠️ python-docx 로드 실패: {e}")


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
# DocumentProcessor 클래스
# =============================================================================

class DocumentProcessor:
    """
    문서 처리 엔진
    - 앵커 텍스트 기반 데이터 매핑
    - 다양한 전략 지원: BELOW_CELL, NEXT_CELL, CHECKBOX, SPLIT_CELLS, APPEND_TO_SAME_CELL
    """
    
    def __init__(self, data: Dict[str, Any]):
        """
        Args:
            data: Layer 1 + Layer 2 + Layer 3 통합 데이터
        """
        self.data = data
        self.logs = []
    
    def normalize_text(self, text: str) -> str:
        """텍스트 정규화 (공백 제거, 소문자)"""
        return re.sub(r'\s+', '', text).lower()
    
    def process_file(self, mapping_config: Dict, input_path: str, output_path: str) -> bool:
        """
        문서 파일 처리
        
        Args:
            mapping_config: 매핑 설정 (fields 포함)
            input_path: 입력 템플릿 경로 (.docx)
            output_path: 출력 파일 경로
            
        Returns:
            성공 여부
        """
        if not DOCX_AVAILABLE:
            self._log("❌ python-docx 미설치 - pip install python-docx 실행 필요")
            return False
        
        if not os.path.exists(input_path):
            self._log(f"❌ 파일을 찾을 수 없습니다: {input_path}")
            return False
        
        if not input_path.lower().endswith('.docx'):
            self._log(f"❌ .docx 파일만 지원합니다: {input_path}")
            return False
        
        try:
            doc = Document(input_path)
            self._log(f"🔄 [분석 시작] {os.path.basename(input_path)}")
            
            for field in mapping_config.get('fields', []):
                self._apply_field(doc, field)
            
            doc.save(output_path)
            self._log(f"✅ [저장 완료] {output_path}")
            return True
            
        except Exception as e:
            self._log(f"❌ 오류 발생: {e}")
            return False
    
    def _log(self, message: str):
        """로그 기록"""
        self.logs.append(message)
        print(message)
    
    def _apply_field(self, doc, field: Dict):
        """개별 필드 적용"""
        data_key = field['data_key']
        value = self.data.get(data_key, "")
        
        if not value:
            return
        
        # anchor_text 처리 (문자열 또는 리스트)
        anchors = field.get('anchor_text', [])
        if isinstance(anchors, str):
            anchors = [anchors]
        
        strategy = field.get('strategy', 'NEXT_CELL')
        target_index = field.get('index', 0)
        
        found_count = 0
        processed = False
        
        # 테이블 전체 순회
        for t_idx, table in enumerate(doc.tables):
            for r_idx, row in enumerate(table.rows):
                try:
                    row_cells = row.cells
                except:
                    continue
                
                for c_idx, cell in enumerate(row_cells):
                    cell_text_clean = self.normalize_text(cell.text)
                    
                    # 앵커 텍스트 매칭
                    if any(self.normalize_text(a) in cell_text_clean for a in anchors):
                        if found_count == target_index:
                            self._log(f"   🔎 [발견] '{anchors[0]}' (Table{t_idx}, R{r_idx}, C{c_idx})")
                            
                            # 전략 실행
                            self._execute_strategy(
                                strategy, table, r_idx, c_idx, 
                                value, field, cell, row_cells
                            )
                            processed = True
                            break
                        found_count += 1
                
                if processed:
                    break
            if processed:
                break
        
        if not processed:
            self._log(f"   ⚠️ [Skip] 앵커를 찾지 못함: {anchors}")
    
    def _execute_strategy(self, strategy: str, table, r_idx: int, c_idx: int, 
                         value: Any, field: Dict, current_cell, row_cells):
        """전략별 실행"""
        try:
            # -----------------------------------------------------------------
            # [전략 A] CHECKBOX - 체크박스 선택
            # -----------------------------------------------------------------
            if strategy == "CHECKBOX":
                value_map = field.get('value_map', GENDER_CHECKBOX_MAP)
                target_candidates = value_map.get(str(value), [str(value)])
                
                scan_targets = []
                
                # 1. 현재 칸 확인
                scan_targets.append(("현재칸", current_cell))
                
                # 2. 오른쪽으로 끝까지 스캔
                for i in range(c_idx + 1, len(row_cells)):
                    scan_targets.append((f"오른쪽+{i-c_idx}", row_cells[i]))
                
                # 3. 아래 줄도 확인
                if r_idx + 1 < len(table.rows):
                    try:
                        below_row_cells = table.rows[r_idx + 1].cells
                        start = max(0, c_idx - 1)
                        end = min(len(below_row_cells), c_idx + 3)
                        for k in range(start, end):
                            scan_targets.append((f"아래쪽(C{k})", below_row_cells[k]))
                    except:
                        pass
                
                checked_success = False
                
                for pos_name, cell in scan_targets:
                    original_text = cell.text
                    if not original_text.strip():
                        continue
                    
                    for target in target_candidates:
                        # 체크박스 패턴: [ ] 남, ( ) M, □ Male
                        pattern = fr"(\[\s*\]|□|☐|\(\s*\))(\s*)({re.escape(target)})"
                        match = re.search(pattern, original_text)
                        
                        if match:
                            # [V] 체크
                            new_text = re.sub(pattern, fr"[V]\2\3", original_text, count=1)
                            cell.text = new_text
                            self._log(f"      ✅ [성공] {pos_name}에서 '{target}' 체크박스 선택!")
                            checked_success = True
                            break
                    
                    if checked_success:
                        break
                
                if not checked_success:
                    self._log(f"      ⚠️ [실패] 체크박스를 찾지 못함: {target_candidates}")
            
            # -----------------------------------------------------------------
            # [전략 B] SPLIT_CELLS - 문자열 분할 (주민번호 등)
            # -----------------------------------------------------------------
            elif strategy == "SPLIT_CELLS":
                options = field.get('options', {})
                skip_chars = options.get('skip_chars', [])
                val_str = str(value)
                
                for char in skip_chars:
                    val_str = val_str.replace(char, "")
                
                candidates = []
                for i in range(c_idx + 1, len(row_cells)):
                    cell = row_cells[i]
                    if (cell._tc != current_cell._tc) and ("-" not in cell.text):
                        candidates.append(cell)
                
                self._log(f"      ℹ️ [분할] '{val_str}' -> {len(candidates)}칸에 입력")
                
                for i, char in enumerate(val_str):
                    if i < len(candidates):
                        candidates[i].text = char
                        for p in candidates[i].paragraphs:
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # -----------------------------------------------------------------
            # [전략 C] NEXT_CELL - 오른쪽 셀에 입력
            # -----------------------------------------------------------------
            elif strategy == "NEXT_CELL":
                for i in range(c_idx + 1, len(row_cells)):
                    cell = row_cells[i]
                    if cell._tc != current_cell._tc:
                        cell.text = str(value)
                        self._log(f"      ✅ [입력] 옆({i-c_idx}칸 뒤)에 '{value}' 입력")
                        return
            
            # -----------------------------------------------------------------
            # [전략 D] BELOW_CELL - 아래 셀에 입력
            # -----------------------------------------------------------------
            elif strategy == "BELOW_CELL":
                if r_idx + 1 < len(table.rows):
                    table.rows[r_idx + 1].cells[c_idx].text = str(value)
                    self._log(f"      ✅ [입력] 아래 칸에 '{value}' 입력")
            
            # -----------------------------------------------------------------
            # [전략 E] APPEND_TO_SAME_CELL - 같은 셀에 추가
            # -----------------------------------------------------------------
            elif strategy == "APPEND_TO_SAME_CELL":
                if str(value) not in current_cell.text:
                    current_cell.text += f"  {value}"
                    self._log(f"      ✅ [추가] 같은 칸에 '{value}' 덧붙임")
            
            # -----------------------------------------------------------------
            # [전략 F] INSERT_IMAGE - 이미지 삽입 (추후 구현)
            # -----------------------------------------------------------------
            elif strategy == "INSERT_IMAGE":
                self._log(f"      ℹ️ [이미지] 이미지 삽입 기능은 추후 구현 예정")
        
        except Exception as e:
            self._log(f"      ❌ 처리 중 에러: {e}")


# =============================================================================
# DocumentService 클래스
# =============================================================================

class DocumentService:
    """문서 서비스 클래스"""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        초기화
        
        Args:
            templates_dir: 템플릿 파일이 있는 디렉토리
        """
        self.templates_dir = templates_dir
        
        if DOCX_AVAILABLE:
            print("✅ python-docx 사용 가능 - .docx 파일 처리 지원")
        else:
            print("❌ python-docx 미설치 - pip install python-docx 실행 필요")
    
    def merge_all_data(self, user_data: Dict, form_data: Dict, narrative_data: Dict) -> Dict:
        """
        모든 레이어 데이터 병합
        
        Args:
            user_data: Layer 1 (Universal) - DB에서 로드
            form_data: Layer 2 (Variable) - 폼 입력
            narrative_data: Layer 3 (Narrative) - 서술형
            
        Returns:
            병합된 데이터
        """
        merged = {}
        
        # Layer 1: Universal (DB 데이터)
        if user_data:
            merged.update(user_data)
        
        # Layer 2: Variable (폼 데이터)
        if form_data:
            merged.update(form_data)
        
        # Layer 3: Narrative (서술형 데이터)
        if narrative_data:
            merged.update(narrative_data)
        
        # 파생 데이터 생성
        if merged.get('surname') and merged.get('given_name'):
            merged['full_name'] = f"{merged['surname']} {merged['given_name']}"
        
        # 생년월일 분리
        if merged.get('birth_date'):
            birth_str = str(merged['birth_date'])
            if '-' in birth_str:
                parts = birth_str.split('-')
                if len(parts) == 3:
                    merged['dob_year'] = parts[0]
                    merged['dob_month'] = parts[1]
                    merged['dob_day'] = parts[2]
        
        # 신청일 기본값
        if 'application_date' not in merged:
            merged['application_date'] = datetime.now().strftime('%Y.%m.%d')
        
        return merged
    
    def get_template_path(self, doc_name: str) -> Optional[str]:
        """
        문서명으로 템플릿 파일 경로 가져오기
        
        Args:
            doc_name: 문서명 (예: "구직활동계획서")
            
        Returns:
            템플릿 파일 전체 경로 또는 None
        """
        from config.settings import DOCUMENT_TEMPLATES
        
        template_file = DOCUMENT_TEMPLATES.get(doc_name)
        if not template_file:
            print(f"⚠️ 템플릿 매핑 없음: {doc_name}")
            return None
        
        template_path = os.path.join(self.templates_dir, template_file)
        
        if not os.path.exists(template_path):
            print(f"⚠️ 템플릿 파일 없음: {template_path}")
            return None
        
        return template_path
    
    def generate_document(self, doc_name: str, user_data: Dict, 
                         form_data: Dict, narrative_data: Dict) -> bytes:
        """
        단일 문서 생성
        
        Args:
            doc_name: 문서 이름
            user_data: Layer 1 데이터
            form_data: Layer 2 데이터
            narrative_data: Layer 3 데이터
            
        Returns:
            생성된 문서 바이트
        """
        from templates.mapping_guide import get_document_mapping
        
        # 데이터 병합
        merged_data = self.merge_all_data(user_data, form_data, narrative_data)
        
        # 템플릿 파일 경로
        template_path = self.get_template_path(doc_name)
        
        # python-docx가 없거나 템플릿이 없으면 폴백
        if not DOCX_AVAILABLE or not template_path:
            return self._create_fallback_document(doc_name, merged_data)
        
        # 매핑 설정 가져오기
        mapping_config = get_document_mapping(doc_name)
        
        if not mapping_config:
            print(f"ℹ️ 매핑 설정 없음: {doc_name} - 템플릿 원본 복사")
            # 매핑 없이 템플릿만 복사
            try:
                with open(template_path, 'rb') as f:
                    return f.read()
            except:
                return self._create_fallback_document(doc_name, merged_data)
        
        # DocumentProcessor로 처리
        try:
            processor = DocumentProcessor(merged_data)
            
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
                temp_output = tmp.name
            
            if processor.process_file(mapping_config, template_path, temp_output):
                with open(temp_output, 'rb') as f:
                    doc_bytes = f.read()
                
                # 임시 파일 삭제
                try:
                    os.remove(temp_output)
                except:
                    pass
                
                return doc_bytes
            else:
                return self._create_fallback_document(doc_name, merged_data)
                
        except Exception as e:
            print(f"❌ 문서 생성 오류: {str(e)}")
            return self._create_fallback_document(doc_name, merged_data)
    
    def _create_fallback_document(self, doc_name: str, data: Dict) -> bytes:
        """템플릿이 없을 경우 텍스트 기반 문서 생성"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"  {doc_name}")
        lines.append("=" * 60)
        lines.append("")
        
        # Layer 1: 신청인 정보
        lines.append("[신청인 정보 - Layer 1]")
        layer1_fields = ['surname', 'given_name', 'birth_date', 'gender', 
                        'nationality', 'passport_no', 'alien_registration_no',
                        'korea_address', 'korea_phone', 'email']
        for key in layer1_fields:
            if key in data and data[key]:
                label = key.replace('_', ' ').title()
                lines.append(f"  {label}: {data[key]}")
        lines.append("")
        
        # Layer 2: 시나리오별 정보
        lines.append("[시나리오별 정보 - Layer 2]")
        layer2_printed = False
        for key, value in data.items():
            if key not in layer1_fields and not key.startswith('plan_') and value:
                if key not in ['full_name', 'dob_year', 'dob_month', 'dob_day', 'application_date']:
                    label = key.replace('_', ' ').title()
                    lines.append(f"  {label}: {value}")
                    layer2_printed = True
        if not layer2_printed:
            lines.append("  (입력된 정보 없음)")
        lines.append("")
        
        # Layer 3: 서술형 내용
        lines.append("[서술형 내용 - Layer 3]")
        layer3_printed = False
        for key, value in data.items():
            if key.startswith('plan_') and value:
                label = key.replace('plan_month_', '').replace('_', ' ')
                lines.append(f"  {label}개월차: {value}")
                layer3_printed = True
        if not layer3_printed:
            lines.append("  (입력된 내용 없음)")
        lines.append("")
        
        lines.append("=" * 60)
        lines.append(f"  생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}")
        lines.append("  K-Stay - Korea Stay Assistant")
        lines.append("=" * 60)
        
        return "\n".join(lines).encode('utf-8')
    
    def generate_full_package(self, scenario_id: str, user_data: Dict,
                             form_data: Dict, narrative_data: Dict) -> bytes:
        """
        시나리오별 전체 문서 패키지 생성 (ZIP)
        
        Args:
            scenario_id: 시나리오 ID
            user_data: Layer 1 데이터
            form_data: Layer 2 데이터
            narrative_data: Layer 3 데이터
            
        Returns:
            ZIP 파일 바이트
        """
        from config.settings import SCENARIOS
        from templates.mapping_guide import get_scenario_documents
        
        scenario = SCENARIOS.get(scenario_id)
        if not scenario:
            st.error("유효하지 않은 시나리오입니다.")
            return b""
        
        # 시나리오별 필요 문서 목록
        required_docs = get_scenario_documents(scenario_id)
        if not required_docs:
            required_docs = scenario.required_docs
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc_name in required_docs:
                try:
                    doc_bytes = self.generate_document(
                        doc_name, user_data, form_data, narrative_data
                    )
                    
                    safe_name = doc_name.replace(' ', '_').replace('/', '_')
                    
                    # 확장자 결정 (DOCX 시그니처 확인: PK로 시작)
                    if len(doc_bytes) >= 4 and doc_bytes[:4] == b'PK\x03\x04':
                        filename = f"{safe_name}.docx"
                    else:
                        filename = f"{safe_name}.txt"
                    
                    zip_file.writestr(filename, doc_bytes)
                    print(f"📄 추가됨: {filename}")
                    
                except Exception as e:
                    error_content = f"문서 생성 오류: {str(e)}"
                    zip_file.writestr(f"ERROR_{doc_name}.txt", error_content.encode('utf-8'))
                    print(f"❌ 오류: {doc_name} - {str(e)}")
            
            # README 추가
            readme_content = self._create_readme(scenario, required_docs, datetime.now())
            zip_file.writestr("README.txt", readme_content.encode('utf-8'))
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _create_readme(self, scenario, docs: List[str], generated_at: datetime) -> str:
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
        
        for i, doc in enumerate(docs, 1):
            lines.append(f"  {i}. {doc}")
        
        lines.extend([
            "",
            "-" * 40,
            "",
            "데이터 레이어 구조:",
            "  - Layer 1 (Universal): 회원가입 시 입력된 불변 정보",
            "  - Layer 2 (Variable): 시나리오별 폼 입력 정보",
            "  - Layer 3 (Narrative): AI 검토된 서술형 정보",
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


# =============================================================================
# DocumentPreviewService 클래스
# =============================================================================

class DocumentPreviewService:
    """문서 미리보기 서비스"""
    
    @staticmethod
    def preview_document(doc_bytes: bytes, doc_name: str):
        """문서 미리보기 렌더링"""
        try:
            # 텍스트 파일인 경우
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
            except UnicodeDecodeError:
                # DOCX 파일인 경우
                st.info(f"📄 {doc_name} - Word 문서 파일입니다. 다운로드하여 확인하세요.")
                
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