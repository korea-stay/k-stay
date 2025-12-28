"""
K-Stay AI Service
OpenAI 기반 AI 기능 처리
"""

import streamlit as st
from typing import Optional, Dict, List, Tuple
import json

# OpenAI 클라이언트 (실제 배포 시 활성화)
# from openai import OpenAI
# from config.settings import OPENAI_API_KEY


class AIService:
    """AI 서비스 클래스"""
    
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        # 실제 배포 시 아래 주석 해제
        # self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4o"  # 또는 "gpt-4o-mini"
    
    def validate_narrative(self, narrative: str, validation_prompt: str, scenario_context: Dict) -> Dict:
        """
        사연 내용 검증 및 피드백
        
        Args:
            narrative: 사용자가 작성한 사연
            validation_prompt: 시나리오별 검증 프롬프트
            scenario_context: 시나리오 컨텍스트 정보
            
        Returns:
            검증 결과 딕셔너리
        """
        try:
            # =================================================================
            # 실제 OpenAI 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            system_prompt = f'''
            {validation_prompt}
            
            응답 형식 (JSON):
            {{
                "is_valid": true/false,
                "score": 1-10,
                "issues": ["문제점1", "문제점2"],
                "suggestions": ["개선점1", "개선점2"],
                "improved_version": "개선된 버전 (문제가 있을 경우)"
            }}
            '''
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"다음 내용을 검토해주세요:\n\n{narrative}"}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            # 간단한 규칙 기반 검증
            issues = []
            suggestions = []
            score = 8
            
            if len(narrative) < 100:
                issues.append("내용이 너무 짧습니다.")
                suggestions.append("최소 200자 이상 작성해주세요.")
                score -= 2
            
            if "취업 확정" in narrative or "내정" in narrative:
                issues.append("'취업 확정', '내정' 등의 표현은 D-10 비자에 부적합합니다.")
                suggestions.append("'구직 활동 계획'으로 수정하세요.")
                score -= 3
            
            if "위장 결혼" in narrative or "돈을 받고" in narrative:
                issues.append("위장결혼을 암시하는 표현이 감지되었습니다.")
                suggestions.append("진정한 교제 과정을 설명하세요.")
                score -= 5
            
            return {
                "is_valid": len(issues) == 0,
                "score": max(1, score),
                "issues": issues,
                "suggestions": suggestions,
                "improved_version": None if len(issues) == 0 else "AI가 개선된 버전을 제안할 수 있습니다."
            }
            
        except Exception as e:
            return {
                "is_valid": False,
                "score": 0,
                "issues": [f"검증 중 오류 발생: {str(e)}"],
                "suggestions": [],
                "improved_version": None
            }
    
    def generate_narrative(self, generation_prompt: str, user_data: Dict) -> str:
        """
        사연 내용 자동 생성
        
        Args:
            generation_prompt: 생성 프롬프트 템플릿
            user_data: 사용자 입력 데이터
            
        Returns:
            생성된 사연 텍스트
        """
        try:
            # 프롬프트에 사용자 데이터 삽입
            formatted_prompt = generation_prompt.format(**user_data)
            
            # =================================================================
            # 실제 OpenAI 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            system_prompt = '''
            당신은 한국 출입국관리사무소에 제출할 서류를 작성하는 전문가입니다.
            다음 원칙을 지켜주세요:
            1. 진정성 있고 설득력 있게 작성
            2. 구체적인 날짜, 장소, 에피소드 포함
            3. 행정적으로 적합한 표현 사용
            4. 한국어 존댓말 사용
            '''
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": formatted_prompt}
                ],
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            return f"""
[AI 생성 예시]

안녕하십니까. 저는 {user_data.get('nationality', '외국')} 국적의 {user_data.get('given_name', '신청인')}입니다.

본 서류를 통해 제 상황과 계획을 말씀드리고자 합니다.

{user_data.get('narrative_content', '(상세 내용이 여기에 생성됩니다.)')}

감사합니다.

---
※ 이것은 AI가 생성한 초안입니다. 실제 제출 전 반드시 검토하세요.
            """
            
        except Exception as e:
            return f"생성 중 오류가 발생했습니다: {str(e)}"
    
    def chat_response(self, user_message: str, chat_history: List[Dict], rag_context: str = "") -> str:
        """
        AI 채팅 응답 생성
        
        Args:
            user_message: 사용자 메시지
            chat_history: 이전 대화 기록
            rag_context: RAG로 검색된 컨텍스트
            
        Returns:
            AI 응답 텍스트
        """
        try:
            # =================================================================
            # 실제 OpenAI 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            system_prompt = f'''
            당신은 K-Stay의 AI 상담사입니다.
            외국인의 한국 체류, 비자, 출입국 관련 질문에 답변합니다.
            
            참고 자료:
            {rag_context}
            
            원칙:
            1. 정확하고 최신 정보 제공
            2. 불확실한 경우 하이코리아 확인 권장
            3. 친절하고 이해하기 쉬운 설명
            4. 필요시 영어 병행 사용
            '''
            
            messages = [{"role": "system", "content": system_prompt}]
            
            # 이전 대화 기록 추가
            for msg in chat_history[-10:]:  # 최근 10개 대화만
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            """
            # =================================================================
            # 개발용 목업 코드
            # =================================================================
            # 간단한 키워드 기반 응답
            user_lower = user_message.lower()
            
            if "d-10" in user_lower or "구직" in user_lower:
                return """
D-10 비자 (구직 비자)에 대해 안내드립니다.

📋 **자격 요건**
- 학사 이상 학위 소지자
- 한국 내 대학 졸업자 또는 해외 대학 졸업 후 한국어 능력 보유자

📝 **필요 서류**
1. 통합신청서
2. 구직활동계획서
3. 여권 사본
4. 졸업증명서
5. 성적증명서

⏰ **체류 기간**
- 최대 6개월 (1회 연장 가능, 총 1년)

더 궁금한 점이 있으시면 언제든 물어보세요! 😊
                """
            
            elif "시간제" in user_lower or "아르바이트" in user_lower:
                return """
시간제 취업 (아르바이트)에 대해 안내드립니다.

📋 **허가 조건**
- D-2 (유학), D-4 (연수) 비자 소지자
- 입국 후 6개월 경과
- 직전 학기 출석률 90% 이상

⏰ **근무 시간 제한**
- 학기 중: 주 20시간 이내
- 방학 중: 무제한

🚫 **금지 업종**
- 유흥업소, 사행성 업소
- 단순 노무 (제조업 생산직 등)

필요한 서류를 K-Stay에서 자동으로 생성해드릴 수 있습니다!
                """
            
            elif "f-6" in user_lower or "결혼" in user_lower:
                return """
F-6 결혼이민 비자에 대해 안내드립니다.

💍 **자격 요건**
- 한국인과 법적 혼인 상태
- 기본 한국어 소통 능력 또는 결혼이민자 프로그램 이수

📝 **주요 서류**
1. 통합신청서
2. 결혼배경 진술서 (매우 중요!)
3. 배우자 초청장
4. 혼인관계증명서
5. 소득증명 서류

💡 **Tip**
결혼배경 진술서는 진정성이 매우 중요합니다.
K-Stay에서 AI가 도와드릴 수 있습니다!
                """
            
            else:
                return f"""
안녕하세요! K-Stay AI 상담사입니다. 😊

"{user_message}"에 대해 답변드립니다.

출입국 관련 문의는 다음 주제들을 다룹니다:
- 비자 종류 및 요건 (D-10, F-6, E-7 등)
- 시간제 취업 허가
- 체류자격 변경/연장
- 필요 서류 안내

구체적인 질문을 해주시면 더 정확한 안내가 가능합니다!

📞 긴급 문의: 하이코리아 1345
🌐 공식 사이트: www.hikorea.go.kr
                """
            
        except Exception as e:
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    def validate_and_coach(self, user_message: str, scenario, form_data: dict) -> str:
        """
        Phase 3: AI Validator - 법적/행정적 리스크 검토 및 코칭
        
        Args:
            user_message: 사용자가 작성한 사연 내용
            scenario: 현재 시나리오 객체
            form_data: Phase 2에서 입력된 데이터
            
        Returns:
            AI 검토 결과 및 코칭 메시지
        """
        # 위험 표현 감지 규칙
        danger_patterns = {
            "A": {  # D-10 구직
                "words": ["취업 확정", "내정", "계약 완료", "채용 확정", "이미 취업"],
                "warning": "D-10 비자는 '구직 활동' 목적입니다. 이미 취업이 확정된 것처럼 보이면 거절될 수 있습니다."
            },
            "B": {  # 시간제 취업
                "words": ["풀타임", "40시간", "주 40", "전일제"],
                "warning": "학기 중 주 20시간 초과 근무는 불법입니다."
            },
            "C": {  # F-6 결혼이민
                "words": ["돈을 받고", "위장", "계약 결혼", "돈을 벌기 위해", "비자 때문에"],
                "warning": "위장결혼을 암시하는 표현은 심각한 문제입니다. 진정한 사랑과 교제 과정을 설명해야 합니다."
            },
            "D": {  # F-1-5 가족초청
                "words": ["취업하러", "일하러", "돈 벌러", "노동"],
                "warning": "방문 목적으로 초청하면서 취업 의도를 암시하면 불법체류 의심을 받습니다."
            },
            "E": {  # E-7 전문인력
                "words": ["단순 노무", "청소", "설거지", "포장", "단순 작업"],
                "warning": "E-7은 전문인력 비자입니다. 단순 노무 업무로 보이면 거절됩니다."
            },
            "F": {  # 귀화
                "words": ["한국이 싫", "빨리 떠나", "다른 나라로"],
                "warning": "한국에 대한 부정적 표현은 귀화 심사에 불리합니다."
            }
        }
        
        scenario_id = scenario.id if hasattr(scenario, 'id') else str(scenario)
        patterns = danger_patterns.get(scenario_id, {"words": [], "warning": ""})
        
        # 위험 표현 검사
        found_dangers = []
        for word in patterns["words"]:
            if word in user_message:
                found_dangers.append(word)
        
        if found_dangers:
            danger_list = ", ".join([f'**"{w}"**' for w in found_dangers])
            return f"""⚠️ **AI Warning - 위험 표현 감지**

작성하신 내용에서 다음 표현이 감지되었습니다:
{danger_list}

**🚨 문제점:**
{patterns["warning"]}

**💡 수정 제안:**
- 해당 표현을 삭제하거나 수정해주세요
- 더 중립적이고 긍정적인 표현을 사용하세요
- 구체적인 계획과 진정성을 강조해주세요

수정된 내용을 다시 입력해주시겠어요?"""
        
        # 내용 길이 검사
        if len(user_message) < 50:
            return """📝 내용이 조금 짧습니다.

심사관이 납득할 수 있도록 더 구체적으로 작성해주세요.

**추가하면 좋을 내용:**
- 구체적인 날짜나 기간
- 실제 경험이나 에피소드  
- 목표나 계획의 세부 사항
- 한국에서의 활동 계획

더 자세히 적어주시겠어요?"""
        
        # 긍정적인 피드백
        import random
        positive_responses = [
            f"""✅ 좋습니다!

작성하신 내용이 잘 정리되어 있습니다. 

**AI 검토 결과:**
- 문맥 적합성 ✓
- 구체성 ✓  
- 진정성 ✓

추가로 보완하고 싶은 내용이 있으신가요? 
없으시면 **'작성 완료 → 문서 생성'** 버튼을 눌러주세요.""",
            
            f"""✅ 잘 작성하셨습니다!

**AI 분석 결과:**
논리적이고 설득력 있는 내용입니다.

혹시 다음 내용도 추가해보시겠어요?
- 앞으로의 구체적인 계획
- 한국 사회에 기여하고 싶은 점

추가할 내용이 없으시면 **'작성 완료'**를 눌러주세요.""",
            
            f"""✅ 검토 완료!

작성하신 내용에서 문제가 되는 표현이 발견되지 않았습니다.

**확인된 항목:**
- ❌ 위험 표현 없음
- ✓ 적절한 분량
- ✓ 맥락에 맞는 내용

더 추가하실 내용이 있으시면 계속 작성해주세요.
완료되셨다면 **'작성 완료 → 문서 생성'** 버튼을 눌러주세요!"""
        ]
        
        return random.choice(positive_responses)


class RAGService:
    """RAG (Retrieval-Augmented Generation) 서비스"""
    
    def __init__(self):
        """RAG 초기화"""
        # 실제 배포 시: Vector DB 연결
        # self.vector_store = None
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        """지식 베이스 로드"""
        # =================================================================
        # 실제 배포 시: Vector DB에서 로드 또는 파일에서 로드
        # =================================================================
        # 개발용 샘플 지식 베이스
        return {
            "visa_types": {
                "D-10": {
                    "name": "구직비자",
                    "duration": "6개월 (연장 가능)",
                    "requirements": ["학사 이상", "한국 대학 졸업 또는 한국어 능력"],
                    "documents": ["통합신청서", "구직활동계획서", "졸업증명서"]
                },
                "F-6": {
                    "name": "결혼이민",
                    "duration": "1~3년",
                    "requirements": ["한국인 배우자", "한국어 기본 소통"],
                    "documents": ["통합신청서", "결혼배경진술서", "혼인관계증명서"]
                },
                "E-7": {
                    "name": "특정활동",
                    "duration": "1~3년",
                    "requirements": ["전문인력", "고용계약"],
                    "documents": ["통합신청서", "고용계약서", "학력증명"]
                }
            },
            "common_rejections": [
                "서류 미비 또는 불충분",
                "구직계획의 구체성 부족",
                "소득 요건 미충족",
                "결혼의 진정성 의심"
            ],
            "tips": [
                "서류는 최소 2주 전 준비 시작",
                "번역 서류는 공증 필요",
                "접수 전 서류 점검표 확인"
            ]
        }
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """
        쿼리와 관련된 컨텍스트 검색
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 결과 수
            
        Returns:
            검색된 컨텍스트 텍스트
        """
        try:
            # =================================================================
            # 실제 Vector DB 연동 코드 (배포 시 활성화)
            # =================================================================
            """
            # Pinecone / FAISS / Weaviate 등 사용
            from sentence_transformers import SentenceTransformer
            
            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            query_embedding = model.encode(query)
            
            # Vector DB 검색
            results = self.vector_store.search(query_embedding, top_k=top_k)
            
            context = "\n\n".join([r.text for r in results])
            return context
            """
            # =================================================================
            # 개발용 목업 코드: 키워드 기반 검색
            # =================================================================
            context_parts = []
            query_lower = query.lower()
            
            # 비자 타입 관련 정보 검색
            for visa_code, visa_info in self.knowledge_base["visa_types"].items():
                if visa_code.lower() in query_lower or visa_info["name"] in query:
                    context_parts.append(f"""
[{visa_code} - {visa_info['name']}]
- 체류 기간: {visa_info['duration']}
- 요건: {', '.join(visa_info['requirements'])}
- 필요 서류: {', '.join(visa_info['documents'])}
                    """)
            
            # 일반 팁 추가
            if not context_parts:
                context_parts.append(f"""
[일반 안내]
- 주요 거절 사유: {', '.join(self.knowledge_base['common_rejections'][:2])}
- 팁: {self.knowledge_base['tips'][0]}
                """)
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"컨텍스트 검색 중 오류: {str(e)}"


class NarrativeValidator:
    """사연 검증 헬퍼 클래스"""
    
    @staticmethod
    def render_validation_result(result: Dict):
        """검증 결과 UI 렌더링"""
        
        if result["is_valid"]:
            st.success(f"✅ 검토 완료! 점수: {result['score']}/10")
        else:
            st.warning(f"⚠️ 수정이 필요합니다. 점수: {result['score']}/10")
        
        # 문제점 표시
        if result.get("issues"):
            st.markdown("### 🔍 발견된 문제")
            for issue in result["issues"]:
                st.markdown(f"- ❌ {issue}")
        
        # 개선점 표시
        if result.get("suggestions"):
            st.markdown("### 💡 개선 제안")
            for suggestion in result["suggestions"]:
                st.markdown(f"- 💡 {suggestion}")
        
        # 개선된 버전 제안
        if result.get("improved_version"):
            with st.expander("📝 AI 개선 버전 보기"):
                st.markdown(result["improved_version"])
                if st.button("이 버전 사용하기"):
                    return result["improved_version"]
        
        return None
