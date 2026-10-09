import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { corsHeaders } from "../_shared/cors.ts";
import { validateRut, normalizeRut, formatRutMasked, computeRutLookup } from "../_shared/rut.ts";
import { getAdminClient, hashToken } from "../_shared/db.ts";

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    if (req.method !== "POST") {
      return new Response(JSON.stringify({ error: "method_not_allowed", message: "Método no permitido" }), {
        status: 405,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const body = await req.json().catch(() => ({}));
    const rawRut = body.rut;
    const courseId = body.courseId || "intro-r";

    if (!rawRut || typeof rawRut !== "string") {
      return new Response(
        JSON.stringify({ error: "validation_error", message: "Ingresa tu RUT o IPE para continuar." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 1. Modulo 11 check digit validation
    if (!validateRut(rawRut)) {
      return new Response(
        JSON.stringify({ error: "validation_error", message: "Revisa el RUT o IPE ingresado." }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const normalizedRut = normalizeRut(rawRut);

    const rutSecret = Deno.env.get("RUT_SECRET_KEY") || Deno.env.get("RUT_LOOKUP_SECRET");
    if (!rutSecret) {
      console.error("[student-login] Error: Missing RUT_SECRET_KEY / RUT_LOOKUP_SECRET in environment");
      return new Response(
        JSON.stringify({ error: "server_error", message: "Error de configuración de seguridad del servidor." }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const rutLookup = await computeRutLookup(normalizedRut, rutSecret);
    const adminClient = getAdminClient();

    // 2. Lookup student in roster using cryptographic HMAC hash
    const { data: student, error: studentError } = await adminClient
      .from("students")
      .select("student_id, rut_lookup, rut_masked, display_name, active")
      .eq("rut_lookup", rutLookup)
      .eq("active", true)
      .maybeSingle();

    if (studentError || !student) {
      return new Response(
        JSON.stringify({
          error: "roster_error",
          message: "No encontramos este RUT o IPE en la nómina del curso. Revisa que esté escrito correctamente.",
        }),
        { status: 404, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 3. Lookup active enrollment
    const { data: enrollment, error: enrollError } = await adminClient
      .from("enrollments")
      .select("enrollment_id, section, role, active, course_id")
      .eq("student_id", student.student_id)
      .eq("course_id", courseId)
      .eq("active", true)
      .maybeSingle();

    if (enrollError || !enrollment) {
      return new Response(
        JSON.stringify({
          error: "roster_error",
          message: "El estudiante no está matriculado en este curso activo.",
        }),
        { status: 403, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const userRole = (enrollment.role as string) || "student";
    const isAdmin = userRole === "admin";

    // 4. Generate opaque session token & store its SHA-256 hash
    const rawToken = `${crypto.randomUUID()}.${crypto.randomUUID()}.${Date.now()}`;
    const tokenHash = await hashToken(rawToken);

    const expiresAt = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString(); // 90 days

    const { error: sessionError } = await adminClient.from("student_sessions").insert({
      student_id: student.student_id,
      token_hash: tokenHash,
      expires_at: expiresAt,
      last_used_at: new Date().toISOString(),
    });

    if (sessionError) {
      console.error("[student-login] Session creation error:", sessionError);
      return new Response(
        JSON.stringify({ error: "server_error", message: "Error temporal al iniciar sesión. Intenta de nuevo." }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 5. Minimal activity logging
    await adminClient.from("activity_events").insert({
      student_id: student.student_id,
      course_id: courseId,
      event_type: "login",
      resource_id: null,
      metadata: { section: enrollment.section, role: userRole },
    });

    // 6. Return session & identity (RUT is masked for privacy)
    return new Response(
      JSON.stringify({
        sessionToken: rawToken,
        expiresAt,
        student: {
          id: student.student_id,
          displayName: student.display_name,
          rutMasked: student.rut_masked || formatRutMasked(normalizedRut),
          section: enrollment.section,
          role: userRole,
          isAdmin: isAdmin,
        },
        course: {
          courseId: courseId,
        },
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error("[student-login] Uncaught exception:", err);
    return new Response(
      JSON.stringify({ error: "server_error", message: "Ocurrió un error inesperado. Intenta nuevamente." }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
