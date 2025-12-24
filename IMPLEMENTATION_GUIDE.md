# 🚀 K-Stay 구현 가이드 (Step-by-Step)

이 문서는 K-Stay를 실제로 배포하기 위해 필요한 모든 단계를 상세히 설명합니다.

---

## 📋 전체 작업 목록

### ✅ Phase 1: 코드 작성 (완료)
- [x] 프로젝트 구조 설정
- [x] 메인 앱 (app.py)
- [x] 설정 파일 (config/settings.py)
- [x] 인증 서비스 (services/auth_service.py)
- [x] 결제 서비스 (services/payment_service.py)
- [x] AI 서비스 (services/ai_service.py)
- [x] 문서 서비스 (services/document_service.py)
- [x] 페이지 컴포넌트 (pages/*)
- [x] DB 스키마 (database/schema.sql)
- [x] RAG 지식 베이스 (rag_data/knowledge_base.py)

### ⏳ Phase 2: 인프라 설정 (해야 할 일)
- [ ] Supabase 프로젝트 생성 및 설정
- [ ] OpenAI API 키 발급
- [ ] Stripe 계정 및 상품 설정
- [ ] Stripe Webhook 설정

### ⏳ Phase 3: 데이터 엔지니어링 (해야 할 일)
- [ ] Word 템플릿 수집 및 변환
- [ ] 문서 필드 매핑 완성
- [ ] RAG 지식 베이스 확장

### ⏳ Phase 4: 테스트 및 배포 (해야 할 일)
- [ ] 로컬 테스트
- [ ] Streamlit Cloud 배포
- [ ] 최종 테스트

---

## 📌 Phase 2: 인프라 설정 상세 가이드

### Step 2.1: Supabase 설정

#### 2.1.1 프로젝트 생성
1. https://supabase.com 접속
2. "Start your project" 클릭
3. GitHub 계정으로 로그인
4. "New project" 클릭
5. 프로젝트 정보 입력:
   - Name: `kstay`
   - Database Password: (안전한 비밀번호 설정)
   - Region: Northeast Asia (Seoul) 선택
6. "Create new project" 클릭 (2-3분 소요)

#### 2.1.2 데이터베이스 스키마 생성
1. 좌측 메뉴에서 "SQL Editor" 클릭
2. "New query" 클릭
3. `database/schema.sql` 파일 내용 전체 복사하여 붙여넣기
4. "Run" 클릭
5. 성공 메시지 확인

#### 2.1.3 API 키 확인
1. 좌측 메뉴에서 "Project Settings" (톱니바퀴) 클릭
2. "API" 탭 클릭
3. 다음 값들을 복사해 둠:
   - Project URL: `https://xxxxx.supabase.co`
   - anon public key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

#### 2.1.4 Storage 버킷 생성 (선택사항)
1. 좌측 메뉴에서 "Storage" 클릭
2. "Create a new bucket" 클릭
3. Name: `documents`
4. Public bucket: Off
5. "Create bucket" 클릭

---

### Step 2.2: OpenAI API 설정

#### 2.2.1 API 키 발급
1. https://platform.openai.com 접속
2. 로그인 또는 계정 생성
3. 우측 상단 프로필 > "View API keys"
4. "Create new secret key" 클릭
5. Name: `kstay-production`
6. 생성된 키 복사 (다시 볼 수 없으므로 안전하게 저장)

#### 2.2.2 사용량 제한 설정 (권장)
1. "Settings" > "Limits" 이동
2. Monthly spending limit 설정 (예: $50)
3. 알림 이메일 설정

---

### Step 2.3: Stripe 결제 설정

#### 2.3.1 계정 생성
1. https://dashboard.stripe.com 접속
2. 계정 생성 또는 로그인
3. 테스트 모드 확인 (우측 상단 "Test mode" 토글)

#### 2.3.2 상품 생성
1. "Products" 메뉴 클릭
2. "+ Add product" 클릭
3. 정보 입력:
   - Name: `K-Stay Premium`
   - Description: `출입국 민원 서류 자동 생성 서비스`
   - Pricing: One time - $9.99
4. "Save product" 클릭
5. 생성된 Price ID 복사 (예: `price_1234567890`)

#### 2.3.3 API 키 확인
1. "Developers" > "API keys" 이동
2. Secret key 확인 (테스트 키: `sk_test_...`)
3. 복사해 둠

#### 2.3.4 Webhook 설정 (중요!)
Streamlit은 Webhook을 직접 받을 수 없으므로, 다음 중 하나를 선택:

**옵션 A: Supabase Edge Functions 사용**
1. Supabase 프로젝트에서 "Edge Functions" 생성
2. Stripe webhook 이벤트를 받아 DB 업데이트

**옵션 B: 별도 서버 운영**
1. FastAPI/Flask 서버를 별도로 배포
2. Stripe webhook 엔드포인트 구현

**옵션 C: 개발용 단순화 (테스트용)**
1. 결제 성공 시 URL 파라미터로 확인
2. 프로덕션에서는 보안상 권장하지 않음

Webhook 엔드포인트 예시 (Supabase Edge Function):
```javascript
// supabase/functions/stripe-webhook/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import Stripe from 'https://esm.sh/stripe@11.1.0?target=deno'

const stripe = new Stripe(Deno.env.get('STRIPE_API_KEY'), {
  apiVersion: '2022-11-15',
})

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()
  
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    Deno.env.get('STRIPE_WEBHOOK_SECRET')
  )
  
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object
    const userId = session.metadata.user_id
    
    // Supabase에서 사용자 결제 상태 업데이트
    // ...
  }
  
  return new Response(JSON.stringify({ received: true }))
})
```

---

## 📌 Phase 3: 데이터 엔지니어링 상세 가이드

### Step 3.1: Word 템플릿 수집

#### 3.1.1 하이코리아에서 서식 다운로드
1. https://www.hikorea.go.kr 접속
2. "민원안내/신청" 메뉴
3. 각 민원 유형별 서식 다운로드:
   - 통합신청서 (별지 제34호)
   - 구직활동계획서
   - 결혼배경 진술서
   - 고용활용계획서
   - 기타 필요 서식

#### 3.1.2 HWP → DOCX 변환
한글 파일(.hwp)은 python-docx로 처리할 수 없으므로 변환 필요:

**방법 1: 한글 프로그램 사용**
1. 한컴오피스 한글에서 파일 열기
2. "다른 이름으로 저장" > MS Word 문서 (.docx) 선택

**방법 2: 온라인 변환**
- https://smallpdf.com/hwp-to-word
- https://www.zamzar.com/convert/hwp-to-docx/

**방법 3: LibreOffice 사용 (무료)**
```bash
libreoffice --headless --convert-to docx *.hwp
```

#### 3.1.3 템플릿 구조 분석
각 문서에 대해 다음을 분석:
1. 테이블 구조 (행, 열)
2. 각 셀의 라벨 텍스트
3. 입력해야 할 필드 위치
4. 체크박스/선택 영역

예시 분석 결과:
```python
# 통합신청서 구조
{
    "table_0": {  # 인적사항 테이블
        "row_0": ["성명(한글)", "입력칸", "성명(영문)", "입력칸"],
        "row_1": ["성별", "□남 □여", "생년월일", "입력칸"],
        # ...
    },
    "table_1": {  # 여권정보 테이블
        # ...
    }
}
```

### Step 3.2: 문서 매핑 정의

`templates/mapping_guide.py`를 기반으로 각 문서의 매핑을 완성:

```python
# 예시: 통합신청서 매핑 상세화
UNIFIED_APPLICATION_DETAIL = {
    "template_file": "templates/unified_application.docx",
    "tables": [
        {
            "index": 0,  # 첫 번째 테이블
            "mappings": [
                {
                    "row": 0, "col": 1,  # (0행, 1열)
                    "field_type": "text",
                    "data_source": "user_data.name_korean",
                    "label": "성명(한글)"
                },
                {
                    "row": 0, "col": 3,
                    "field_type": "text",
                    "data_source": ["user_data.surname", " ", "user_data.given_name"],
                    "label": "성명(영문)"
                },
                {
                    "row": 1, "col": 1,
                    "field_type": "checkbox",
                    "data_source": "user_data.gender",
                    "options": {"Male": "☑남 □여", "Female": "□남 ☑여"},
                    "label": "성별"
                },
                # ... 모든 필드 매핑
            ]
        }
    ]
}
```

### Step 3.3: RAG 지식 베이스 확장

#### 3.3.1 데이터 수집
다음 소스에서 정보 수집:
1. **하이코리아 공식 가이드**
   - 각 비자 유형별 안내 페이지
   - FAQ 섹션
   - 민원 처리 안내

2. **출입국관리법령**
   - 법률, 시행령, 시행규칙
   - 조문별 분리 저장

3. **실제 사례 (익명화)**
   - 성공 사례의 패턴
   - 거절 사유 분석

#### 3.3.2 데이터 청킹 및 임베딩
```python
# RAG 데이터 처리 예시
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

# 텍스트 청킹
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(document_text)

# 임베딩 생성
client = OpenAI()

for chunk in chunks:
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    
    # Supabase에 저장
    supabase.table('rag_documents').insert({
        'content': chunk,
        'embedding': embedding.data[0].embedding,
        'source': 'hikorea_guide',
        'category': 'visa_d10'
    }).execute()
```

---

## 📌 Phase 4: 테스트 및 배포

### Step 4.1: 로컬 테스트

```bash
# 1. 가상환경 활성화
source venv/bin/activate

# 2. secrets.toml 설정 확인
cat .streamlit/secrets.toml

# 3. 앱 실행
streamlit run app.py

# 4. 브라우저에서 테스트
# http://localhost:8501
```

테스트 체크리스트:
- [ ] 회원가입 플로우
- [ ] 로그인/로그아웃
- [ ] 각 시나리오 폼 입력
- [ ] AI 검증 기능
- [ ] 문서 생성 및 다운로드
- [ ] AI 채팅

### Step 4.2: Streamlit Cloud 배포

1. **GitHub에 코드 푸시**
```bash
git init
git add .
git commit -m "Initial K-Stay commit"
git remote add origin https://github.com/your-username/kstay.git
git push -u origin main
```

2. **Streamlit Cloud 설정**
   - https://share.streamlit.io 접속
   - "New app" 클릭
   - GitHub 저장소 선택
   - Branch: `main`
   - Main file path: `app.py`

3. **Secrets 설정**
   - "Advanced settings" 클릭
   - Secrets 영역에 `.streamlit/secrets.toml` 내용 붙여넣기

4. **Deploy!**

### Step 4.3: 프로덕션 체크리스트

- [ ] HTTPS 활성화 (Streamlit Cloud 자동)
- [ ] Stripe 라이브 모드 전환
- [ ] 에러 모니터링 설정
- [ ] 백업 정책 수립
- [ ] 개인정보처리방침 페이지 추가
- [ ] 이용약관 페이지 추가

---

## 🔧 문제 해결

### 자주 발생하는 문제

**1. Supabase 연결 실패**
```
Error: Invalid API key
```
해결: secrets.toml의 SUPABASE_KEY가 올바른지 확인

**2. OpenAI 할당량 초과**
```
Error: Rate limit exceeded
```
해결: 사용량 확인 및 요금제 업그레이드

**3. 문서 생성 실패**
```
Error: Template not found
```
해결: templates/ 폴더에 해당 .docx 파일 존재 확인

**4. Stripe 결제 실패**
```
Error: Invalid price ID
```
해결: STRIPE_PRICE_ID가 올바른지 확인

---

## 📞 지원

문제 발생 시:
1. GitHub Issues에 등록
2. 에러 메시지와 재현 단계 포함
3. 스크린샷 첨부 권장

---

**행운을 빕니다! 🍀**
