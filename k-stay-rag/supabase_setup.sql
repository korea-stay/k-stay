-- ============================================
-- K-Stay RAG 시스템용 Supabase 설정
-- Supabase SQL Editor에서 실행하세요
-- ============================================

-- 1. pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. 비자 문서 테이블 생성
CREATE TABLE IF NOT EXISTS visa_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1536),  -- OpenAI text-embedding-3-small 차원
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 인덱스 생성 (검색 성능 향상)
-- IVFFlat 인덱스 - 대용량 데이터에 적합
CREATE INDEX IF NOT EXISTS visa_documents_embedding_idx 
ON visa_documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- chunk_id 인덱스
CREATE INDEX IF NOT EXISTS visa_documents_chunk_id_idx 
ON visa_documents (chunk_id);

-- metadata GIN 인덱스 (JSONB 검색용)
CREATE INDEX IF NOT EXISTS visa_documents_metadata_idx 
ON visa_documents 
USING GIN (metadata);

-- 4. 유사도 검색 함수
CREATE OR REPLACE FUNCTION match_visa_documents (
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    chunk_id TEXT,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        visa_documents.id,
        visa_documents.chunk_id,
        visa_documents.content,
        visa_documents.metadata,
        1 - (visa_documents.embedding <=> query_embedding) AS similarity
    FROM visa_documents
    WHERE 1 - (visa_documents.embedding <=> query_embedding) > match_threshold
    ORDER BY visa_documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 5. 키워드 기반 검색 함수 (하이브리드 검색용)
CREATE OR REPLACE FUNCTION search_visa_documents_by_keyword (
    search_query TEXT,
    result_limit INT DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    chunk_id TEXT,
    content TEXT,
    metadata JSONB,
    rank FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        visa_documents.id,
        visa_documents.chunk_id,
        visa_documents.content,
        visa_documents.metadata,
        ts_rank(
            to_tsvector('simple', visa_documents.content),
            plainto_tsquery('simple', search_query)
        ) AS rank
    FROM visa_documents
    WHERE 
        to_tsvector('simple', visa_documents.content) @@ plainto_tsquery('simple', search_query)
        OR visa_documents.metadata->>'keywords' ILIKE '%' || search_query || '%'
    ORDER BY rank DESC
    LIMIT result_limit;
END;
$$;

-- 6. 업데이트 시간 자동 갱신 트리거
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER visa_documents_updated_at
    BEFORE UPDATE ON visa_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- 7. RLS (Row Level Security) 정책 - 필요시 활성화
-- ALTER TABLE visa_documents ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기 가능
-- CREATE POLICY "Allow public read" ON visa_documents
--     FOR SELECT USING (true);

-- 인증된 사용자만 쓰기 가능
-- CREATE POLICY "Allow authenticated write" ON visa_documents
--     FOR ALL USING (auth.role() = 'authenticated');

-- ============================================
-- 확인 쿼리
-- ============================================

-- 테이블 확인
-- SELECT * FROM visa_documents LIMIT 5;

-- 함수 테스트 (임베딩 있을 때)
-- SELECT * FROM match_visa_documents(
--     '[0.1, 0.2, ...]'::vector,  -- 실제 임베딩 벡터
--     0.5,
--     5
-- );
