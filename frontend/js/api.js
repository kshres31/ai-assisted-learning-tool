export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, { method = "GET", body, sessionId } = {}) {
  const headers = { Accept: "application/json" };
  if (body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  if (sessionId) {
    headers["X-Session-ID"] = sessionId;
  }

  const response = await fetch(path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      if (typeof payload.detail === "string") {
        message = payload.detail;
      } else if (Array.isArray(payload.detail)) {
        message = payload.detail.map((item) => item.msg).join("; ");
      }
    } catch {
      // Keep the status-based message when the server did not return JSON.
    }
    throw new ApiError(message, response.status);
  }

  return response.status === 204 ? null : response.json();
}

export const learningApi = {
  listExercises() {
    return request("/api/exercises");
  },

  getExercise(exerciseId) {
    return request(`/api/exercises/${encodeURIComponent(exerciseId)}`);
  },

  submit(exerciseId, code, durationSeconds, sessionId) {
    return request(`/api/exercises/${encodeURIComponent(exerciseId)}/submit`, {
      method: "POST",
      sessionId,
      body: { code, duration_seconds: durationSeconds },
    });
  },

  requestHint(exerciseId, code, level, sessionId) {
    return request(`/api/exercises/${encodeURIComponent(exerciseId)}/hint`, {
      method: "POST",
      sessionId,
      body: { code, level },
    });
  },

  requestExplanation(exerciseId, code, sessionId) {
    return request(`/api/exercises/${encodeURIComponent(exerciseId)}/explain`, {
      method: "POST",
      sessionId,
      body: { code },
    });
  },

  createSession() {
    return request("/api/sessions", { method: "POST" });
  },

  getAnalytics(sessionId) {
    return request(`/api/sessions/${encodeURIComponent(sessionId)}/analytics`);
  },

  recordConfidence(sessionId, rating) {
    return request(`/api/sessions/${encodeURIComponent(sessionId)}/confidence`, {
      method: "POST",
      body: { rating },
    });
  },
};
