"""
Chilean RUT and IPE validation and normalization utilities in Python.
Used by roster importer, export script, and test suites.

Supports two identifier classes:
A. Chilean RUN/RUT (traditional body of 7-8 digits + DV, 8-9 characters cleaned).
B. IPE (Provisional Educational Identifier used in higher education / exchange,
   observed body of 9 digits + DV, 10 characters cleaned, verified via Modulo 11).
"""

import hashlib
import hmac
import re


def clean_rut(rut: str) -> str:
    """Removes all non-alphanumeric characters and converts 'k' to 'K'."""
    if not rut:
        return ""
    return re.sub(r"[^0-9kK]", "", str(rut)).upper()


def calculate_dv(body: str) -> str:
    """Calculates Modulo 11 check digit for Chilean RUT/IPE body."""
    if not body or not body.isdigit():
        return ""
    s = 0
    multiplier = 2
    for char in reversed(body):
        s += int(char) * multiplier
        multiplier = 2 if multiplier == 7 else multiplier + 1
    remainder = 11 - (s % 11)
    if remainder == 11:
        return "0"
    if remainder == 10:
        return "K"
    return str(remainder)


def get_identifier_type(identifier: str) -> str:
    """
    Returns identifier classification based on cleaned length and body sanity:
    - 'rut': Chilean RUN/RUT (cleaned len 7-9, body >= 100000)
    - 'ipe': Provisional Educational Identifier (observed 9-digit body, cleaned len 10)
    - '': empty or unrecognized length/body
    """
    cleaned = clean_rut(identifier)
    if len(cleaned) < 7 or len(cleaned) > 10:
        return ""
    body = cleaned[:-1]
    if not body.isdigit() or int(body) < 100000:
        return ""
    if len(cleaned) <= 9:
        return "rut"
    return "ipe"


def validate_rut(rut: str) -> bool:
    """
    Validates Chilean RUN/RUT or IPE with canonical Modulo 11 algorithm.
    - RUN/RUT: 2-9 characters cleaned (body >= 100000)
    - IPE: 10 characters cleaned (9-digit body)
    """
    cleaned = clean_rut(rut)
    if len(cleaned) < 2 or len(cleaned) > 10:
        return False
    body = cleaned[:-1]
    dv = cleaned[-1]
    if not body.isdigit() or int(body) < 100000:
        return False
    return dv == calculate_dv(body)


def normalize_rut(rut: str) -> str:
    """Normalizes RUT/IPE to canonical format: '12345678-9' or '100000000-9'."""
    cleaned = clean_rut(rut)
    if len(cleaned) < 2:
        return ""
    return f"{cleaned[:-1]}-{cleaned[-1]}"


def format_rut(rut: str) -> str:
    """Formats RUT/IPE as '12.345.678-9' or '100.000.000-9'."""
    cleaned = clean_rut(rut)
    if len(cleaned) < 2:
        return cleaned
    body = cleaned[:-1]
    dv = cleaned[-1]
    formatted_body = ""
    for idx, char in enumerate(reversed(body)):
        if idx > 0 and idx % 3 == 0:
            formatted_body = "." + formatted_body
        formatted_body = char + formatted_body
    return f"{formatted_body}-{dv}"


def format_rut_masked(rut: str) -> str:
    """Formats RUT/IPE for discreet display: '••.•••.678-9' or '•••.•••.431-8'."""
    formatted = format_rut(rut)
    if len(formatted) < 6:
        return formatted
    parts = formatted.split("-")
    if len(parts) != 2:
        return formatted
    body, dv = parts
    last_three = body[-3:]
    prefix = body[:-3]
    masked_prefix = re.sub(r"\d", "•", prefix)
    return f"{masked_prefix}{last_three}-{dv}"


def compute_rut_lookup(rut: str, secret: str) -> str:
    """
    Computes deterministic HMAC-SHA256 lookup hash for a normalized Chilean RUT or IPE.
    Used for privacy-preserving roster imports, student lookups, and local export joins.
    """
    if not rut or not secret:
        return ""
    norm = normalize_rut(rut)
    if not norm:
        return ""
    return hmac.new(
        secret.encode("utf-8"),
        norm.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


# Canonical aliases for general student identifier support
validate_identifier = validate_rut
normalize_identifier = normalize_rut
format_identifier = format_rut
format_identifier_masked = format_rut_masked
mask_rut = format_rut_masked
compute_identifier_lookup = compute_rut_lookup
