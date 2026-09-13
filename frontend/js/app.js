import { ApiError, learningApi } from "./api.js";
import {
  ActiveTimer,
  MAX_HINT_LEVEL,
  conditionPresentation,
  formatDuration,
  nextHintLevel,
  submissionSummary,
} from "./state.js";

const SESSION_STORAGE_KEY = "tracelab-experiment-session";

const elements = {
  globalStatus: document.querySelector("#global-status"),
  exerciseSearch: document.querySelector("#exercise-search"),
  difficultyFilter: document.querySelector("#difficulty-filter"),
  exerciseCount: document.querySelector("#exercise-count"),
  exerciseList: document.querySelector("#exercise-list"),
  exercisePosition: document.querySelector("#exercise-position"),
  exerciseTitle: document.querySelector("#exercise-title"),
  exerciseDifficulty: document.querySelector("#exercise-difficulty"),
  exerciseDescription: document.querySelector("#exercise-description"),
  exerciseTags: document.querySelector("#exercise-tags"),
  expectedBehavior: document.querySelector("#expected-behavior"),
  visibleExamples: document.querySelector("#visible-examples"),
  codeEditor: document.querySelector("#code-editor"),
  resetCode: document.querySelector("#reset-code"),
  submitCode: document.querySelector("#submit-code"),
  resultsEmpty: document.querySelector("#results-empty"),
  testResults: document.querySelector("#test-results"),
  resultSummary: document.querySelector("#result-summary"),
  sessionTitle: document.querySelector("#session-title"),
  sessionDescription: document.querySelector("#session-description"),
  modeDot: document.querySelector("#mode-dot"),
  startSession: document.querySelector("#start-session"),
  exitSession: document.querySelector("#exit-session"),
  coachCard: document.querySelector(".coach-card"),
  assistanceContent: document.querySelector("#assistance-content"),
  hintCounter: document.querySelector("#hint-counter"),
  requestHint: document.querySelector("#request-hint"),
  requestExplanation: document.querySelector("#request-explanation"),
  hintSteps: [...document.querySelectorAll("[data-hint-step]")],
  refreshProgress: document.querySelector("#refresh-progress"),
  metricCompleted: document.querySelector("#metric-completed"),
  metricAttempts: document.querySelector("#metric-attempts"),
  metricHints: document.querySelector("#metric-hints"),
  metricTime: document.querySelector("#metric-time"),
  confidencePanel: document.querySelector("#confidence-panel"),
  confidenceButtons: [...document.querySelectorAll("[data-rating]")],
  confidenceStatus: document.querySelector("#confidence-status"),
  toast: document.querySelector("#toast"),
};

const state = {
  exerciseSummaries: [],
  exercise: null,
  session: restoreSession(),
  hintLevel: 0,
  assistanceMessages: [],
  loadSequence: 0,
};

const activeTimer = new ActiveTimer();
let toastTimeout;

function restoreSession() {
  try {
    const session = JSON.parse(sessionStorage.getItem(SESSION_STORAGE_KEY));
    if (
      typeof session?.session_id === "string" &&
      ["control", "ai_assisted"].includes(session.condition)
    ) {
      return session;
    }
  } catch {
    sessionStorage.removeItem(SESSION_STORAGE_KEY);
  }
  return null;
}

function setServiceStatus(message, tone = "") {
  elements.globalStatus.textContent = message;
  elements.globalStatus.dataset.tone = tone;
}

function showToast(message) {
  window.clearTimeout(toastTimeout);
  elements.toast.textContent = message;
  elements.toast.hidden = false;
  toastTimeout = window.setTimeout(() => {
    elements.toast.hidden = true;
  }, 3600);
}

function clearElement(element) {
  element.replaceChildren();
}

function filteredExercises() {
  const query = elements.exerciseSearch.value.trim().toLowerCase();
  const difficulty = elements.difficultyFilter.value;
  return state.exerciseSummaries.filter((exercise) => {
    const matchesDifficulty = difficulty === "all" || exercise.difficulty === difficulty;
    const searchable = [exercise.title, exercise.description, ...exercise.concept_tags]
      .join(" ")
      .toLowerCase();
    return matchesDifficulty && (!query || searchable.includes(query));
  });
}

