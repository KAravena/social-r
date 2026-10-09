import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { corsHeaders } from "../_shared/cors.ts";
import { getAdminClient, resolveStudentFromHeader } from "../_shared/db.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const adminClient = getAdminClient();
    const auth = await resolveStudentFromHeader(req, adminClient);

    if (!auth) {
      return new Response(
        JSON.stringify({ error: "unauthorized", message: "Sesión inválida o expirada. Ingresa tu RUT nuevamente." }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { studentId } = auth;
    const url = new URL(req.url);
    const courseId = url.searchParams.get("courseId") || "intro-r";

    // 1. Fetch completed exercises
    const { data: exercises, error: exError } = await adminClient
      .from("exercise_progress")
      .select("exercise_id, completed, completed_at")
      .eq("student_id", studentId)
      .eq("course_id", courseId)
      .eq("completed", true);

    if (exError) throw exError;

    const completedExercises = (exercises || []).map((e) => e.exercise_id);

    // 2. Fetch challenge statuses
    const { data: challenges, error: chError } = await adminClient
      .from("challenge_progress")
      .select("module_id, challenge_id, status, passed_at")
      .eq("student_id", studentId)
      .eq("course_id", courseId);

    if (chError) throw chError;

    const challengeMap: Record<string, { status: string; passedAt: string | null }> = {};
    (challenges || []).forEach((c) => {
      challengeMap[c.module_id] = {
        status: c.status,
        passedAt: c.passed_at,
      };
    });

    // 3. Fetch exercise drafts (editor code)
    const { data: drafts, error: draftError } = await adminClient
      .from("exercise_drafts")
      .select("exercise_id, code, updated_at")
      .eq("student_id", studentId)
      .eq("course_id", courseId);

    if (draftError) throw draftError;

    const editorState: Record<string, string> = {};
    (drafts || []).forEach((d) => {
      if (d.code) editorState[d.exercise_id] = d.code;
    });

    // 4. Fetch active enrollment to return server-authoritative role & identity
    const { data: enrollment } = await adminClient
      .from("enrollments")
      .select("enrollment_id, section, role, active")
      .eq("student_id", studentId)
      .eq("course_id", courseId)
      .eq("active", true)
      .maybeSingle();

    const userRole = (enrollment && (enrollment.role as string)) || "student";
    const isAdmin = userRole === "admin";

    return new Response(
      JSON.stringify({
        completedExercises,
        challenges: challengeMap,
        editorState,
        syncedAt: new Date().toISOString(),
        student: {
          role: userRole,
          isAdmin: isAdmin,
          section: enrollment ? enrollment.section : null,
        },
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error("[student-progress-get] Error:", err);
    return new Response(
      JSON.stringify({ error: "server_error", message: "Error al recuperar el progreso." }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
