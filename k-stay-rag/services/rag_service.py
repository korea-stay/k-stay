"""
RAG (Retrieval-Augmented Generation) 서비스
OpenAI API + Supabase pgvector 기반
키워드/패턴 검색 우선 방식
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from openai import OpenAI
from supabase import create_client, Client

@dataclass
class SearchResult:
    """검색 결과"""
    chunk_id: str
    content: str
    metadata: Dict
    similarity: float

@dataclass
class RAGResponse:
    """RAG 응답"""
    answer: str
    sources: List[SearchResult]
    tokens_used: int

class RAGService:
    """RAG 서비스 클래스"""
    
    def __init__(
        self,
        openai_api_key: str = None,
        supabase_url: str = None,
        supabase_key: str = None,
        embedding_model: str = "text-embedding-3-small",
        chat_model: str = "gpt-4o-mini",
        max_context_chunks: int = 5
    ):
        self.openai_client = OpenAI(
            api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        
        self.supabase: Client = create_client(
            supabase_url or os.getenv("SUPABASE_URL"),
            supabase_key or os.getenv("SUPABASE_KEY")
        )
        
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.max_context_chunks = max_context_chunks
        self.embedding_dimension = 1536
    
    # ==================== 임베딩 ====================
    
    def create_embedding(self, text: str) -> List[float]:
        """텍스트 임베딩 생성"""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """배치 임베딩 생성"""
        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
    # ==================== 벡터 저장 ====================
    
    def store_chunk(
        self,
        chunk_id: str,
        content: str,
        metadata: Dict,
        embedding: List[float] = None
    ) -> bool:
        """청크를 벡터 DB에 저장"""
        try:
            if embedding is None:
                embedding = self.create_embedding(content)
            
            data = {
                "chunk_id": chunk_id,
                "content": content,
                "metadata": metadata,
                "embedding": embedding
            }
            
            self.supabase.table("visa_documents").upsert(data).execute()
            return True
            
        except Exception as e:
            print(f"저장 오류: {e}")
            return False
    
    def store_chunks_batch(self, chunks: List[Dict]) -> int:
        """배치로 청크 저장"""
        stored_count = 0
        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.create_embeddings_batch(texts)
        
        for chunk, embedding in zip(chunks, embeddings):
            success = self.store_chunk(
                chunk_id=chunk["id"],
                content=chunk["content"],
                metadata={
                    "category": chunk.get("category", ""),
                    "subcategory": chunk.get("subcategory", ""),
                    "title": chunk.get("title", ""),
                    "keywords": chunk.get("keywords", [])
                },
                embedding=embedding
            )
            if success:
                stored_count += 1
        
        return stored_count
    
    # ==================== 검색 (키워드/패턴 우선) ====================
    
    def search_similar(
        self,
        query: str,
        top_k: int = None
    ) -> List[SearchResult]:
        """문서 검색 - 패턴 매칭 우선"""
        top_k = top_k or self.max_context_chunks
        print(f"\n{'='*50}")
        print(f"🔍 검색: '{query}'")
        print('='*50)
        
        # 1단계: chunk_id 패턴 매칭 (가장 정확)
        results = self._smart_pattern_search(query, top_k)
        
        if len(results) >= 2:
            print(f"✅ 패턴 검색 성공: {len(results)}개")
            self._print_results(results)
            return results
        
        # 2단계: 키워드 검색
        print("  → 패턴 결과 부족, 키워드 검색 추가...")
        keyword_results = self._keyword_search(query, top_k)
        
        # 결과 합치기 (중복 제거)
        for kr in keyword_results:
            if not any(r.chunk_id == kr.chunk_id for r in results):
                results.append(kr)
        
        if results:
            print(f"✅ 최종 검색 결과: {len(results)}개")
            self._print_results(results)
        else:
            print("❌ 검색 결과 없음")
        
        return results[:top_k]
    
    def _smart_pattern_search(self, query: str, top_k: int) -> List[SearchResult]:
        """스마트 패턴 검색 - 질문 분석 후 관련 chunk_id 찾기"""
        try:
            patterns = self._analyze_query(query)
            print(f"  📝 분석된 패턴: {patterns}")
            
            results = []
            
            for pattern in patterns:
                response = self.supabase.table("visa_documents").select(
                    "chunk_id, content, metadata"
                ).ilike("chunk_id", f"%{pattern}%").execute()
                
                if response.data:
                    for item in response.data:
                        if not any(r.chunk_id == item["chunk_id"] for r in results):
                            results.append(SearchResult(
                                chunk_id=item["chunk_id"],
                                content=item["content"],
                                metadata=item["metadata"] or {},
                                similarity=0.9
                            ))
                
                if len(results) >= top_k:
                    break
            
            return results[:top_k]
            
        except Exception as e:
            print(f"  ❌ 패턴 검색 오류: {e}")
            return []
    
    def _analyze_query(self, query: str) -> List[str]:
        """질문 분석하여 검색 패턴 추출"""
        patterns = []
        q = query.lower()
        
        # === 인사/잡담 감지 (검색 불필요) ===
        greetings = ["하이", "안녕", "헬로", "hello", "hi", "hey", "반가워", "ㅎㅇ", "ㅎㅎ", "ㅋㅋ"]
        small_talk = ["뭐해", "뭐하니", "심심", "고마워", "감사", "잘가", "바이", "bye", "굿", "good", "네", "응", "오케이", "ok", "알겠어", "ㅇㅋ"]
        
        # 짧은 인사/잡담이면 검색 안함
        if len(q.strip()) <= 10:
            for g in greetings + small_talk:
                if g in q:
                    return []  # 빈 패턴 반환 → 검색 안함
        
        # 비자 관련 키워드가 없으면 검색 안함
        visa_keywords = ["비자", "visa", "체류", "자격", "f-6", "f6", "d-10", "d10", "d-2", "d2", "c-4", "c4",
                        "유학", "유학생", "대학", "학사", "석사", "박사", "아르바이트", "시간제", "학교",
                        "구직", "결혼", "이민", "혼인", "배우자", "서류", "신청", "연장", "변경",
                        "단기취업", "계절근로", "근무처", "흥행", "모델", "강연"]
        
        has_visa_keyword = any(kw in q for kw in visa_keywords)
        if not has_visa_keyword:
            return []  # 비자 관련 없으면 검색 안함
        
        # === F-6 세부 유형 (결혼이민) ===
        if "f-6-1" in q or "f6-1" in q:
            patterns.append("f6_1")
        if "f-6-2" in q or "f6-2" in q:
            patterns.append("f6_2")
        if "f-6-3" in q or "f6-3" in q:
            patterns.append("f6_3")
        if "f-1-6" in q or "f1-6" in q:
            patterns.append("f6_1_6")
        
        # === F-6 주제별 ===
        is_f6_query = "f-6" in q or "f6" in q or "결혼" in q or "혼인" in q or "배우자" in q
        
        if is_f6_query:
            if "차이" in q or "비교" in q:
                if ("f-6-1" in q or "1" in q) and ("f-6-2" in q or "2" in q):
                    patterns = ["f6_1_definition", "f6_2_definition"]
                elif ("f-6-2" in q or "2" in q) and ("f-6-3" in q or "3" in q):
                    patterns = ["f6_2_definition", "f6_3_definition"]
                elif ("f-6-1" in q or "1" in q) and ("f-6-3" in q or "3" in q):
                    patterns = ["f6_1_definition", "f6_3_definition"]
                else:
                    patterns.extend(["f6_1_definition", "f6_2_definition", "f6_3_definition"])
            
            if "소득" in q:
                patterns.append("f6_income")
            
            if "의사소통" in q or "한국어" in q or "토픽" in q or "topik" in q:
                patterns.append("f6_communication")
            
            if "주거" in q or "집" in q or "거주" in q:
                patterns.append("f6_housing")
            
            if "서류" in q or "제출" in q or "준비" in q:
                patterns.append("f6_required_documents")
                patterns.append("f6_income_documents")
            
            if "체류" in q or "기간" in q or "연장" in q:
                patterns.append("f6_extension")
            
            if "변경" in q or "자격변경" in q:
                patterns.append("f6_status_change")
            
            if "이혼" in q:
                patterns.append("f6_3_divorce")
                patterns.append("f6_3_definition")
            
            if "사망" in q:
                patterns.append("f6_3_death")
            
            if "실종" in q:
                patterns.append("f6_3_missing")
            
            if "별거" in q:
                patterns.append("f6_1_separation")
            
            if "자녀" in q or "양육" in q or "아이" in q:
                patterns.append("f6_2")
                patterns.append("f6_simplified_documents_child")
            
            if "면제" in q:
                patterns.append("f6_income_exemption")
                patterns.append("f6_communication_exemption")
            
            if "국제결혼" in q or "안내프로그램" in q:
                patterns.append("f6_international_marriage_program")
            
            if "결핵" in q or "건강" in q or "진단서" in q:
                patterns.append("f6_tb_high_risk")
                patterns.append("f6_korean_spouse_health")
                patterns.append("f6_foreign_spouse_documents")
            
            if "재입국" in q:
                patterns.append("f6_reentry")
            
            if "등록" in q:
                patterns.append("f6_foreigner_registration")
            
            if "교제" in q or "만남" in q or "사귄" in q:
                patterns.append("f6_dating_proof")
            
            # F-6 일반 질문
            if not patterns:
                patterns = ["f6_overview", "f6_1_definition"]
        
        # === D-10 세부 유형 ===
        if "d-10-1" in q or "d10-1" in q:
            patterns.append("d10_1")
        if "d-10-2" in q or "d10-2" in q:
            patterns.append("d10_2")
        if "d-10-3" in q or "d10-3" in q:
            patterns.append("d10_3")
        if "d-10-t" in q or "d10-t" in q or "최우수" in q:
            patterns.append("d10_t")
        
        # === D-10 주제별 ===
        is_d10_query = "d-10" in q or "d10" in q or "구직" in q
        
        if is_d10_query and not is_f6_query:
            if "차이" in q or "비교" in q:
                if ("d-10-1" in q or "1" in q) and ("d-10-2" in q or "2" in q):
                    patterns = ["d10_1_activity", "d10_2_activity"]
                elif ("d-10-2" in q or "2" in q) and ("d-10-3" in q or "3" in q):
                    patterns = ["d10_2_activity", "d10_3_activity"]
                else:
                    patterns.extend(["activity"])
            
            if "점수" in q or "배점" in q:
                patterns.append("points")
            
            if "서류" in q or "제출" in q or "준비" in q:
                patterns.append("documents")
            
            if "체류" in q or "기간" in q or "연장" in q:
                patterns.append("stay")
            
            if "자격" in q or "요건" in q or "조건" in q:
                if not patterns:
                    patterns.append("eligibility")
                patterns.append("activity")
            
            if "시간" in q and "취업" in q:
                patterns.append("parttime")
            
            if "인턴" in q:
                patterns.append("intern")
            
            if "창업" in q or "기술창업" in q:
                patterns.append("d10_2")
            
            if "일반" in q and "구직" in q:
                patterns.append("d10_1")
            
            if "첨단" in q or "기술인턴" in q:
                patterns.append("d10_3")
            
            if "제한" in q or "불가" in q:
                patterns.append("restriction")
            
            if "재입국" in q or "출국" in q:
                patterns.append("reentry")
            
            if "등록" in q:
                patterns.append("registration")
            
            # D-10 일반 질문
            if not patterns:
                patterns = ["d10_overview", "d10_1_activity"]
        
        # === D-2 세부 유형 (유학) ===
        if "d-2-1" in q or "d2-1" in q:
            patterns.append("d2_subtypes")
        if "d-2-2" in q or "d2-2" in q:
            patterns.append("d2_subtypes")
        if "d-2-3" in q or "d2-3" in q:
            patterns.append("d2_subtypes")
        if "d-2-4" in q or "d2-4" in q:
            patterns.append("d2_subtypes")
        if "d-2-5" in q or "d2-5" in q:
            patterns.append("d2_research_exception")
        if "d-2-6" in q or "d2-6" in q:
            patterns.append("d2_subtypes")
        if "d-2-7" in q or "d2-7" in q:
            patterns.append("d2_subtypes")
        if "d-2-8" in q or "d2-8" in q:
            patterns.append("d2_subtypes")
        
        # === 학교변경은 D-2 전용 (먼저 체크) ===
        if ("학교" in q and "변경" in q) or "학교변경" in q or "전학" in q or "편입" in q:
            patterns.append("d2_school_change_principle")
            patterns.append("d2_school_change_restriction")
            patterns.append("d2_school_change_documents")
        
        # === D-2 주제별 ===
        is_d2_query = "d-2" in q or "d2" in q or "유학" in q or "유학생" in q or "대학" in q or "학사" in q or "석사" in q or "박사" in q or "학교" in q
        
        if is_d2_query and not is_f6_query and not is_d10_query:
            if "종류" in q or "유형" in q or "세부" in q:
                patterns.append("d2_subtypes")
            
            if "시간제" in q or "아르바이트" in q or "알바" in q or "파트타임" in q:
                patterns.append("d2_parttime_principle")
                patterns.append("d2_parttime_hours")
                patterns.append("d2_parttime_target")
            
            if "허용시간" in q or "몇시간" in q or "근무시간" in q:
                patterns.append("d2_parttime_hours")
            
            if "제한" in q and ("취업" in q or "분야" in q):
                patterns.append("d2_parttime_restricted")
            
            if "서류" in q or "제출" in q or "준비" in q:
                if "시간제" in q or "아르바이트" in q or "취업" in q:
                    patterns.append("d2_parttime_documents")
                elif "연장" in q:
                    patterns.append("d2_extension_documents")
                elif "등록" in q:
                    patterns.append("d2_registration_documents")
                elif "변경" in q:
                    patterns.append("d2_status_change_documents")
                else:
                    patterns.append("d2_parttime_documents")
                    patterns.append("d2_extension_documents")
            
            if "체류" in q or "기간" in q or "연장" in q:
                patterns.append("d2_extension_principle")
                patterns.append("d2_extension_max_period")
            
            if "변경" in q or "자격변경" in q:
                patterns.append("d2_status_change_principle")
                patterns.append("d2_status_change_documents")
            
            if "학교" in q and "변경" in q:
                patterns.append("d2_school_change_principle")
                patterns.append("d2_school_change_restriction")
            
            if "인증대학" in q or "우수대학" in q:
                patterns.append("d2_extension_certified_univ")
            
            if "비자심사강화" in q or "하위대학" in q:
                patterns.append("d2_extension_reinforced_univ")
                patterns.append("d2_visa_reinforced_korean")
            
            if "한국어" in q or "토픽" in q or "topik" in q:
                patterns.append("d2_parttime_hours")
                patterns.append("d2_visa_reinforced_korean")
            
            if "영어" in q or "영어트랙" in q or "toefl" in q or "ielts" in q:
                patterns.append("d2_parttime_english_track")
                patterns.append("d2_visa_reinforced_english")
            
            if "연구" in q or "연구활동" in q:
                patterns.append("d2_research_activity")
                patterns.append("d2_research_exception")
            
            if "현장실습" in q or "실습" in q:
                patterns.append("d2_field_training")
            
            if "재입국" in q or "출국" in q:
                patterns.append("d2_reentry")
            
            if "등록" in q and ("외국인" in q or "신고" in q):
                patterns.append("d2_registration_documents")
                patterns.append("d2_registration_change")
            
            if "휴학" in q:
                patterns.append("d2_extension_leave_restriction")
            
            if "야간" in q or "주말" in q:
                patterns.append("d2_extension_night_class")
                patterns.append("d2_excluded_institutions")
            
            if "위반" in q or "처벌" in q or "불법" in q:
                patterns.append("d2_parttime_violation")
            
            if "하위" in q and "과정" in q:
                patterns.append("d2_lower_degree_exception")
                patterns.append("d2_lower_degree_majors")
            
            # D-2 일반 질문
            if not patterns:
                patterns = ["d2_overview", "d2_subtypes"]
        
        # === C-4 세부 유형 (단기취업) ===
        if "c-4-1" in q or "c4-1" in q:
            patterns.append("c4_seasonal_work")
        if "c-4-2" in q or "c4-2" in q:
            patterns.append("c4_seasonal_work")
        if "c-4-3" in q or "c4-3" in q:
            patterns.append("c4_seasonal_work")
        if "c-4-4" in q or "c4-4" in q:
            patterns.append("c4_seasonal_work")
        if "c-4-5" in q or "c4-5" in q:
            patterns.append("c4_other_work")
        
        # === C-4 주제별 ===
        is_c4_query = "c-4" in q or "c4" in q or "단기취업" in q or "계절근로" in q
        
        if is_c4_query and not is_f6_query and not is_d10_query and not is_d2_query:
            if "계절" in q or "농작물" in q or "수확" in q or "수산물" in q:
                patterns.append("c4_seasonal_work")
                patterns.append("c4_seasonal_workplace_change")
            
            if "흥행" in q or "모델" in q or "강연" in q or "강의" in q or "연구" in q or "기술지도" in q:
                patterns.append("c4_other_work")
            
            if "근무처" in q and ("변경" in q or "추가" in q):
                if "계절" in q:
                    patterns.append("c4_seasonal_workplace_change")
                    patterns.append("c4_seasonal_change_documents")
                else:
                    patterns.append("c4_other_workplace_change")
                    patterns.append("c4_workplace_addition")
            
            if "서류" in q or "제출" in q:
                if "연장" in q:
                    patterns.append("c4_extension_documents")
                elif "변경" in q and "자격" in q:
                    patterns.append("c4_status_change_documents")
                else:
                    patterns.append("c4_change_documents")
                    patterns.append("c4_seasonal_change_documents")
            
            if "연장" in q or "기간" in q:
                patterns.append("c4_extension_principle")
                patterns.append("c4_extension_documents")
            
            if "자격" in q and "변경" in q:
                patterns.append("c4_status_change_athlete")
                patterns.append("c4_status_change_celebrity")
            
            if "운동" in q or "선수" in q or "연주" in q or "무용" in q:
                patterns.append("c4_status_change_athlete")
            
            if "저명" in q or "노벨" in q:
                patterns.append("c4_status_change_celebrity")
            
            if "출국" in q:
                patterns.append("c4_extension_departure")
            
            # C-4 일반 질문
            if not patterns:
                patterns = ["c4_overview", "c4_seasonal_work", "c4_other_work"]
        
        # === 기본값 ===
        if not patterns:
            # 비자 유형을 특정할 수 없는 경우 키워드로 판단
            if "결혼" in q or "혼인" in q or "배우자" in q:
                patterns = ["f6_overview"]
            elif "구직" in q:
                patterns = ["d10_overview"]
            elif "유학" in q or "유학생" in q or "대학" in q or "학사" in q or "석사" in q or "박사" in q:
                patterns = ["d2_overview"]
            elif "단기취업" in q or "계절근로" in q or "흥행" in q or "모델" in q:
                patterns = ["c4_overview"]
            else:
                patterns = ["f6_overview", "d10_overview", "d2_overview", "c4_overview"]
        
        return patterns
    
    def _keyword_search(self, query: str, top_k: int) -> List[SearchResult]:
        """content 내용에서 키워드 검색"""
        try:
            results = []
            keywords = self._extract_keywords(query)
            print(f"  📝 키워드: {keywords}")
            
            for keyword in keywords:
                response = self.supabase.table("visa_documents").select(
                    "chunk_id, content, metadata"
                ).ilike("content", f"%{keyword}%").limit(3).execute()
                
                if response.data:
                    for item in response.data:
                        if not any(r.chunk_id == item["chunk_id"] for r in results):
                            results.append(SearchResult(
                                chunk_id=item["chunk_id"],
                                content=item["content"],
                                metadata=item["metadata"] or {},
                                similarity=0.7
                            ))
                
                if len(results) >= top_k:
                    break
            
            return results[:top_k]
            
        except Exception as e:
            print(f"  ❌ 키워드 검색 오류: {e}")
            return []
    
    def _extract_keywords(self, query: str) -> List[str]:
        """검색용 키워드 추출"""
        keywords = []
        
        # F-6 비자 유형 키워드
        if "F-6-1" in query.upper():
            keywords.append("F-6-1")
            keywords.append("국민의 배우자")
        if "F-6-2" in query.upper():
            keywords.append("F-6-2")
            keywords.append("자녀 양육")
        if "F-6-3" in query.upper():
            keywords.append("F-6-3")
            keywords.append("혼인단절")
        if "F-6" in query.upper() or "결혼" in query or "혼인" in query or "배우자" in query:
            keywords.append("F-6")
            keywords.append("결혼이민")
        
        # D-10 비자 유형 키워드
        if "D-10-1" in query.upper():
            keywords.append("D-10-1")
            keywords.append("일반구직")
        if "D-10-2" in query.upper():
            keywords.append("D-10-2")
            keywords.append("기술창업준비")
        if "D-10-3" in query.upper():
            keywords.append("D-10-3")
            keywords.append("첨단기술인턴")
        if "D-10-T" in query.upper():
            keywords.append("D-10-T")
            keywords.append("최우수인재")
        if "D-10" in query.upper() or "구직" in query:
            keywords.append("D-10")
            keywords.append("구직")
        
        # D-2 비자 유형 키워드
        if "D-2-1" in query.upper():
            keywords.append("D-2-1")
            keywords.append("전문학사")
        if "D-2-2" in query.upper():
            keywords.append("D-2-2")
            keywords.append("학사")
        if "D-2-3" in query.upper():
            keywords.append("D-2-3")
            keywords.append("석사")
        if "D-2-4" in query.upper():
            keywords.append("D-2-4")
            keywords.append("박사")
        if "D-2-5" in query.upper():
            keywords.append("D-2-5")
            keywords.append("연구")
        if "D-2-6" in query.upper():
            keywords.append("D-2-6")
            keywords.append("교환학생")
        if "D-2-7" in query.upper():
            keywords.append("D-2-7")
            keywords.append("일-학습연계")
        if "D-2-8" in query.upper():
            keywords.append("D-2-8")
            keywords.append("방문학생")
        if "D-2" in query.upper() or "유학" in query or "유학생" in query:
            keywords.append("D-2")
            keywords.append("유학")
        
        # C-4 비자 유형 키워드
        if "C-4-1" in query.upper() or "C-4-2" in query.upper() or "C-4-3" in query.upper() or "C-4-4" in query.upper():
            keywords.append("C-4")
            keywords.append("계절근로")
        if "C-4-5" in query.upper():
            keywords.append("C-4-5")
            keywords.append("단기취업")
        if "C-4" in query.upper() or "단기취업" in query or "계절근로" in query:
            keywords.append("C-4")
            keywords.append("단기취업")
        if "흥행" in query or "모델" in query or "강연" in query:
            keywords.append("C-4")
            keywords.append("단기취업")
        
        # 주제 키워드
        topic_keywords = {
            "점수": "점수",
            "서류": "서류",
            "체류": "체류기간",
            "자격": "자격요건",
            "시간제": "시간제",
            "인턴": "인턴",
            "창업": "창업",
            "연장": "연장",
            "소득": "소득요건",
            "한국어": "의사소통",
            "주거": "주거요건",
            "이혼": "이혼",
            "사망": "사망",
            "자녀": "자녀",
            "양육": "양육",
            "국제결혼": "국제결혼",
            "건강": "건강진단서",
            "범죄": "범죄경력",
            "아르바이트": "시간제취업",
            "알바": "시간제취업",
            "학교변경": "학교 변경",
            "대학": "대학",
            "휴학": "휴학",
            "근무처": "근무처",
            "계절": "계절근로",
        }
        
        for key, value in topic_keywords.items():
            if key in query:
                keywords.append(value)
        
        if not keywords:
            # 기본 키워드
            if "결혼" in query or "혼인" in query or "배우자" in query:
                keywords = ["F-6", "결혼이민"]
            elif "유학" in query or "유학생" in query or "대학" in query:
                keywords = ["D-2", "유학"]
            elif "단기취업" in query or "계절근로" in query or "흥행" in query or "모델" in query:
                keywords = ["C-4", "단기취업"]
            else:
                keywords = ["D-10", "구직"]
        
        return keywords[:5]
    
    def _print_results(self, results: List[SearchResult]):
        """검색 결과 출력"""
        for i, r in enumerate(results[:3], 1):
            title = r.metadata.get("title", r.chunk_id) if r.metadata else r.chunk_id
            print(f"  [{i}] {title}")
    
    # ==================== RAG 응답 생성 ====================
    
    def generate_response(
        self,
        query: str,
        search_results: List[SearchResult] = None,
        conversation_history: List[Dict] = None,
        language: str = "ko"
    ) -> RAGResponse:
        """RAG 기반 응답 생성"""
        
        # 인사/잡담 감지
        if self._is_greeting_or_smalltalk(query):
            return self._generate_greeting_response(query, conversation_history)
        
        if search_results is None:
            search_results = self.search_similar(query)
        
        context = self._build_context(search_results)
        system_prompt = self._get_system_prompt(language)
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history[-6:])
        
        if search_results:
            user_message = f"""참고 자료:
{context}