function renderExerciseList() {
  const exercises = filteredExercises();
  elements.exerciseCount.textContent = String(exercises.length);
  clearElement(elements.exerciseList);

  if (exercises.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No exercises match those filters.";
    elements.exerciseList.append(empty);
    return;
  }

  for (const exercise of exercises) {
    const button = document.createElement("button");
    const title = document.createElement("strong");
    const concepts = document.createElement("span");
    button.type = "button";
    button.className = "exercise-item";
    button.dataset.exerciseId = exercise.id;
    button.setAttribute("aria-current", String(state.exercise?.id === exercise.id));
    title.textContent = exercise.title;
    concepts.textContent = exercise.concept_tags.join(" · ");
    button.append(title, concepts);
    button.addEventListener("click", () => loadExercise(exercise.id));
    elements.exerciseList.append(button);
  }
}

function addTag(label) {
  const tag = document.createElement("span");
  tag.className = "tag";
  tag.textContent = label;
  elements.exerciseTags.append(tag);
}

function renderExercise(exercise) {
  const index = state.exerciseSummaries.findIndex((item) => item.id === exercise.id);
  elements.exercisePosition.textContent = `Exercise ${index + 1} of ${state.exerciseSummaries.length}`;
  elements.exerciseTitle.textContent = exercise.title;
  elements.exerciseDifficulty.textContent = exercise.difficulty;
  elements.exerciseDescription.textContent = exercise.description;
  elements.expectedBehavior.textContent = exercise.expected_behavior;
  elements.codeEditor.value = exercise.starter_code;

  clearElement(elements.exerciseTags);
  exercise.concept_tags.forEach(addTag);

  clearElement(elements.visibleExamples);
  for (const example of exercise.visible_tests) {
    const line = document.createElement("p");
    const call = document.createElement("code");
    const result = document.createElement("code");
    const argumentsText = example.arguments.map((item) => JSON.stringify(item)).join(", ");
    call.textContent = `${exercise.function_name}(${argumentsText})`;
    result.textContent = JSON.stringify(example.expected);
    line.append(call, document.createTextNode(" → "), result);
    elements.visibleExamples.append(line);
  }

  resetLearningPanels();
  activeTimer.reset();
  renderExerciseList();
}

async function loadExercise(exerciseId) {
  if (state.exercise?.id === exerciseId) {
    return;
  }
  const sequence = ++state.loadSequence;
  elements.codeEditor.disabled = true;
  elements.submitCode.disabled = true;
  try {
    const exercise = await learningApi.getExercise(exerciseId);
    if (sequence !== state.loadSequence) {
      return;
    }
    state.exercise = exercise;
    renderExercise(exercise);
  } catch (error) {
    showToast(error.message);
  } finally {
    if (sequence === state.loadSequence) {
      elements.codeEditor.disabled = false;
      elements.submitCode.disabled = false;
    }
  }
}

function resetLearningPanels() {
  state.hintLevel = 0;
  state.assistanceMessages = [];
  elements.resultsEmpty.hidden = false;
  elements.testResults.hidden = true;
  clearElement(elements.testResults);
  elements.resultSummary.textContent = "Not run yet";
  delete elements.resultSummary.dataset.tone;
  renderAssistance();
}

function renderAssistance() {
  const presentation = conditionPresentation(state.session);
  const assistanceEnabled = presentation.assistanceEnabled;
  elements.coachCard.dataset.disabled = String(!assistanceEnabled);
  elements.hintCounter.textContent = `${state.hintLevel} / ${MAX_HINT_LEVEL}`;
  elements.hintSteps.forEach((step, index) => {
    step.dataset.complete = String(index < state.hintLevel);
  });

  clearElement(elements.assistanceContent);
  if (!assistanceEnabled) {
    const message = document.createElement("p");
    message.textContent =
      "This anonymous session was assigned to traditional debugging, so assistance is disabled.";
    elements.assistanceContent.append(message);
  } else if (state.assistanceMessages.length === 0) {
    const message = document.createElement("p");
    message.textContent = "Try the exercise first. Ask for a conceptual nudge when you feel stuck.";
    elements.assistanceContent.append(message);
  } else {
    for (const item of state.assistanceMessages) {
      const message = document.createElement("p");
      message.textContent = `${item.label}: ${item.content}`;
      elements.assistanceContent.append(message);
    }
  }

  const nextLevel = nextHintLevel(state.hintLevel);
  elements.requestHint.textContent =
    state.hintLevel >= MAX_HINT_LEVEL ? "All hints viewed" : `Request hint ${nextLevel}`;
  elements.requestHint.disabled = !state.exercise || !assistanceEnabled || state.hintLevel >= 3;
  elements.requestExplanation.disabled = !state.exercise || !assistanceEnabled;
}

