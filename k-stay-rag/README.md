# 🤖 K-Stay RAG 챗봇 시스템

OpenAI API + Supabase pgvector 기반의 한국 비자 상담 RAG 챗봇입니다.

---

## 📁 프로젝트 구조

```
k-stay-rag/
├── data/
│   └── d10_visa_knowledge.json   # D-10 비자 지식베이스 (청킹됨)
├── services/
│   ├── rag_service.py            # RAG 핵심 서비스
│   └── data_loader.py            # 데이터 로더
├── pages/
│   └── ai_chat.py                # Streamlit 챗봇 페이지
├── supabase_setup.sql            # Supabase 테이블/함수 설정
├── requirements.txt              # 의존성
├── .env.example                  # 환경변수 템플릿
└── README.md                     # 이 파일
```

---

## 🚀 설치 및 실행

### 1단계: 패키지 설치

```bash
pip install -r requirements.txt
```

### 2단계: 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열고 실제 값을 입력:

```env
OPENAI_API_KEY=sk-your-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ...your-key-here
```

### 3단계: Supabase 테이블 생성

Supabase 대시보드 → SQL Editor에서 `supabase_setup.sql` 내용을 실행합니다.

```sql
-- pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS visa_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 검색 함수 생성 (자세한 내용은 supabase_setup.sql 참조)
```

### 4단계: 지식베이스 업로드

```bash
cd services
python data_loader.py
```

출력 예시:
```
🔧 K-Stay RAG 지식베이스 로더
==================================================
📁 파일: d10_visa_knowledge.json
==================================================
📚 25개 청크 로드됨
🚀 25개 청크 업로드 시작...
  ✅ 10/25 완료
  ✅ 20/25 완료
  ✅ 25/25 완료
📊 업로드 결과: 성공 25, 실패 0
```

### 5단계: 챗봇 실행

```bash
streamlit run pages/ai_chat.py
```

브라우저에서 `http://localhost:8501` 접속

---

## 💬 사용 예시

### Python에서 직접 사용

```python
from services.rag_service import RAGService

# 서비스 초기화
rag = RAGService()

# 단일 질문
response = rag.generate_response("D-10 비자 자격요건이 뭐예요?")
print(response.answer)
print(f"참고 자료: {len(response.sources)}개")

# 대화형
history = []
answer, history = rag.chat("D-10-1 점수제 알려줘", conversation_history=history)
print(answer)

answer, history = rag.chat("그럼 서류는 뭐가 필요해?", conversation_history=history)
print(answer)
```

### 빠른 답변 함수

```python
from services.rag_service import quick_answer

answer = quick_answer("시간제 취업 허용 시간이 어떻게 되나요?")
print(answer)
```

---

## 📊 작동 원리

```
┌─────────────────────────────────────────────────────────────┐
│                      사용자 질문                             │
│              "D-10 비자 연장하려면 뭐가 필요해요?"            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    1. 질문 임베딩 생성                        │
│              OpenAI text-embedding-3-small                  │
│                    [0.023, -0.156, ...]                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   2. 벡터 유사도 검색                         │
│              Supabase pgvector (코사인 유사도)               │
│                                                             │
│   검색 결과:                                                 │
│   - D-10 체류기간 연장 (유사도: 0.89)                        │
│   - D-10-1 제출서류 (유사도: 0.85)                           │
│   - D-10 체류기간 상한 (유사도: 0.82)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   3. 컨텍스트 구성                           │
│                                                             │
│   [자료 1] 체류기간 - D-10 체류기간 연장                      │
│   D-10-1 일반구직 체류기간: 3년(1회 1년 부여)...             │
│                                                             │
│   [자료 2] 제출서류 - D-10-1 점수제 적용                     │
│   공통서류(신청서, 사진, 여권사본...)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4. GPT 응답 생성                           │
│                    OpenAI gpt-4o-mini                       │
│                                                             │
│   "D-10 비자 연장을 위해서는 다음 서류가 필요합니다:          │
│    1. 공통서류 (신청서, 사진, 여권사본, 수수료)               │
│    2. 구직활동 계획서                                        │
│    3. 체재비 입증서류..."                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 커스터마이징

### 새 지식베이스 추가

1. `data/` 폴더에 `{name}_knowledge.json` 파일 생성:

```json
{
  "visa_type": "F-6",
  "visa_name": "결혼이민",
  "chunks": [
    {
      "id": "f6_overview",
      "category": "개요",
      "title": "F-6 결혼이민 개요",
      "content": "F-6 비자는...",
      "keywords": ["F-6", "결혼이민"]
    }
  ]
}
```

2. 데이터 로더 실행:
```bash
python services/data_loader.py
```

### 모델 변경

```python
rag = RAGService(
    embedding_model="text-embedding-3-large",  # 더 정확한 임베딩
    chat_model="gpt-4o",                       # 더 강력한 모델
    max_context_chunks=10                      # 더 많은 컨텍스트
)
```

---

## 💰 비용 예상

| 항목 | 모델 | 가격 |
|------|------|------|
| 임베딩 | text-embedding-3-small | $0.02 / 1M 토큰 |
| 채팅 | gpt-4o-mini | $0.15 / 1M 입력 토큰 |
| Supabase | Free tier | 무료 (500MB) |

**예상 비용 (월 1,000 질문 기준)**: ~$1-2

---

## ❓ FAQ

### Q: 임베딩은 언제 다시 생성해야 하나요?
A: 지식베이스 내용이 변경되었을 때만 다시 생성하면 됩니다.

### Q: 한국어 검색이 잘 되나요?
A: OpenAI 임베딩 모델은 한국어를 잘 지원합니다.

### Q: 대화 이력은 어디에 저장되나요?
A: 현재는 Streamlit 세션에만 저장됩니다. 영구 저장이 필요하면 DB에 저장하는 로직을 추가하세요.

---

## 🐛 문제 해결

### "API key not found" 오류
→ `.env` 파일에 `OPENAI_API_KEY`가 설정되었는지 확인

### "Table does not exist" 오류
→ Supabase에서 `supabase_setup.sql`을 실행했는지 확인

### 검색 결과가 없음
→ 데이터 로더로 지식베이스를 업로드했는지 확인

---

## 📞 지원

문의사항은 K-Stay 팀에 연락해주세요.
