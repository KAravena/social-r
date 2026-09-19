/**
 * Social R Platform - Event Bus
 * Lightweight, decoupled event emitter for platform actions.
 */
(function () {
  "use strict";

  class SocialREventBus extends EventTarget {
    on(type, callback) {
      this.addEventListener(type, callback);
    }
    off(type, callback) {
      this.removeEventListener(type, callback);
    }
    emit(type, detail = {}) {
      if (window.SocialR && window.SocialR.debug) {
        console.log(`[SocialR Event] ${type}`, detail);
      }
      const event = new CustomEvent(type, { detail });
      this.dispatchEvent(event);
    }
  }

  window.SocialR = window.SocialR || {};
  window.SocialR.events = new SocialREventBus();
})();
