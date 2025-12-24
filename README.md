# 🇰🇷 K-Stay: Korea Stay Assistant

외국인을 위한 출입국 민원 서류 자동 생성 플랫폼

![K-Stay Banner](https://via.placeholder.com/1200x400/0A1628/C9A227?text=K-Stay+Korea+Stay+Assistant)

## 📋 프로젝트 개요

K-Stay는 한국에 체류하는 외국인들이 출입국 관련 민원 서류를 쉽게 작성할 수 있도록 도와주는 AI 기반 플랫폼입니다.

### 핵심 기능
- 🔐 **3계층 데이터 구조**: 불변정보 / 가변정보 / AI 검토 정보 분리
- 📄 **6가지 시나리오**: D-10 구직, 시간제 취업, F-6 결혼이민, 가족초청, E-7 전문인력, 귀화
- 🤖 **AI 문서 검토**: 실시간 사연 검증 및 개선 제안
- 📦 **ZIP 패키지 생성**: 시나리오별 필수 서류 일괄 생성

---

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/kstay.git
cd kstay
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 환경 설정
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml 파일을 편집하여 API 키 입력
```

### 4. 실행
```bash
streamlit run app.py
```

---

## 📁 프로젝트 구조

```
kstay/
├── app.py                    # 메인 앱 엔트리 포인트
├── requirements.txt          # Python 의존성
├── .streamlit/
│   └── secrets.toml.example  # 시크릿 템플릿
│
├── config/
│   ├── __init__.py
│   └── settings.py           # 설정 및 시나리오 정의
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py       # 인증 서비스 (Supabase)
│   ├── payment_service.py    # 결제 서비스 (Stripe)
│   ├── ai_service.py         # AI 서비스 (OpenAI)
│   └── document_service.py   # 문서 생성 서비스
│
├── pages/
│   ├── __init__.py
│   ├── login.py              # 로그인 페이지
│   ├── signup.py             # 회원가입 (Universal Fact)
│   ├── main_dashboard.py     # 메인 대시보드
│   ├── scenario_form.py      # 시나리오 폼 (Variable + Narrative)
│   ├── ai_chat.py            # AI 상담사
│   └── document_preview.py   # 문서 미리보기/다운로드
│
├── database/
│   └── schema.sql            # Supabase DB 스키마
│
├── templates/
│   └── mapping_guide.py      # 문서 매핑 가이드
│
└── rag_data/
    └── knowledge_base.py     # RAG 지식 베이스
```

---

## ⚙️ 설정 가이드

### Step 1: Supabase 설정

1. [Supabase](https://supabase.com)에서 새 프로젝트 생성
2. SQL Editor에서 `database/schema.sql` 실행
3. Project Settings > API에서 URL과 anon key 복사
4. `.streamlit/secrets.toml`에 입력:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

### Step 2: OpenAI API 설정

1. [OpenAI Platform](https://platform.openai.com)에서 API 키 생성
2. `.streamlit/secrets.toml`에 입력:
```toml
OPENAI_API_KEY = "sk-your-api-key"
```

### Step 3: Stripe 결제 설정

1. [Stripe Dashboard](https://dashboard.stripe.com)에서 계정 생성
2. Products > Add Product로 $9.99 상품 생성
3. API Keys에서 Secret Key 복사
4. `.streamlit/secrets.toml`에 입력:
```toml
STRIPE_API_KEY = "sk_test_your-key"
STRIPE_PRICE_ID = "price_your-price-id"
STRIPE_SUCCESS_URL = "https://your-app.streamlit.app/?payment=success"
STRIPE_CANCEL_URL = "https://your-app.streamlit.app/?payment=cancel"
```

### Step 4: Word 템플릿 준비

1. [하이코리아](https://www.hikorea.go.kr)에서 공식 서식 다운로드
2. `.hwp` 파일을 `.docx`로 변환
3. `templates/` 폴더에 저장
4. `templates/mapping_guide.py` 참조하여 매핑 정의

---

## 📝 시나리오 목록

| ID | 시나리오 | 비자 유형 | 생성 문서 |
|----|---------|----------|----------|
| A | 구직 준비 | D-10 | 통합신청서, 구직활동계획서, 거주숙소제공확인서 등 |
| B | 아르바이트 | 시간제취업 | 시간제취업확인서, 표준근로계약서 등 |
| C | 결혼 이민 | F-6 | 통합신청서, 결혼배경진술서, 배우자초청장 등 |
| D | 가족 초청 | F-1-5 | 가족초청장, 신원보증서, 불법취업방지서약서 등 |
| E | 전문 인력 | E-7 | 사증발급인정신청서, 고용활용계획서 등 |
| F | 국적 귀화 | 귀화 | 귀화허가신청서, 귀화동기서 등 |

---

## 🔧 개발 모드

개발 중에는 실제 API 연동 없이 목업 데이터로 테스트할 수 있습니다.

```python
# services/auth_service.py 등에서
# 실제 코드는 주석 처리되어 있고
# 개발용 목업 코드가 활성화되어 있습니다.
```

배포 시:
1. 각 서비스 파일에서 실제 API 연동 코드의 주석 해제
2. 개발용 목업 코드 주석 처리 또는 삭제

---

## 🚢 배포 (Streamlit Cloud)

1. GitHub에 코드 푸시
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 새 앱 배포
3. Settings > Secrets에 모든 API 키 입력
4. Reboot 후 확인

---

## 📊 데이터 3계층 구조

### Layer 1: Universal Fact (불변 정보)
- 회원가입 시 1회 입력
- 성명, 생년월일, 여권번호 등
- AI 개입 ❌

### Layer 2: Variable Fact (가변 정보)
- 시나리오별 폼 입력
- 근무처, 학교, 소득 등
- AI 개입 ❌

### Layer 3: Narrative (사연 정보)
- AI가 적극적으로 검토
- 구직계획, 결혼배경, 귀화동기 등
- AI 개입 ✅ (검증 + 제안 + 생성)

---

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 라이선스

This project is licensed under the MIT License.

---

## 📞 문의

- 프로젝트 이슈: GitHub Issues
- 출입국 관련 공식 문의: 1345 (하이코리아)

---

**Made with ❤️ for foreigners in Korea**
