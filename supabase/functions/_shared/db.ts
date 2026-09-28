import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.8";

/**
 * Resolves the Supabase Secret Key for elevated administrative database access.
 * Follows modern Supabase API key architecture (sb_secret_...) with fallback to legacy.
 *
 * Checks in order:
 * 1. SUPABASE_SECRET_KEY (modern direct environment variable)
 * 2. SUPABASE_SECRET_KEYS JSON string (modern runtime dictionary, e.g. {"default": "sb_secret_..."})
 * 3. SUPABASE_SERVICE_ROLE_KEY (legacy fallback)
 */
export function getSecretKey(): string {
  const direct = Deno.env.get("SUPABASE_SECRET_KEY");
  if (direct && direct.trim()) {
    return direct.trim();
  }

  const keysJson = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (keysJson) {
    try {
      const parsed = JSON.parse(keysJson);
      if (parsed && typeof parsed.default === "string" && parsed.default.trim()) {
        return parsed.default.trim();
      }
      if (parsed && typeof parsed === "object") {
        const first = Object.values(parsed)[0];
        if (typeof first === "string" && first.trim()) {
          return first.trim();
        }
      }
    } catch {
      // Fall through if not valid JSON
    }
  }

  const legacy = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (legacy && legacy.trim()) {
    return legacy.trim();
  }

  return "";
}

/**
 * Resolves the Supabase Publishable Key for public API access.
 * Follows modern Supabase API key architecture (sb_publishable_...) with fallback to legacy.
 *
 * Checks in order:
 * 1. SUPABASE_PUBLISHABLE_KEY (modern direct environment variable)
 * 2. SUPABASE_PUBLISHABLE_KEYS JSON string (modern runtime dictionary, e.g. {"default": "sb_publishable_..."})
 * 3. SUPABASE_ANON_KEY (legacy fallback)
 */
export function getPublishableKey(): string {
  const direct = Deno.env.get("SUPABASE_PUBLISHABLE_KEY");
  if (direct && direct.trim()) {
    return direct.trim();
  }

  const keysJson = Deno.env.get("SUPABASE_PUBLISHABLE_KEYS");
  if (keysJson) {
    try {
      const parsed = JSON.parse(keysJson);
      if (parsed && typeof parsed.default === "string" && parsed.default.trim()) {
        return parsed.default.trim();
      }
      if (parsed && typeof parsed === "object") {
        const first = Object.values(parsed)[0];
        if (typeof first === "string" && first.trim()) {
          return first.trim();
        }
      }
    } catch {
      // Fall through if not valid JSON
    }
  }

  const legacy = Deno.env.get("SUPABASE_ANON_KEY");
  if (legacy && legacy.trim()) {
    return legacy.trim();
  }

  return "";
}

export function getAdminClient() {
  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const secretKey = getSecretKey();

  if (!supabaseUrl || !secretKey) {
    throw new Error("Missing SUPABASE_URL or SUPABASE_SECRET_KEY in environment");
  }

  return createClient(supabaseUrl, secretKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  });
}

/**
 * Computes SHA-256 hex hash of an opaque string token.
 */
export async function hashToken(token: string): Promise<string> {
  const data = new TextEncoder().encode(token);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

/**
 * Resolves student_id from an Authorization: Bearer <sessionToken> header.
 * Derives identity strictly server-side.
 */
export async function resolveStudentFromHeader(
  req: Request,
  adminClient: ReturnType<typeof getAdminClient>
): Promise<{ studentId: string; sessionId: string } | null> {
  const authHeader = req.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return null;
  }

  const token = authHeader.replace("Bearer ", "").trim();
  if (!token) return null;

  const tokenHash = await hashToken(token);

  const { data: session, error } = await adminClient
    .from("student_sessions")
    .select("session_id, student_id, expires_at")
    .eq("token_hash", tokenHash)
    .gt("expires_at", new Date().toISOString())
    .maybeSingle();

  if (error || !session) {
    return null;
  }

  // Update last_used_at in background
  adminClient
    .from("student_sessions")
    .update({ last_used_at: new Date().toISOString() })
    .eq("session_id", session.session_id)
    .then();

  return {
    studentId: session.student_id,
    sessionId: session.session_id,
  };
}
