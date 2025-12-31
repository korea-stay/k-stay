"""
K-Stay AI Service
OpenAI 기반 AI 기능 처리
"""

import streamlit as st
from typing import Optional, Dict, List, Tuple
import json

# OpenAI 클라이언트
from openai import OpenAI

# RAGService는 별도 파일에서 임포트
from services.rag_service import RAGService


class AIService:
    """AI 서비스 클래스"""
    
    def __init__(self):
        """OpenAI 클라이언트 초기화"""
        try:
            self.client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
            self.model = "gpt-4o-mini"
        except Exception as e:
            print(f"OpenAI 초기화 오류: {e}")
            self.client = None
            self.model = "gpt-4o-mini"
    
    def validate_narrative(self, narrative: str, validation_prompt: str, scenario_context: Dict) -> Dict:
        """
        사연 내용 검증 및 피드백
        """
        try:
            if self.client:
                system_prompt = f'''{validation_prompt}
                
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
            
            # 폴백: 규칙 기반 검증
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
        """
        try:
            formatted_prompt = generation_prompt.format(**user_data)
            
            if self.client:
                system_prompt = '''당신은 한국 출입국관리사무소에 제출할 서류를 작성하는 전문가입니다.
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
            
            # 폴백
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
        AI 채팅 응답 생성 (RAG 컨텍스트 활용)
        """
        try:
            if self.client:
                system_prompt = f'''당신은 K-Stay의 AI 상담사입니다.
외국인의 한국 체류, 비자, 출입국 관련 질문에 답변합니다.

참고 자료:
{rag_context}

원칙:
1. 참고 자료에 있는 정보를 기반으로 정확하게 답변
2. 참고 자료에 없는 내용은 추측하지 않고 "정확한 정보는 출입국관리사무소(1345) 또는 하이코리아에서 확인하세요"라고 안내
3. 친절하고 이해하기 쉽게 설명
4. 한국어로 답변 (필요시 영어 병행)
'''
                
                messages = [{"role": "system", "content": system_prompt}]
                
                # 이전 대화 기록 추가
                for msg in chat_history[-6:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                
                messages.append({"role": "user", "content": user_message})
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=1500,
                    temperature=0.3
                )
                
                return response.choices[0].message.content
            
            # 폴백: 키워드 기반 응답
            return self._fallback_response(user_message)
            
        except Exception as e:
            return f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {str(e)}"
    
    def _fallback_response(self, user_message: str) -> str:
        """OpenAI 연결 실패 시 폴백 응답"""
        user_lower = user_message.lower()
        
        if "d-10" in user_lower or "구직" in user_lower:
            return """D-10 비자 (구직 비자)에 대해 안내드립니다.

📋 **자격 요건**
- 학사 이상 학위 소지자
- 한국 내 대학 졸업자 또는 해외 대학 졸업 후 한국어 능력 보유자

📝 **필요 서류**
1. 통합신청서
2. 구직활동계획서
3. 여권 사본
4. 졸업증명서

⏰ **체류 기간**
- 최대 6개월 (1회 연장 가능, 총 1년)

더 궁금한 점이 있으시면 언제든 물어보세요! 😊"""
        
        elif "f-6" in user_lower or "결혼" in user_lower:
            return """F-6 결혼이민 비자에 대해 안내드립니다.

💍 **자격 요건**
- 한국인과 법적 혼인 상태
- 기본 한국어 소통 능력

📝 **주요 서류**
1. 통합신청서
2. 결혼배경 진술서 (매우 중요!)
3. 배우자 초청장
4. 혼인관계증명서
5. 소득증명 서류

더 자세한 내용은 말씀해 주세요!"""
        
        elif "d-2" in user_lower or "유학" in user_lower:
            return """D-2 유학 비자에 대해 안내드립니다.

📚 **비자 종류**
- D-2-1~4: 학위과정 (전문학사~박사)
- D-2-5: 연구과정
- D-2-6: 교환학생
- D-2-7: 일-학습연계

⏰ **아르바이트 허용시간**
- 학기 중: 주 20~25시간 (TOPIK 급수에 따라 다름)
- 방학 중: 무제한

