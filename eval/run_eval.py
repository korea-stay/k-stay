"""
RAG 검색 평가 스크립트
eval/questions.json의 질문으로 검색 방식별 성능을 비교

실행: python eval/run_eval.py [--modes pattern vector] [--top-k 5]

지표
- Hit@1 / Hit@k : 정답 청크가 1위 / 상위 k개 안에 있는 비율
- MRR           : 첫 정답 순위의 역수 평균 (1위=1.0, 2위=0.5 ...)
- 타비자 혼입률 : 상위 k개 중 질문 대상이 아닌 비자 청크의 비율
- 결과없음      : 검색 결과가 0건인 질문 비율
"""

import sys
import io
import json
import glob
import argparse
import contextlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from services.rag_service import RAGService


def load_chunk_visa_map() -> dict:
    """chunk_id → 비자 코드 (지식베이스 파일 기준)"""
    mapping = {}
    for path in glob.glob(str(ROOT / "data" / "*_knowledge.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for chunk in data["chunks"]:
            mapping[chunk["id"]] = data["visa_type"]
    return mapping


# ==================== 검색 방식 ====================

def search_pattern(rag: RAGService, item: dict, top_k: int) -> list:
    """현재 운영 방식: 규칙 기반 패턴/키워드 검색 (영어는 번역 후 검색, 대화 이력 미사용)"""
    query = item["q"]
    if item.get("lang") == "en":
        query = rag._translate_query_to_korean(query)
    with contextlib.redirect_stdout(io.StringIO()):
        results = rag.search_similar(query, top_k=top_k)
    return [r.chunk_id for r in results]


def search_vector(rag: RAGService, item: dict, top_k: int) -> list:
    """벡터 검색: 질문 임베딩 → match_visa_documents RPC (번역 없음, 대화 이력 미사용)"""
    embedding = rag.create_embedding(item["q"], task_type="RETRIEVAL_QUERY")
    response = rag.supabase.rpc("match_visa_documents", {
        "query_embedding": embedding,
        "match_threshold": 0.0,
        "match_count": top_k
    }).execute()
    return [row["chunk_id"] for row in response.data]


SEARCH_MODES = {
    "pattern": search_pattern,
    "vector": search_vector,
}


# ==================== 평가 ====================

def evaluate(rag, mode: str, questions: list, chunk_visa: dict, top_k: int) -> dict:
    search_fn = SEARCH_MODES[mode]
    rows = []
    for item in questions:
        try:
            retrieved = search_fn(rag, item, top_k)
            error = None
        except Exception as e:
            retrieved, error = [], str(e)[:120]

        expected = set(item["expected"])
        rank = next((i + 1 for i, cid in enumerate(retrieved) if cid in expected), None)
        other_visa = sum(1 for cid in retrieved if chunk_visa.get(cid) != item["visa"])
        rows.append({
            "id": item["id"],
            "q": item["q"],
            "retrieved": retrieved,
            "rank": rank,
            "contamination": other_visa / len(retrieved) if retrieved else 0.0,
            "error": error,
        })

    n = len(rows)
    return {
        "mode": mode,
        "rows": rows,
        "hit1": sum(1 for r in rows if r["rank"] == 1) / n,
        "hitk": sum(1 for r in rows if r["rank"]) / n,
        "mrr": sum(1 / r["rank"] for r in rows if r["rank"]) / n,
        "contamination": sum(r["contamination"] for r in rows) / n,
        "empty": sum(1 for r in rows if not r["retrieved"]) / n,
    }


def print_report(results: list, top_k: int):
    print("\n" + "=" * 72)
    print(f"{'방식':<10}{'Hit@1':>9}{f'Hit@{top_k}':>9}{'MRR':>8}{'타비자 혼입':>12}{'결과없음':>10}")
    print("-" * 72)
    for res in results:
        print(f"{res['mode']:<10}{res['hit1']:>9.1%}{res['hitk']:>9.1%}{res['mrr']:>8.3f}"
              f"{res['contamination']:>12.1%}{res['empty']:>10.1%}")
    print("=" * 72)

    # 질문별 비교 (하나라도 놓친 질문만)
    modes = [res["mode"] for res in results]
    print(f"\n놓친 질문 (순위, - = 상위 {top_k}개 밖)")
    print(f"{'id':<11}" + "".join(f"{m:>9}" for m in modes) + "  질문")
    for i, row in enumerate(results[0]["rows"]):
        ranks = [res["rows"][i]["rank"] for res in results]
        if all(r == 1 for r in ranks):
            continue
        cells = "".join(f"{(str(r) if r else '-'):>9}" for r in ranks)
        print(f"{row['id']:<11}{cells}  {row['q']}")
        for res in results:
            r = res["rows"][i]
            if r["rank"] != 1:
                detail = r["error"] or ", ".join(r["retrieved"][:3]) or "(결과 없음)"
                print(f"{'':<11}  └ {res['mode']}: {detail}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--modes", nargs="+", default=list(SEARCH_MODES), choices=list(SEARCH_MODES))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--save", help="결과를 JSON으로 저장할 경로")
    args = parser.parse_args()

    with open(ROOT / "eval" / "questions.json", encoding="utf-8") as f:
        questions = json.load(f)
    chunk_visa = load_chunk_visa_map()
    rag = RAGService()

    results = []
    for mode in args.modes:
        print(f"▶ {mode} 평가 중... ({len(questions)}문항)")
        results.append(evaluate(rag, mode, questions, chunk_visa, args.top_k))

    print_report(results, args.top_k)

    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 저장: {args.save}")


if __name__ == "__main__":
    main()
