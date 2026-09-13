# Usability Test Plan

## Status

This document is a runnable plan for a future moderated pilot. No sessions have been conducted and
no participant observations or results exist yet.

## Study objective

Evaluate whether learners can independently find an exercise, understand the task, edit and submit
Python code, interpret test feedback, use only the assistance available to their assigned
condition, and report confidence. The usability study complements the A/B experiment: usability
observations explain where the interface causes confusion, while experiment events describe what
participants did.

## Recruitment target

Recruit at least 16 adult volunteers who have learned basic programming but are not already expert
Python developers. This is a practical pilot target, not a statistically powered sample or a claim
that recruitment has happened. Record only eligibility and consent status outside the application;
do not add names or contact information to the learning database.

## Roles and materials

- **Moderator:** reads the same prompts, avoids teaching during tasks, and records observations.
- **Observer, if available:** records behavior without interacting with the participant.
- **Materials:** local application, participant instructions, note sheet, timer backup, and
  post-study questionnaire.
- **Environment:** same browser size, keyboard, application version, exercise order, and network
  arrangement for every session.

Before recruitment, decide whether institutional review, instructor approval, or a formal consent
process is required. This repository does not replace those processes.

## Session structure

Target duration: 25–35 minutes.

1. **Welcome and consent — 3 minutes.** Explain the purpose, voluntary participation, recording
   policy, withdrawal process, and what anonymous events are stored.
2. **Background questions — 2 minutes.** Ask only broad experience bands needed to interpret the
   pilot, and store them separately from application events if approved.
3. **Think-aloud practice — 2 minutes.** Demonstrate thinking aloud with a neutral non-coding task.
4. **Assigned exercises — 15–20 minutes.** Start one anonymous A/B session, then use the same
   exercise order and time limit for all participants.
5. **Questionnaire — 5 minutes.** Collect the ratings and open-response feedback defined in the
   questionnaire document.
6. **Debrief — 3 minutes.** Explain the two conditions, answer questions, and repeat the withdrawal
   process.

## Tasks and success criteria

### Task 1: Orient to the workspace

Prompt: “Find the beginner exercise about even numbers and describe what the function should
return.”

Success means the participant finds the exercise without moderator navigation and can restate the
expected behavior.

### Task 2: Submit and interpret feedback

Prompt: “Work on the exercise and run the tests. Use the feedback to make another attempt if
needed.”

Success means the participant can edit code, submit it, distinguish passing and failing results,
and identify a reasonable next action.

### Task 3: Use the assigned support

Prompt: “If the interface offers learning support, use it only when you normally would. If it does
not, continue with the available debugging information.”

Success means assisted participants can request staged guidance and control participants
understand that assistance is intentionally unavailable.

### Task 4: Review progress and rate confidence

Prompt: “Find your session progress and record how confident you feel.”

Success means the participant can locate attempts, completions, hint count, active time, and the
confidence controls.

## Observation guide

Record timestamps and observable behavior, not guesses about motivation. Useful observations
include:

- first navigation path and any backtracking;
- labels the participant rereads or misunderstands;
- submission errors and whether feedback supports recovery;
- requests for moderator help, including the neutral response given;
- whether staged guidance changes the participant's next action;
- accessibility problems involving focus, keyboard use, contrast, or zoom;
- task completion, abandonment, and elapsed time.

Use neutral follow-ups such as “What are you looking for?” and “What do you expect that control to
do?” Do not say where to click or explain a programming solution during a task.

## Measures

- task completion and completion with moderator help;
- time on task and number of attempts;
- critical and non-critical usability errors;
- hint and explanation use for assisted sessions;
- self-reported confidence and questionnaire ratings;
- qualitative themes from think-aloud comments and open responses.

## Severity scale

- **0 — observation:** preference or comment with no clear obstacle.
- **1 — minor:** hesitation or recoverable confusion that does not prevent completion.
- **2 — major:** repeated confusion, substantial delay, or moderator help required.
- **3 — critical:** task failure, data loss, safety concern, or inability to continue.

Two reviewers should independently classify ambiguous issues when possible and document how they
resolved disagreements.

## Pilot and stopping rules

Run one or two internal pilot sessions before recruiting the target sample. Pilot data must be
clearly labeled and excluded from the main analysis if the procedure or interface changes. Pause
the study if the application records identity data unexpectedly, assigns conditions incorrectly,
exposes hidden tests, loses participant work, or creates a security concern.

## Data handling

Use random application session IDs. Keep consent records and recruitment contact information out
of the repository and separate from event data. Define access, encryption, retention, deletion,
and withdrawal procedures before collection. Never commit raw study data to GitHub.