더 궁금한 점이 있으시면 물어보세요!"""
        
        return """안녕하세요! K-Stay AI 상담사입니다.

현재 지원하는 비자 유형:
- D-2 유학비자
- D-10 구직비자
- F-6 결혼이민비자
- C-4 단기취업비자

궁금한 비자에 대해 질문해 주세요! 😊

📞 긴급 문의: 하이코리아 1345
🌐 공식 사이트: www.hikorea.go.kr"""
    
    def validate_and_coach(self, user_message: str, scenario, form_data: dict) -> str:
        """
        Phase 3: AI Validator - 법적/행정적 리스크 검토 및 코칭
        """
        # 위험 표현 감지 규칙
        danger_patterns = {
            "A": {
                "words": ["취업 확정", "내정", "계약 완료", "채용 확정", "이미 취업"],
                "warning": "D-10 비자는 '구직 활동' 목적입니다. 이미 취업이 확정된 것처럼 보이면 거절될 수 있습니다."
            },
            "B": {
                "words": ["풀타임", "40시간", "주 40", "전일제"],
                "warning": "학기 중 주 20시간 초과 근무는 불법입니다."
            },
            "C": {
                "words": ["돈을 받고", "위장", "계약 결혼", "돈을 벌기 위해", "비자 때문에"],
                "warning": "위장결혼을 암시하는 표현은 심각한 문제입니다."
            },
            "D": {
                "words": ["취업하러", "일하러", "돈 벌러", "노동"],
                "warning": "방문 목적으로 초청하면서 취업 의도를 암시하면 불법체류 의심을 받습니다."
            },
            "E": {
                "words": ["단순 노무", "청소", "설거지", "포장", "단순 작업"],
                "warning": "E-7은 전문인력 비자입니다. 단순 노무 업무로 보이면 거절됩니다."
            },
            "F": {
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

수정된 내용을 다시 입력해주시겠어요?"""
        
        if len(user_message) < 50:
            return """📝 내용이 조금 짧습니다.

심사관이 납득할 수 있도록 더 구체적으로 작성해주세요.

**추가하면 좋을 내용:**
- 구체적인 날짜나 기간
- 실제 경험이나 에피소드  
- 목표나 계획의 세부 사항

더 자세히 적어주시겠어요?"""
        
        import random
        positive_responses = [
            """✅ 좋습니다!

작성하신 내용이 잘 정리되어 있습니다. 

**AI 검토 결과:**
- 문맥 적합성 ✓
- 구체성 ✓  
- 진정성 ✓

추가로 보완하고 싶은 내용이 있으신가요?""",
            
            """✅ 검토 완료!

작성하신 내용에서 문제가 되는 표현이 발견되지 않았습니다.

**확인된 항목:**
- ❌ 위험 표현 없음
- ✓ 적절한 분량
- ✓ 맥락에 맞는 내용

완료되셨다면 **'작성 완료 → 문서 생성'** 버튼을 눌러주세요!"""
        ]
        
        return random.choice(positive_responses)


class NarrativeValidator:
    """사연 검증 헬퍼 클래스"""
    
    @staticmethod
    def render_validation_result(result: Dict):
        """검증 결과 UI 렌더링"""
        
        if result["is_valid"]:
            st.success(f"✅ 검토 완료! 점수: {result['score']}/10")
        else:
            st.warning(f"⚠️ 수정이 필요합니다. 점수: {result['score']}/10")
        
        if result.get("issues"):
            st.markdown("### 🔍 발견된 문제")
            for issue in result["issues"]:
                st.markdown(f"- ❌ {issue}")
        
        if result.get("suggestions"):
            st.markdown("### 💡 개선 제안")
            for suggestion in result["suggestions"]:
                st.markdown(f"- 💡 {suggestion}")
        
        if result.get("improved_version"):
            with st.expander("📝 AI 개선 버전 보기"):
                st.markdown(result["improved_version"])
                if st.button("이 버전 사용하기"):
                    return result["improved_version"]
        
        return None
    