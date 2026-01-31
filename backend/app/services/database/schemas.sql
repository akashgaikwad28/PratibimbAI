-- SQL for creating the jobs table in Supabase dashboard

CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY,
    status TEXT NOT NULL,
    topic TEXT,
    urls JSONB,
    tone TEXT,
    style TEXT,
    platform TEXT,
    num_posts INTEGER,
    final_posts JSONB,
    errors JSONB DEFAULT '[]'::jsonb,
    llm_provider TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Optional: Enable row level security (RLS) if needed, 
-- but for now we'll keep it simple for service-role access.
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- Policy to allow service-role access (bypass RLS for the backend)
CREATE POLICY "Enable all for service role" ON jobs
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');
