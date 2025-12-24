-- =============================================================================
-- K-Stay Database Schema for Supabase
-- =============================================================================
-- Run this SQL in your Supabase SQL Editor to create the necessary tables

-- =============================================================================
-- 1. USERS TABLE (사용자 정보 - Universal Fact)
-- =============================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- 인적사항 (Personal Info)
    surname VARCHAR(100),
    given_name VARCHAR(100),
    birth_date DATE,
    gender VARCHAR(20), -- 'Male', 'Female'
    nationality VARCHAR(100),
    alien_registration_no VARCHAR(50), -- 외국인등록번호
    
    -- 여권정보 (Passport Info)
    passport_no VARCHAR(50),
    passport_issue_date DATE,
    passport_expiry_date DATE,
    
    -- 연락처 (Contact Info)
    korea_address TEXT,
    korea_phone VARCHAR(30),
    home_country_address TEXT,
    home_country_phone VARCHAR(50),
    
    -- 결제 및 권한 (Payment & Auth)
    is_paid BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    paid_at TIMESTAMPTZ,
    
    -- 메타데이터
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS (Row Level Security) 활성화
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 사용자 본인만 자신의 데이터 접근 가능
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (auth.uid() = id);


-- =============================================================================
-- 2. PAYMENTS TABLE (결제 기록)
-- =============================================================================
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    stripe_session_id VARCHAR(255),
    stripe_payment_intent VARCHAR(255),
    
    amount DECIMAL(10, 2),
    currency VARCHAR(10) DEFAULT 'usd',
    status VARCHAR(50), -- 'pending', 'succeeded', 'failed', 'refunded'
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own payments" ON payments
    FOR SELECT USING (auth.uid() = user_id);


-- =============================================================================
-- 3. SCENARIOS TABLE (시나리오 실행 기록)
-- =============================================================================
CREATE TABLE IF NOT EXISTS scenario_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    scenario_id VARCHAR(10) NOT NULL, -- 'A', 'B', 'C', 'D', 'E', 'F'
    scenario_name VARCHAR(100),
    visa_type VARCHAR(50),
    
    -- Variable Fact Data (JSONB for flexibility)
    form_data JSONB DEFAULT '{}',
    
    -- Narrative Data
    narrative_data JSONB DEFAULT '{}',
    
    -- AI Feedback
    ai_feedback JSONB DEFAULT '{}',
    
    -- Status
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'completed', 'downloaded'
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

ALTER TABLE scenario_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own submissions" ON scenario_submissions
    FOR ALL USING (auth.uid() = user_id);


-- =============================================================================
-- 4. GENERATED_DOCUMENTS TABLE (생성된 문서 기록)
-- =============================================================================
CREATE TABLE IF NOT EXISTS generated_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    submission_id UUID REFERENCES scenario_submissions(id) ON DELETE CASCADE,
    
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(50), -- 'docx', 'pdf', 'zip'
    
    -- Storage reference (Supabase Storage)
    storage_path TEXT,
    file_size INTEGER,
    
    download_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE generated_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can access own documents" ON generated_documents
    FOR ALL USING (auth.uid() = user_id);


-- =============================================================================
-- 5. CHAT_HISTORY TABLE (AI 채팅 기록)
-- =============================================================================
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant'
    content TEXT NOT NULL,
    
    -- Optional: RAG context used
    rag_context TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own chat history" ON chat_history
    FOR ALL USING (auth.uid() = user_id);


-- =============================================================================
-- 6. RAG_DOCUMENTS TABLE (RAG 지식 베이스)
-- =============================================================================
CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    title VARCHAR(255) NOT NULL,
    source VARCHAR(255), -- '하이코리아', '출입국관리법', etc.
    category VARCHAR(100), -- 'visa_guide', 'law', 'form_guide', etc.
    
    content TEXT NOT NULL,
    
    -- Vector embedding (if using pgvector)
    -- embedding VECTOR(1536),
    
    metadata JSONB DEFAULT '{}',
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Public read access for RAG
ALTER TABLE rag_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read RAG documents" ON rag_documents
    FOR SELECT USING (is_active = TRUE);


-- =============================================================================
-- 7. INDEXES FOR PERFORMANCE
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON scenario_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_scenario ON scenario_submissions(scenario_id);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON generated_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_rag_category ON rag_documents(category);


-- =============================================================================
-- 8. FUNCTIONS & TRIGGERS
-- =============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_submissions_updated_at
    BEFORE UPDATE ON scenario_submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- =============================================================================
-- 9. INITIAL DATA (Optional)
-- =============================================================================

-- Insert sample RAG documents
INSERT INTO rag_documents (title, source, category, content, metadata) VALUES
(
    'D-10 구직비자 개요',
    '하이코리아',
    'visa_guide',
    'D-10 비자는 한국에서 구직 활동을 하려는 외국인에게 부여되는 체류자격입니다. 대학(전문대학 포함) 이상의 학위를 가진 자로서 국내에서 취업활동을 하려는 사람에게 발급됩니다. 체류기간은 최대 6개월이며, 1회에 한해 6개월 연장이 가능합니다.',
    '{"visa_type": "D-10", "duration": "6개월", "extendable": true}'
),
(
    'F-6 결혼이민 비자 요건',
    '하이코리아',
    'visa_guide',
    'F-6 비자는 한국인과 결혼한 외국인에게 부여되는 체류자격입니다. 신청 요건으로는 유효한 혼인관계 증명, 한국어 기본 소통 능력 또는 결혼이민자 사전교육 이수, 그리고 배우자의 소득 요건 충족이 있습니다.',
    '{"visa_type": "F-6", "category": "결혼이민"}'
),
(
    '시간제 취업 허가 조건',
    '하이코리아',
    'work_permit',
    '유학생(D-2)과 연수생(D-4)은 입국 후 6개월 경과 후 시간제 취업이 가능합니다. 학기 중에는 주 20시간 이내, 방학 중에는 무제한 근무가 가능합니다. 단, 유흥업소 등 금지 업종에서는 취업이 불가합니다.',
    '{"visa_types": ["D-2", "D-4"], "weekly_limit": 20}'
);


-- =============================================================================
-- END OF SCHEMA
-- =============================================================================