사용자 질문: {query}

위 참고 자료를 기반으로 정확하게 답변해주세요. 참고 자료에 없는 내용은 추측하지 마세요."""
        else:
            user_message = f"""사용자 질문: {query}

관련 자료를 찾지 못했습니다. 
다음과 같이 안내해주세요:
- "죄송합니다. 해당 질문에 대한 정확한 자료를 찾지 못했습니다."
- 현재 지원하는 비자: D-2(유학), D-10(구직), F-6(결혼이민), C-4(단기취업)
- 정확한 정보는 출입국관리사무소 또는 하이코리아(www.hikorea.go.kr)에서 확인하시기 바랍니다.
- 절대로 자체 지식으로 비자 정보를 만들어내지 마세요."""
        
        messages.append({"role": "user", "content": user_message})
        
        response = self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )
        
        answer = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        return RAGResponse(
            answer=answer,
            sources=search_results,
            tokens_used=tokens_used
        )
    
    def _is_greeting_or_smalltalk(self, query: str) -> bool:
        """인사/잡담/일상대화인지 확인"""
        q = query.lower().strip()
        
        # 비자 관련 키워드 (이게 있으면 무조건 비자 질문)
        visa_keywords = ["비자", "visa", "체류", "자격", "f-6", "f6", "d-10", "d10", "d-2", "d2", "c-4", "c4",
                        "유학", "유학생", "구직", "결혼", "이민", "서류", "신청", "연장", "변경",
                        "학교", "대학", "아르바이트", "취업", "근무", "허가", "등록", "외국인"]
        
        has_visa_keyword = any(kw in q for kw in visa_keywords)
        if has_visa_keyword:
            return False
        
        # 인사/잡담/일상 패턴
        greetings = ["하이", "안녕", "헬로", "hello", "hi", "hey", "반가워", "ㅎㅇ", "ㅎㅎ", "ㅋㅋ", "안뇽"]
        small_talk = ["뭐해", "뭐하니", "심심", "고마워", "감사", "잘가", "바이", "bye", "굿", "good", 
                     "네", "응", "오케이", "ok", "알겠어", "ㅇㅋ", "잘했어", "좋아", "멋져"]
        everyday = ["배고", "졸려", "졸리", "피곤", "힘들", "지쳐", 
                   "뭐먹", "밥먹", "점심", "저녁", "아침", "간식", "커피", "음식", "맛집",
                   "날씨", "덥다", "춥다", "비온다", "눈온다", "화창", "흐림",
                   "ㅠㅠ", "ㅜㅜ", "ㅋㅋㅋ", "ㅎㅎㅎ", "ㄱㅅ", "ㄴㄴ", "ㅇㅇ",
                   "재미없", "심심하", "놀자", "놀아", "영화", "게임", "음악", "노래"]
        
        all_patterns = greetings + small_talk + everyday
        
        # 짧은 메시지이고 일상 패턴 포함
        if len(q) <= 20:
            for pattern in all_patterns:
                if pattern in q:
                    return True
        
        # 아주 짧고 비자 키워드 없는 입력 (오타, 의미없는 입력)
        if len(q) <= 10 and not has_visa_keyword:
            # 한글 자음/모음만 있거나 의미없는 짧은 입력
            meaningful_chars = sum(1 for c in q if c.isalnum())
            if meaningful_chars <= 6:
                return True
        
        return False
    
    def _generate_greeting_response(self, query: str, conversation_history: List[Dict] = None) -> RAGResponse:
        """인사/잡담/일상대화에 대한 응답 생성"""
        messages = [
            {"role": "system", "content": """당신은 K-Stay 비자 상담 AI입니다.

