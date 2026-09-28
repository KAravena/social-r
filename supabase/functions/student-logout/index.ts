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

    if (auth) {
      await adminClient.from("student_sessions").delete().eq("session_id", auth.sessionId);
      await adminClient.from("activity_events").insert({
        student_id: auth.studentId,
        course_id: "intro-r",
        event_type: "logout",
      });
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    console.error("[student-logout] Error:", err);
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
