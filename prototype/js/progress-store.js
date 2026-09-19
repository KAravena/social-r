/**
 * Stable application-facing progress interface.
 * The Quarto Live adapter is intentionally separate so a future backend can
 * replace localStorage without changing exercise content.
 */
class LocalProgressStore {
  constructor(namespace = "social-r:v1") {
    this.namespace = namespace;
  }

  key(exerciseId) {
    return `${this.namespace}:exercise:${exerciseId}`;
  }

  get(exerciseId) {
    const raw = window.localStorage.getItem(this.key(exerciseId));
    return raw ? JSON.parse(raw) : { status: "not_started", attempts: 0, hintsUsed: 0 };
  }

  save(exerciseId, patch) {
    const current = this.get(exerciseId);
    const next = { ...current, ...patch, updatedAt: new Date().toISOString() };
    window.localStorage.setItem(this.key(exerciseId), JSON.stringify(next));
    return next;
  }

  clear(exerciseId) {
    window.localStorage.removeItem(this.key(exerciseId));
  }
}

class SocialREventBus extends EventTarget {
  emit(type, detail = {}) {
    this.dispatchEvent(new CustomEvent(type, { detail }));
  }
}

window.SocialR = window.SocialR || {};
window.SocialR.progress = new LocalProgressStore();
window.SocialR.events = new SocialREventBus();