사용자가 인사하면 간단히 인사로 응답하고, 비자 관련 질문이 있으면 도움을 드릴 수 있다고 안내하세요.

비자와 관련 없는 일상적인 이야기(음식, 날씨, 감정 표현 등)에는:
- 짧고 친근하게 공감하거나 응답하세요
- 비자 관련 도움이 필요하면 질문해달라고 자연스럽게 안내하세요
- 절대로 비자 정보를 임의로 제공하지 마세요
- 음식 추천, 날씨 정보 등 비자와 무관한 정보는 제공하지 마세요

응답은 1-2문장으로 짧게 하세요."""},
            {"role": "user", "content": query}
        ]
        
        if conversation_history:
            messages = [messages[0]] + conversation_history[-4:] + [messages[-1]]
        
        response = self.openai_client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        return RAGResponse(
            answer=response.choices[0].message.content,
            sources=[],  # 참고자료 없음
            tokens_used=response.usage.total_tokens
        )
    
    def _build_context(self, search_results: List[SearchResult]) -> str:
        """검색 결과로 컨텍스트 구성"""
        if not search_results:
            return ""
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            title = result.metadata.get("title", "") if result.metadata else ""
            category = result.metadata.get("category", "") if result.metadata else ""
            
            context_parts.append(f"""[자료 {i}] {category} - {title}
{result.content}
""")
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self, language: str) -> str:
        """시스템 프롬프트"""
        return """당신은 한국 비자 및 체류자격 전문 상담 AI입니다.

