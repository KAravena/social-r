-- ==============================================================================
-- Social R — Cloud Progress Schema Migration
-- Version: 2026.03.1
-- Architecture: Supabase / PostgreSQL
-- ==============================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ------------------------------------------------------------------------------
-- 1. COURSES TABLE
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.courses (
    course_id TEXT PRIMARY KEY,
    slug TEXT NOT NULL,
    name TEXT NOT NULL,
    year INTEGER NOT NULL DEFAULT 2026,
    active BOOLEAN NOT NULL DEFAULT true,
    published_exercises INTEGER NOT NULL DEFAULT 36,
    total_exercises INTEGER NOT NULL DEFAULT 89,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- Seed current course: intro-r
INSERT INTO public.courses (course_id, slug, name, year, active, published_exercises, total_exercises)
VALUES ('intro-r', 'intro-r', 'Introducción a R para Ciencias Sociales', 2026, true, 36, 89)
ON CONFLICT (course_id) DO UPDATE
SET name = EXCLUDED.name,
    published_exercises = EXCLUDED.published_exercises,
    total_exercises = EXCLUDED.total_exercises;

-- ------------------------------------------------------------------------------
-- 2. STUDENTS TABLE (Privacy-First: Plaintext RUT is NEVER stored in cloud)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.students (
    student_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rut_lookup TEXT UNIQUE NOT NULL, -- Deterministic HMAC-SHA256(secret, rut_normalized)
    rut_masked TEXT NOT NULL,         -- Discreet display: e.g. '••.•••.678-5'
    display_name TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_students_rut_lookup ON public.students(rut_lookup);

-- ------------------------------------------------------------------------------
-- 3. ENROLLMENTS TABLE
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.enrollments (
    enrollment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT NOT NULL REFERENCES public.courses(course_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    section TEXT DEFAULT '1',
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_enrollment_course_student UNIQUE (course_id, student_id)
);

CREATE INDEX IF NOT EXISTS idx_enrollments_course_student ON public.enrollments(course_id, student_id);

-- ------------------------------------------------------------------------------
-- 4. STUDENT SESSIONS (Token Hash Authentication)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.student_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL, -- SHA-256 hash of opaque client session token
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (timezone('utc'::text, now()) + interval '90 days'),
    last_used_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_student_sessions_token_hash ON public.student_sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_student_sessions_student_id ON public.student_sessions(student_id);

-- ------------------------------------------------------------------------------
-- 5. EXERCISE PROGRESS TABLE
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.exercise_progress (
    progress_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT NOT NULL REFERENCES public.courses(course_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    exercise_id TEXT NOT NULL, -- Canonical exercise ID: e.g. 'intro-r-01-001'
    completed BOOLEAN NOT NULL DEFAULT true,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_exercise_progress UNIQUE (course_id, student_id, exercise_id)
);

CREATE INDEX IF NOT EXISTS idx_exercise_progress_student ON public.exercise_progress(student_id, course_id);

-- ------------------------------------------------------------------------------
-- 6. CHALLENGE PROGRESS TABLE (Distinct from regular exercises)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.challenge_progress (
    challenge_progress_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT NOT NULL REFERENCES public.courses(course_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    module_id TEXT NOT NULL, -- e.g. '01-empezar-a-pensar-con-r'
    challenge_id TEXT NOT NULL, -- e.g. 'intro-r-01-challenge'
    status TEXT NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'pending', 'passed', 'failed')),
    passed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_challenge_progress UNIQUE (course_id, student_id, module_id)
);

CREATE INDEX IF NOT EXISTS idx_challenge_progress_student ON public.challenge_progress(student_id, course_id);

-- ------------------------------------------------------------------------------
-- 7. EXERCISE DRAFTS TABLE (Code persistence across devices)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.exercise_drafts (
    draft_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id TEXT NOT NULL REFERENCES public.courses(course_id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    exercise_id TEXT NOT NULL,
    code TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT uq_exercise_draft UNIQUE (course_id, student_id, exercise_id)
);

CREATE INDEX IF NOT EXISTS idx_exercise_drafts_student ON public.exercise_drafts(student_id, exercise_id);

-- ------------------------------------------------------------------------------
-- 8. ACTIVITY EVENTS TABLE (Minimal event logging for teaching trace)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.activity_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(student_id) ON DELETE CASCADE,
    course_id TEXT NOT NULL REFERENCES public.courses(course_id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (event_type IN ('login', 'logout', 'exercise_completed', 'challenge_passed', 'course_reset')),
    resource_id TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

CREATE INDEX IF NOT EXISTS idx_activity_events_student ON public.activity_events(student_id, created_at DESC);

-- ------------------------------------------------------------------------------
-- 9. TEACHER PROGRESS SUMMARY VIEW
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW public.teacher_progress_summary AS
SELECT
    s.student_id,
    s.rut_lookup,
    s.rut_masked,
    s.display_name,
    COALESCE(e.section, 'Sin sección') AS section,
    c.course_id,
    c.published_exercises,
    c.total_exercises,
    COUNT(DISTINCT ep.exercise_id) FILTER (WHERE ep.completed = true) AS completed_exercises,
    ROUND(
        (COUNT(DISTINCT ep.exercise_id) FILTER (WHERE ep.completed = true)::numeric / NULLIF(c.published_exercises, 0)::numeric) * 100,
        1
    ) AS exercise_percent,
    COUNT(DISTINCT cp.module_id) FILTER (WHERE cp.status = 'passed') AS passed_challenges,
    COUNT(DISTINCT cp.module_id) FILTER (WHERE cp.status = 'passed') AS accredited_modules,
    MIN(ae.created_at) FILTER (WHERE ae.event_type = 'login') AS first_login,
    GREATEST(
        MAX(ep.updated_at),
        MAX(cp.updated_at),
        MAX(ed.updated_at),
        MAX(ae.created_at)
    ) AS last_activity
FROM public.students s
JOIN public.enrollments e ON s.student_id = e.student_id AND e.active = true
JOIN public.courses c ON e.course_id = c.course_id
LEFT JOIN public.exercise_progress ep ON s.student_id = ep.student_id AND c.course_id = ep.course_id
LEFT JOIN public.challenge_progress cp ON s.student_id = cp.student_id AND c.course_id = cp.course_id
LEFT JOIN public.exercise_drafts ed ON s.student_id = ed.student_id AND c.course_id = ed.course_id
LEFT JOIN public.activity_events ae ON s.student_id = ae.student_id AND c.course_id = ae.course_id
WHERE s.active = true
GROUP BY s.student_id, s.rut_lookup, s.rut_masked, s.display_name, e.section, c.course_id, c.published_exercises, c.total_exercises;

-- ------------------------------------------------------------------------------
-- 10. ROW LEVEL SECURITY (RLS) POLICIES
-- ------------------------------------------------------------------------------
-- Direct anonymous access from frontend is completely disabled.
-- All operations run strictly through authenticated Supabase Edge Functions
-- which use the service_role key to enforce session-derived identity.
ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.challenge_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_events ENABLE ROW LEVEL SECURITY;

-- Allow public read of courses definition only
CREATE POLICY "Public courses read" ON public.courses
    FOR SELECT USING (active = true);
