-- ==============================================================================
-- Social R — Service Role Data API Grants Migration
-- Version: 2026.03.2
-- Purpose: Grant explicit minimal DML privileges to service_role on public schema
--          objects required by Edge Functions and teacher administration scripts.
--
-- Security rules:
-- 1. NO privileges granted to anon or authenticated.
-- 2. RLS remains fully enabled on all tables.
-- 3. Only the exact operations used by backend tools are granted.
-- ==============================================================================

-- 1. Schema access
GRANT USAGE ON SCHEMA public TO service_role;

-- 2. Catalog / Reference Tables
-- courses: Read-only access for FK checks, seed verification, and view aggregation.
GRANT SELECT ON TABLE public.courses TO service_role;

-- 3. Student Identity & Enrollment (Teacher Importer & Student Login)
-- students: SELECT (login lookup), INSERT/UPDATE (roster upsert). No DELETE.
GRANT SELECT, INSERT, UPDATE ON TABLE public.students TO service_role;

-- enrollments: SELECT (login verification), INSERT/UPDATE (roster enrollment upsert). No DELETE.
GRANT SELECT, INSERT, UPDATE ON TABLE public.enrollments TO service_role;

-- 4. Session Management (db.ts, student-login, student-logout)
-- student_sessions: SELECT (auth verification), INSERT (login), UPDATE (last_used_at), DELETE (logout).
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.student_sessions TO service_role;

-- 5. Student Progress & Drafts (student-progress-get, student-progress-sync, student-reset)
-- exercise_progress: SELECT (get), INSERT/UPDATE (sync upsert), DELETE (course reset).
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.exercise_progress TO service_role;

-- challenge_progress: SELECT (get/monotonic check), INSERT/UPDATE (sync upsert), DELETE (course reset).
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.challenge_progress TO service_role;

-- exercise_drafts: SELECT (get), INSERT/UPDATE (sync upsert), DELETE (course reset).
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.exercise_drafts TO service_role;

-- 6. Activity Events Audit Log (student-login, student-logout, student-progress-sync, student-reset)
-- activity_events: SELECT (view aggregation), INSERT (event logging). No UPDATE or DELETE (immutable log).
GRANT SELECT, INSERT ON TABLE public.activity_events TO service_role;

-- 7. Teacher Analytics View (export_student_progress.py)
GRANT SELECT ON public.teacher_progress_summary TO service_role;
