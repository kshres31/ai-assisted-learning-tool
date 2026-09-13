export const MAX_HINT_LEVEL = 3;

export function nextHintLevel(currentLevel) {
  const normalized = Number.isFinite(currentLevel) ? Math.max(0, currentLevel) : 0;
  return Math.min(MAX_HINT_LEVEL, normalized + 1);
}

export function formatDuration(totalSeconds) {
  const seconds = Math.max(0, Math.round(Number(totalSeconds) || 0));
  if (seconds < 60) {
    return `${seconds}s`;
  }
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  return remainder === 0 ? `${minutes}m` : `${minutes}m ${remainder}s`;
}

export function conditionPresentation(session) {
  if (!session) {
    return {
      title: "Practice privately",
      description:
        "Practice is not included in experiment analytics until you start an anonymous session.",
      assistanceEnabled: true,
    };
  }
  if (session.condition === "ai_assisted") {
    return {
      title: "AI-assisted condition",
      description: "Attempts, active time, and assistance use are recorded under a random ID.",
      assistanceEnabled: true,
    };
  }
  return {
    title: "Traditional condition",
    description: "Attempts and active time are recorded; staged assistance is disabled.",
    assistanceEnabled: false,
  };
}

export function submissionSummary(result) {
  if (result.passed) {
    return {
      label: `${result.tests_passed} / ${result.tests_total} tests passed`,
      tone: "success",
    };
  }
  if (result.tests_total > 0) {
    return {
      label: `${result.tests_passed} / ${result.tests_total} tests passed`,
      tone: "error",
    };
  }
  return { label: result.status.replaceAll("_", " "), tone: "error" };
}

export class ActiveTimer {
  constructor(now = () => performance.now()) {
    this.now = now;
    this.accumulatedMilliseconds = 0;
    this.startedAt = null;
  }

  resume() {
    if (this.startedAt === null) {
      this.startedAt = this.now();
    }
  }

  pause() {
    if (this.startedAt !== null) {
      this.accumulatedMilliseconds += this.now() - this.startedAt;
      this.startedAt = null;
    }
  }

  reset() {
    this.accumulatedMilliseconds = 0;
    this.startedAt = this.now();
  }

  consumeSeconds() {
    this.pause();
    const seconds = this.accumulatedMilliseconds / 1000;
    this.accumulatedMilliseconds = 0;
    this.resume();
    return seconds;
  }
}
