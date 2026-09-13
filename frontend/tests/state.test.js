import assert from "node:assert/strict";
import test from "node:test";

import {
  ActiveTimer,
  conditionPresentation,
  formatDuration,
  nextHintLevel,
  submissionSummary,
} from "../js/state.js";

test("hint progression stops after the third staged hint", () => {
  assert.equal(nextHintLevel(0), 1);
  assert.equal(nextHintLevel(2), 3);
  assert.equal(nextHintLevel(3), 3);
});

test("condition presentation enables assistance only where intended", () => {
  assert.equal(conditionPresentation(null).assistanceEnabled, true);
  assert.equal(
    conditionPresentation({ condition: "ai_assisted" }).assistanceEnabled,
    true,
  );
  assert.equal(conditionPresentation({ condition: "control" }).assistanceEnabled, false);
});

test("duration and submission summaries stay concise", () => {
  assert.equal(formatDuration(20.4), "20s");
  assert.equal(formatDuration(125), "2m 5s");
  assert.deepEqual(
    submissionSummary({ passed: true, tests_passed: 3, tests_total: 3 }),
    { label: "3 / 3 tests passed", tone: "success" },
  );
});

test("active timer counts only resumed intervals and resets after consumption", () => {
  let now = 1000;
  const timer = new ActiveTimer(() => now);
  timer.resume();
  now = 3500;
  timer.pause();
  now = 9000;
  timer.resume();
  now = 10500;

  assert.equal(timer.consumeSeconds(), 4);
  now = 11500;
  assert.equal(timer.consumeSeconds(), 1);
});
