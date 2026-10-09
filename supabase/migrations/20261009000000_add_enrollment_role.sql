-- ==============================================================================
-- Social R — Enrollment Role & Teacher Admin Access Migration
-- Version: 2026.10.1
-- Purpose: Add authoritative role-based authorization to course enrollments,
--          elevating administrator accounts while preserving zero-trust security.
-- ==============================================================================

-- 1. Add role column to public.enrollments
ALTER TABLE public.enrollments
ADD COLUMN IF NOT EXISTS role TEXT NOT NULL DEFAULT 'student'
CONSTRAINT chk_enrollment_role CHECK (role IN ('student', 'admin'));

-- 2. Index on role
CREATE INDEX IF NOT EXISTS idx_enrollments_role ON public.enrollments(role);

-- 3. Elevate existing TEST-ADMIN accounts to role = 'admin'
UPDATE public.enrollments
SET role = 'admin'
WHERE section = 'TEST-ADMIN';

-- 4. Recreate teacher_progress_summary view with role
DROP VIEW IF EXISTS public.teacher_progress_summary CASCADE;

CREATE VIEW public.teacher_progress_summary AS
SELECT
    s.student_id,
    s.rut_lookup,
    s.rut_masked,
    s.display_name,
    COALESCE(e.section, 'Sin sección') AS section,
    COALESCE(e.role, 'student') AS role,
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
GROUP BY s.student_id, s.rut_lookup, s.rut_masked, s.display_name, e.section, e.role, c.course_id, c.published_exercises, c.total_exercises;

-- 5. Grant SELECT on updated view to service_role
GRANT SELECT ON public.teacher_progress_summary TO service_role;
