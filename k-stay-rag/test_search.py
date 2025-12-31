"""
RAG 검색 테스트 스크립트
실행: python test_search.py
"""

import os
from dotenv import load_dotenv
load_dotenv()

from services.rag_service import RAGService

def test_search():
    print("=" * 60)
    print("🧪 RAG 검색 테스트")
    print("=" * 60)
    
    # RAG 서비스 초기화
    try:
        rag = RAGService()
        print("✅ RAG 서비스 초기화 성공")
    except Exception as e:
        print(f"❌ RAG 서비스 초기화 실패: {e}")
        return
    
    # 테스트 질문들
    test_queries = [
        "D-10 비자",
        "D-10-1과 D-10-2 차이",
        "구직비자 점수제",
        "시간제 취업",
    ]
    
    for query in test_queries:
        print(f"\n{'─' * 50}")
        print(f"📝 질문: {query}")
        print('─' * 50)
        
        try:
            # 검색 테스트
            results = rag.search_similar(query, top_k=3)
            
            if results:
                print(f"✅ 검색 결과: {len(results)}개")
                for i, r in enumerate(results, 1):
                    print(f"  [{i}] {r.chunk_id} (유사도: {r.similarity:.3f})")
                    print(f"      {r.content[:80]}...")
            else:
                print("⚠️ 검색 결과 없음")
                
        except Exception as e:
            print(f"❌ 검색 오류: {e}")
    
    # 전체 응답 테스트
    print(f"\n{'=' * 60}")
    print("🤖 전체 RAG 응답 테스트")
    print("=" * 60)
    
    try:
        response = rag.generate_response("D-10-1과 D-10-2의 차이점이 뭐야?")
        print(f"\n📚 참조 문서: {len(response.sources)}개")
        print(f"💬 응답:\n{response.answer}")
        print(f"\n🔢 사용 토큰: {response.tokens_used}")
    except Exception as e:
        print(f"❌ 응답 생성 오류: {e}")


if __name__ == "__main__":
    test_search()
