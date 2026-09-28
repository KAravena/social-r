/**
 * Chilean RUN/RUT & IPE normalization & Modulo 11 check digit validator for Deno Edge Functions.
 * Supports:
 * - Traditional Chilean RUN/RUT (2-9 characters cleaned, 7-8 digit body).
 * - Provisional Educational Identifier IPE (10 characters cleaned, 9 digit body, verified via Modulo 11).
 */

export function cleanRut(rut: string): string {
  if (!rut || typeof rut !== "string") return "";
  return rut.replace(/[^0-9kK]/g, "").toUpperCase();
}

export function calculateDv(body: string): string {
  if (!body || !/^\d+$/.test(body)) return "";
  let sum = 0;
  let multiplier = 2;

  for (let i = body.length - 1; i >= 0; i--) {
    sum += parseInt(body[i], 10) * multiplier;
    multiplier = multiplier === 7 ? 2 : multiplier + 1;
  }

  const remainder = 11 - (sum % 11);
  if (remainder === 11) return "0";
  if (remainder === 10) return "K";
  return String(remainder);
}

export function getIdentifierType(identifier: string): string {
  const cleaned = cleanRut(identifier);
  if (cleaned.length < 7 || cleaned.length > 10) return "";
  const body = cleaned.slice(0, -1);
  if (!/^\d+$/.test(body) || parseInt(body, 10) < 100000) return "";
  if (cleaned.length <= 9) return "rut";
  return "ipe";
}

export function validateRut(rut: string): boolean {
  const cleaned = cleanRut(rut);
  if (cleaned.length < 2 || cleaned.length > 10) return false;

  const body = cleaned.slice(0, -1);
  const dv = cleaned.slice(-1);

  if (!/^\d+$/.test(body)) return false;
  if (parseInt(body, 10) < 100000) return false;

  return dv === calculateDv(body);
}

export function normalizeRut(rut: string): string {
  const cleaned = cleanRut(rut);
  if (cleaned.length < 2) return "";
  const body = cleaned.slice(0, -1);
  const dv = cleaned.slice(-1);
  return `${body}-${dv}`;
}

export function formatRut(rut: string): string {
  const cleaned = cleanRut(rut);
  if (cleaned.length < 2) return cleaned;

  const body = cleaned.slice(0, -1);
  const dv = cleaned.slice(-1);

  let formattedBody = "";
  for (let i = body.length - 1, count = 0; i >= 0; i--, count++) {
    if (count > 0 && count % 3 === 0) {
      formattedBody = "." + formattedBody;
    }
    formattedBody = body[i] + formattedBody;
  }

  return `${formattedBody}-${dv}`;
}

export function formatRutMasked(rut: string): string {
  const formatted = formatRut(rut);
  if (formatted.length < 6) return formatted;
  const parts = formatted.split("-");
  if (parts.length !== 2) return formatted;

  const [body, dv] = parts;
  const lastThree = body.slice(-3);
  const prefix = body.slice(0, -3);
  const maskedPrefix = prefix.replace(/\d/g, "•");

  return `${maskedPrefix}${lastThree}-${dv}`;
}

export async function computeRutLookup(rut: string, secret: string): Promise<string> {
  if (!rut || !secret) return "";
  const norm = normalizeRut(rut);
  if (!norm) return "";
  const enc = new TextEncoder();
  const keyData = enc.encode(secret);
  const messageData = enc.encode(norm);
  const cryptoKey = await crypto.subtle.importKey(
    "raw",
    keyData,
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", cryptoKey, messageData);
  const hashArray = Array.from(new Uint8Array(signature));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Canonical aliases for student identifier support
export const validateIdentifier = validateRut;
export const normalizeIdentifier = normalizeRut;
export const formatIdentifier = formatRut;
export const formatIdentifierMasked = formatRutMasked;
export const computeIdentifierLookup = computeRutLookup;