function renderSession() {
  const presentation = conditionPresentation(state.session);
  elements.sessionTitle.textContent = presentation.title;
  elements.sessionDescription.textContent = presentation.description;
  elements.modeDot.dataset.active = String(Boolean(state.session));
  elements.startSession.hidden = Boolean(state.session);
  elements.exitSession.hidden = !state.session;
  elements.confidencePanel.hidden = !state.session;

  if (!state.session) {
    elements.metricCompleted.textContent = "—";
    elements.metricAttempts.textContent = "—";
    elements.metricHints.textContent = "—";
    elements.metricTime.textContent = "—";
    elements.confidenceStatus.textContent = "Optional and anonymous";
    elements.confidenceButtons.forEach((button) => button.removeAttribute("aria-pressed"));
  }
  renderAssistance();
}

function renderResult(result) {
  const summary = submissionSummary(result);
  elements.resultSummary.textContent = summary.label;
  elements.resultSummary.dataset.tone = summary.tone;
  elements.resultsEmpty.hidden = true;
  elements.testResults.hidden = false;
  clearElement(elements.testResults);

  if (result.message?.trim()) {
    const message = document.createElement("p");
    message.className = "empty-state";
    message.textContent = result.message;
    elements.testResults.append(message);
  }

  for (const outcome of result.test_results) {
    const row = document.createElement("div");
    const icon = document.createElement("span");
    const detail = document.createElement("div");
    const name = document.createElement("strong");
    const outcomeMessage = document.createElement("small");
    row.className = "test-result";
    row.dataset.passed = String(outcome.passed);
    icon.className = "test-result-icon";
    icon.textContent = outcome.passed ? "✓" : "×";
    name.textContent = outcome.name;
    outcomeMessage.textContent = outcome.message;
    detail.append(name, outcomeMessage);
    row.append(icon, detail);
    elements.testResults.append(row);
  }
}

async function submitCode() {
  if (!state.exercise || !elements.codeEditor.value.trim()) {
    showToast("Write a solution before running the tests.");
    return;
  }
  elements.submitCode.disabled = true;
  const originalText = elements.submitCode.textContent;
  elements.submitCode.textContent = "Running…";
  const durationSeconds = Number(activeTimer.consumeSeconds().toFixed(2));
  try {
    const result = await learningApi.submit(
      state.exercise.id,
      elements.codeEditor.value,
      durationSeconds,
      state.session?.session_id,
    );
    renderResult(result);
    await refreshAnalytics();
  } catch (error) {
    showToast(error.message);
  } finally {
    elements.submitCode.textContent = originalText;
    elements.submitCode.disabled = false;
  }
}

async function requestHint() {
  if (!state.exercise) {
    return;
  }
  const level = nextHintLevel(state.hintLevel);
  elements.requestHint.disabled = true;
  try {
    const reply = await learningApi.requestHint(
      state.exercise.id,
      elements.codeEditor.value,
      level,
      state.session?.session_id,
    );
    state.hintLevel = level;
    state.assistanceMessages.push({
      label: `Hint ${level} · ${reply.provider}`,
      content: reply.content,
    });
    if (reply.fallback_reason) {
      showToast(reply.fallback_reason);
    }
    renderAssistance();
    await refreshAnalytics();
  } catch (error) {
    showToast(error.message);
    renderAssistance();
  }
}

async function requestExplanation() {
  if (!state.exercise) {
    return;
  }
  elements.requestExplanation.disabled = true;
  try {
    const reply = await learningApi.requestExplanation(
      state.exercise.id,
      elements.codeEditor.value,
      state.session?.session_id,
    );
    state.assistanceMessages.push({
      label: `Explanation · ${reply.provider}`,
      content: reply.content,
    });
    if (reply.fallback_reason) {
      showToast(reply.fallback_reason);
    }
    renderAssistance();
    await refreshAnalytics();
  } catch (error) {
    showToast(error.message);
  } finally {
    elements.requestExplanation.disabled = false;
  }
}

