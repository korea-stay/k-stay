-- =============================================================================
-- K-Stay Supabase 초기 설정 (회원가입용)
-- Supabase SQL Editor에서 실행하세요
-- =============================================================================

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
    gender VARCHAR(20),
    nationality VARCHAR(100),
    alien_registration_no VARCHAR(50),
    
    -- 여권정보 (Passport Info)
    passport_no VARCHAR(50),
    passport_issue_date DATE,
    passport_expiry_date DATE,
    
    -- 연락처 (Contact Info)
    korea_address TEXT,
    korea_phone VARCHAR(30),
    home_country_address TEXT,
    home_country_phone VARCHAR(50),
    
    -- 결제 및 권한
    is_paid BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    paid_at TIMESTAMPTZ,
    
    -- 메타데이터
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================================================
-- 2. RLS (Row Level Security) 설정
-- =============================================================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 사용자 본인만 자신의 데이터 조회 가능
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

-- 사용자 본인만 자신의 데이터 수정 가능
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

-- 사용자 본인만 자신의 데이터 삽입 가능
CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- =============================================================================
-- 3. 자동 updated_at 갱신 트리거
-- =============================================================================
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

-- =============================================================================
-- 4. 인덱스
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- =============================================================================
-- 완료! 이제 프로젝트에서 Supabase 연결 설정을 하세요.
-- =============================================================================
