-- 1. Create PROFILES table (Linked to Supabase Auth)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    profession TEXT,
    preferences JSONB DEFAULT '{
        "default_tone": "Professional",
        "default_style": "Concise",
        "default_platform": "LinkedIn"
    }'::jsonb,
    
    -- API Keys (Note: For absolute security, these should be encrypted, 
    -- but we store them here as per user requirement for the dashboard)
    openai_api_key TEXT,
    groq_api_key TEXT,
    gemini_api_key TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Update JOBS table to be User-Aware
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
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

-- 3. Trigger to automatically create a profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, avatar_url)
  VALUES (new.id, new.email, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 4. ENABLE RLS (Row Level Security)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- 5. Policies (Users can only see/edit their OWN data)
CREATE POLICY "Users can view their own profile" ON profiles 
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON profiles 
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view their own jobs" ON jobs 
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own jobs" ON jobs 
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 6. Monitored Sources Table
CREATE TABLE IF NOT EXISTS monitored_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
    url TEXT NOT NULL,
    source_type TEXT DEFAULT 'website', -- 'website', 'youtube', 'rss'
    poll_interval_hours INTEGER DEFAULT 6, -- 1 to 168 (1 week)
    last_polled_at TIMESTAMP WITH TIME ZONE,
    last_content_hash TEXT, -- To detect changes
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(user_id, url)
);

ALTER TABLE monitored_sources ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own sources" ON monitored_sources 
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage their own sources" ON monitored_sources 
    FOR ALL USING (auth.uid() = user_id);