역할:
- 제공된 참고 자료를 기반으로 정확하게 답변합니다.
- 참고 자료에 있는 내용을 우선적으로 사용하세요.
- 참고 자료에 없는 내용은 추측하지 마세요.

답변 스타일:
- 친절하고 이해하기 쉬운 언어를 사용합니다.
- 필요한 서류, 절차, 기간 등을 구체적으로 안내합니다.
- 중요한 주의사항이 있으면 강조합니다.
- 답변은 한국어로 합니다."""
    
    # ==================== 대화 관리 ====================
    
    def chat(
        self,
        query: str,
        session_id: str = None,
        conversation_history: List[Dict] = None
    ) -> Tuple[str, List[Dict]]:
        """대화형 인터페이스"""
        
        rag_response = self.generate_response(
            query=query,
            conversation_history=conversation_history
        )
        
        # 참고자료가 있을 때만 출처 표시
        source_info = ""
        if rag_response.sources and len(rag_response.sources) > 0:
            source_titles = []
            for s in rag_response.sources[:3]:
                title = s.metadata.get("title", s.chunk_id) if s.metadata else s.chunk_id
                source_titles.append(title)
            source_info = f"\n\n📚 참고: {', '.join(source_titles)}"
        
        full_answer = rag_response.answer + source_info
        
        if conversation_history is None:
            conversation_history = []
        
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": full_answer})
        
        return full_answer, conversation_history


# ==================== 간편 함수 ====================

def create_rag_service() -> RAGService:
    """RAG 서비스 인스턴스 생성"""
    return RAGService()


def quick_answer(query: str) -> str:
    """빠른 답변"""
    service = create_rag_service()
    response = service.generate_response(query)
    return response.answer