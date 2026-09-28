/**
 * Social R - Chilean RUN/RUT & IPE Validation & Normalization Utility
 * Standard Modulo 11 check digit algorithm.
 * Supports:
 * - Chilean RUN/RUT (2-9 characters cleaned, 7-8 digit body).
 * - Provisional Educational Identifier IPE (10 characters cleaned, 9 digit body).
 */
(function () {
  "use strict";

  const RutValidator = {
    /**
     * Cleans RUT/IPE input: removes dots, spaces, hyphens, and upper-cases 'K'.
     * Example: " 12.345.678-k " -> "12345678K"
     */
    clean(rut) {
      if (!rut || typeof rut !== "string") return "";
      return rut.replace(/[^0-9kK]/g, "").toUpperCase();
    },

    /**
     * Calculates the Modulo 11 check digit for a given RUT/IPE body string.
     * @param {string} body - Numeric string of RUT/IPE body.
     * @returns {string} Calculated DV ('0'-'9' or 'K').
     */
    calculateDv(body) {
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
    },

    /**
     * Returns identifier classification based on cleaned length:
     * - 'rut': Chilean RUN/RUT (cleaned len 2-9)
     * - 'ipe': Provisional Educational Identifier (cleaned len 10, 9-digit body)
     * - '': empty or unrecognized length
     * @param {string} identifier
     * @returns {string}
     */
    getIdentifierType(identifier) {
      const cleaned = this.clean(identifier);
      if (cleaned.length < 7 || cleaned.length > 10) return "";
      const body = cleaned.slice(0, -1);
      if (!/^\d+$/.test(body) || parseInt(body, 10) < 100000) return "";
      if (cleaned.length <= 9) return "rut";
      return "ipe";
    },

    /**
     * Validates whether a RUT or IPE is valid using Modulo 11.
     * Accepts inputs with or without dots, spaces, or hyphens.
     * Minimum valid body is 100000. Maximum is 9 digits (IPE) or 8 digits (traditional RUT).
     * @param {string} rut
     * @returns {boolean}
     */
    validate(rut) {
      const cleaned = this.clean(rut);
      if (cleaned.length < 2 || cleaned.length > 10) return false;

      const body = cleaned.slice(0, -1);
      const dv = cleaned.slice(-1);

      if (!/^\d+$/.test(body)) return false;
      if (parseInt(body, 10) < 100000) return false; // Sanity check for realistic Chilean RUT/IPE

      const expectedDv = this.calculateDv(body);
      return dv === expectedDv;
    },

    /**
     * Normalizes a valid or cleanable RUT/IPE to canonical format: "12345678-9" or "100000000-9".
     * @param {string} rut
     * @returns {string} Normalized RUT, or empty string if invalid length.
     */
    normalize(rut) {
      const cleaned = this.clean(rut);
      if (cleaned.length < 2) return "";
      const body = cleaned.slice(0, -1);
      const dv = cleaned.slice(-1);
      return `${body}-${dv}`;
    },

    /**
     * Formats RUT/IPE with standard Chilean punctuation: "12.345.678-9" or "100.000.000-9".
     * @param {string} rut
     * @returns {string}
     */
    format(rut) {
      const cleaned = this.clean(rut);
      if (cleaned.length < 2) return cleaned;

      const body = cleaned.slice(0, -1);
      const dv = cleaned.slice(-1);

      // Add dots to body every 3 digits from right
      let formattedBody = "";
      for (let i = body.length - 1, count = 0; i >= 0; i--, count++) {
        if (count > 0 && count % 3 === 0) {
          formattedBody = "." + formattedBody;
        }
        formattedBody = body[i] + formattedBody;
      }

      return `${formattedBody}-${dv}`;
    },

    /**
     * Masks the RUT/IPE for discreet display: "••.•••.678-9" or "•••.•••.431-8".
     * @param {string} rut
     * @returns {string}
     */
    formatMasked(rut) {
      const formatted = this.format(rut);
      if (formatted.length < 6) return formatted;

      // Mask up to the last 3 digits of body
      const parts = formatted.split("-");
      if (parts.length !== 2) return formatted;

      const body = parts[0];
      const dv = parts[1];

      // Keep last 3 chars of body visible, mask previous with dots preserved
      const lastThree = body.slice(-3);
      const prefix = body.slice(0, -3);
      const maskedPrefix = prefix.replace(/\d/g, "•");

      return `${maskedPrefix}${lastThree}-${dv}`;
    },

    /**
     * Alias for formatMasked
     */
    mask(rut) {
      return this.formatMasked(rut);
    }
  };

  // Export for browser & module environments
  if (typeof module !== "undefined" && module.exports) {
    module.exports = RutValidator;
  }
  window.SocialR = window.SocialR || {};
  window.SocialR.RutValidator = RutValidator;
  window.SocialR.RUTValidator = RutValidator;
  window.SocialR.IdentifierValidator = RutValidator;
})();
