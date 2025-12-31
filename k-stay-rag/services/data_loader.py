"""
지식베이스 데이터 로더
JSON 청킹 데이터를 임베딩하여 Supabase에 저장
"""

import os
import json
from typing import List, Dict
from pathlib import Path

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

from rag_service import RAGService


class KnowledgeBaseLoader:
    """지식베이스 로더"""
    
    def __init__(self, rag_service: RAGService = None):
        self.rag_service = rag_service or RAGService()
        self.data_dir = Path(__file__).parent.parent / "data"
    
    def load_json_knowledge(self, file_path: str) -> List[Dict]:
        """JSON 지식베이스 파일 로드"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data.get("chunks", [])
        print(f"📚 {len(chunks)}개 청크 로드됨: {file_path}")
        return chunks
    
    def upload_to_supabase(self, chunks: List[Dict], batch_size: int = 10) -> Dict:
        """청크를 Supabase에 업로드"""
        total = len(chunks)
        uploaded = 0
        failed = 0
        
        print(f"\n🚀 {total}개 청크 업로드 시작...")
        
        # 배치 처리
        for i in range(0, total, batch_size):
            batch = chunks[i:i + batch_size]
            
            try:
                count = self.rag_service.store_chunks_batch(batch)
                uploaded += count
                print(f"  ✅ {i + count}/{total} 완료")
            except Exception as e:
                failed += len(batch)
                print(f"  ❌ 배치 {i//batch_size + 1} 실패: {e}")
        
        result = {
            "total": total,
            "uploaded": uploaded,
            "failed": failed
        }
        
        print(f"\n📊 업로드 결과: 성공 {uploaded}, 실패 {failed}")
        return result
    
    def load_all_knowledge_files(self) -> int:
        """data 폴더의 모든 지식베이스 파일 로드"""
        total_uploaded = 0
        
        json_files = list(self.data_dir.glob("*_knowledge.json"))
        
        if not json_files:
            print("⚠️ 지식베이스 파일이 없습니다.")
            return 0
        
        for file_path in json_files:
            print(f"\n{'='*50}")
            print(f"📁 파일: {file_path.name}")
            print('='*50)
            
            chunks = self.load_json_knowledge(str(file_path))
            result = self.upload_to_supabase(chunks)
            total_uploaded += result["uploaded"]
        
        print(f"\n{'='*50}")
        print(f"🎉 전체 업로드 완료: {total_uploaded}개 청크")
        print('='*50)
        
        return total_uploaded


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("🔧 K-Stay RAG 지식베이스 로더")
    print("=" * 60)
    
    # 환경변수 확인
    required_vars = ["OPENAI_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"\n❌ 필수 환경변수가 없습니다: {', '.join(missing)}")
        print("\n.env 파일에 다음을 추가하세요:")
        print("  OPENAI_API_KEY=sk-...")
        print("  SUPABASE_URL=https://xxx.supabase.co")
        print("  SUPABASE_KEY=eyJ...")
        return
    
    # 로더 실행
    loader = KnowledgeBaseLoader()
    loader.load_all_knowledge_files()


if __name__ == "__main__":
    main()
