-- ============================================================================
-- K-Stay: user_documents 테이블 스키마
-- Supabase SQL Editor에서 실행하세요
-- ============================================================================

-- 기존 테이블 삭제 (필요시)
-- DROP TABLE IF EXISTS user_documents;

-- 1. user_documents 테이블 생성
CREATE TABLE IF NOT EXISTS user_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,  -- TEXT 타입으로 변경 (UUID 호환성 문제 방지)
    scenario_id VARCHAR(10) NOT NULL,
    scenario_name VARCHAR(100) NOT NULL,
    visa_type VARCHAR(50) NOT NULL,
    document_list JSONB NOT NULL DEFAULT '[]',
    file_data TEXT,  -- Base64 인코딩된 ZIP 파일
    file_size INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_user_documents_user_id ON user_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_user_documents_created_at ON user_documents(created_at DESC);

-- 3. RLS 비활성화 (개발 단계에서 간단하게 사용)
-- 주의: 프로덕션에서는 RLS 활성화 권장
ALTER TABLE user_documents DISABLE ROW LEVEL SECURITY;

-- 4. 모든 사용자에게 권한 부여 (anon, authenticated)
GRANT ALL ON user_documents TO anon;
GRANT ALL ON user_documents TO authenticated;

-- 5. updated_at 자동 업데이트 트리거
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_user_documents_updated_at ON user_documents;
CREATE TRIGGER update_user_documents_updated_at
    BEFORE UPDATE ON user_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 테스트: 테이블 확인
-- ============================================================================
-- SELECT * FROM user_documents LIMIT 10;