async function startSession() {
  elements.startSession.disabled = true;
  elements.startSession.textContent = "Assigning…";
  try {
    state.session = await learningApi.createSession();
    sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(state.session));
    state.assistanceMessages = [];
    state.hintLevel = 0;
    renderSession();
    await refreshAnalytics();
    showToast(`Assigned to the ${conditionPresentation(state.session).title.toLowerCase()}.`);
  } catch (error) {
    showToast(error.message);
  } finally {
    elements.startSession.disabled = false;
    elements.startSession.textContent = "Start A/B session";
  }
}

function exitSession() {
  state.session = null;
  sessionStorage.removeItem(SESSION_STORAGE_KEY);
  state.assistanceMessages = [];
  state.hintLevel = 0;
  renderSession();
  showToast("Session detached. Its anonymous local analytics remain in the study database.");
}

async function refreshAnalytics() {
  if (!state.session) {
    return;
  }
  try {
    const analytics = await learningApi.getAnalytics(state.session.session_id);
    elements.metricCompleted.textContent = String(analytics.exercises_completed);
    elements.metricAttempts.textContent = String(analytics.attempts);
    elements.metricHints.textContent = String(analytics.hints_requested);
    elements.metricTime.textContent = formatDuration(analytics.time_spent_seconds);
    elements.confidenceStatus.textContent =
      analytics.average_confidence === null
        ? "Optional and anonymous"
        : `Average recorded confidence: ${analytics.average_confidence.toFixed(1)} / 5`;
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      state.session = null;
      sessionStorage.removeItem(SESSION_STORAGE_KEY);
      renderSession();
      showToast("That saved session no longer exists. Practice mode has been restored.");
      return;
    }
    showToast(error.message);
  }
}

async function recordConfidence(rating, selectedButton) {
  if (!state.session) {
    return;
  }
  elements.confidenceButtons.forEach((button) => (button.disabled = true));
  try {
    await learningApi.recordConfidence(state.session.session_id, rating);
    elements.confidenceButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button === selectedButton));
    });
    await refreshAnalytics();
  } catch (error) {
    showToast(error.message);
  } finally {
    elements.confidenceButtons.forEach((button) => (button.disabled = false));
  }
}

function bindEvents() {
  elements.exerciseSearch.addEventListener("input", renderExerciseList);
  elements.difficultyFilter.addEventListener("change", renderExerciseList);
  elements.resetCode.addEventListener("click", () => {
    if (state.exercise) {
      elements.codeEditor.value = state.exercise.starter_code;
      activeTimer.reset();
      showToast("Starter code restored.");
    }
  });
  elements.submitCode.addEventListener("click", submitCode);
  elements.requestHint.addEventListener("click", requestHint);
  elements.requestExplanation.addEventListener("click", requestExplanation);
  elements.startSession.addEventListener("click", startSession);
  elements.exitSession.addEventListener("click", exitSession);
  elements.refreshProgress.addEventListener("click", refreshAnalytics);
  elements.confidenceButtons.forEach((button) => {
    button.addEventListener("click", () => recordConfidence(Number(button.dataset.rating), button));
  });
  elements.codeEditor.addEventListener("keydown", (event) => {
    if (event.key === "Tab") {
      event.preventDefault();
      const start = elements.codeEditor.selectionStart;
      const end = elements.codeEditor.selectionEnd;
      elements.codeEditor.setRangeText("    ", start, end, "end");
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      activeTimer.pause();
    } else {
      activeTimer.resume();
    }
  });
}

async function initialize() {
  bindEvents();
  renderSession();
  try {
    state.exerciseSummaries = await learningApi.listExercises();
    renderExerciseList();
    setServiceStatus("Learning service connected", "success");
    if (state.exerciseSummaries.length > 0) {
      await loadExercise(state.exerciseSummaries[0].id);
    }
    await refreshAnalytics();
  } catch (error) {
    setServiceStatus("Learning service unavailable", "error");
    showToast(error.message);
  }
}

initialize();
