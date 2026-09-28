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
        JSON.stringify({ error: "unauthorized", message: "Sesión inválida o expirada." }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const { studentId } = auth;
    const body = await req.json().catch(() => ({}));
    const courseId = body.courseId || "intro-r";

    // Strictly reset only this student's progress in this course
    await adminClient.from("exercise_progress").delete().eq("student_id", studentId).eq("course_id", courseId);
    await adminClient.from("challenge_progress").delete().eq("student_id", studentId).eq("course_id", courseId);
    await adminClient.from("exercise_drafts").delete().eq("student_id", studentId).eq("course_id", courseId);

    await adminClient.from("activity_events").insert({
      student_id: studentId,
      course_id: courseId,
      event_type: "course_reset",
    });

    return new Response(JSON.stringify({ success: true, message: "Progreso reiniciado exitosamente." }), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("[student-reset] Error:", err);
    return new Response(
      JSON.stringify({ error: "server_error", message: "Error al reiniciar el progreso en la nube." }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
