import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { corsHeaders } from "../_shared/cors.ts";
import { getAdminClient, resolveStudentFromHeader } from "../_shared/db.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    if (req.method !== "POST") {
      return new Response(JSON.stringify({ error: "method_not_allowed" }), {
        status: 405,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const adminClient = getAdminClient();
    const auth = await resolveStudentFromHeader(req, adminClient);

    if (!auth) {
      return new Response(
        JSON.stringify({ error: "unauthorized", message: "Sesión inválida o expirada. Ingresa tu RUT nuevamente." }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { studentId } = auth;
    const body = await req.json().catch(() => ({}));
    const courseId = body.courseId || "intro-r";
    const nowIso = new Date().toISOString();

    // 1. Monotonic Exercise Progress Sync
    if (Array.isArray(body.completedExercises) && body.completedExercises.length > 0) {
      const rows = body.completedExercises.map((exId: string) => ({
        course_id: courseId,
        student_id: studentId,
        exercise_id: exId,
        completed: true,
        completed_at: nowIso,
        updated_at: nowIso,
      }));

      // Upsert: on conflict, retain existing completed_at
      await adminClient
        .from("exercise_progress")
        .upsert(rows, { onConflict: "course_id,student_id,exercise_id", ignoreDuplicates: false });
    }

    // 2. Monotonic Challenge Progress Sync
    if (body.challenges && typeof body.challenges === "object") {
      for (const [moduleId, chData] of Object.entries(body.challenges as Record<string, any>)) {
        if (!chData || typeof chData !== "object") continue;
        const status = chData.status;
        const challengeId = chData.challengeId || `intro-r-${moduleId.substring(0, 2)}-challenge`;
        const passedAt = status === "passed" ? (chData.passedAt || nowIso) : null;

        // Check if existing record is already passed; monotonic rule: never downgrade passed!
        const { data: existing } = await adminClient
          .from("challenge_progress")
          .select("status, passed_at")
          .eq("student_id", studentId)
          .eq("course_id", courseId)
          .eq("module_id", moduleId)
          .maybeSingle();

        if (existing && existing.status === "passed" && status !== "passed") {
          continue; // Do not overwrite passed with pending/available
        }

        await adminClient.from("challenge_progress").upsert(
          {
            course_id: courseId,
            student_id: studentId,
            module_id: moduleId,
            challenge_id: challengeId,
            status: status || "available",
            passed_at: (existing && existing.passed_at) ? existing.passed_at : passedAt,
            updated_at: nowIso,
          },
          { onConflict: "course_id,student_id,module_id" }
        );

        if (status === "passed" && (!existing || existing.status !== "passed")) {
          // Log challenge pass event
          await adminClient.from("activity_events").insert({
            student_id: studentId,
            course_id: courseId,
            event_type: "challenge_passed",
            resource_id: challengeId,
            metadata: { module_id: moduleId },
          });
        }
      }
    }

    // 3. Exercise Drafts Sync (persist editor code)
    if (body.editorDrafts && typeof body.editorDrafts === "object") {
      const draftRows = [];
      for (const [exId, code] of Object.entries(body.editorDrafts as Record<string, any>)) {
        if (typeof code === "string" && code.trim().length > 0) {
          draftRows.push({
            course_id: courseId,
            student_id: studentId,
            exercise_id: exId,
            code: code,
            updated_at: nowIso,
          });
        }
      }

      if (draftRows.length > 0) {
        await adminClient
          .from("exercise_drafts")
          .upsert(draftRows, { onConflict: "course_id,student_id,exercise_id" });
      }
    }

    return new Response(
      JSON.stringify({
        success: true,
        syncedAt: nowIso,
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error("[student-progress-sync] Error:", err);
    return new Response(
      JSON.stringify({ error: "server_error", message: "Error al sincronizar el progreso." }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
