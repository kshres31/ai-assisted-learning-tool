# Project status and claim audit

TraceLab is complete as a local portfolio prototype and as infrastructure for a future usability
study. Completion here means the application, offline assistance path, optional provider contract,
experiment assignment, anonymous analytics, documentation, and automated checks are implemented.
It does not mean that a live paid model or human-subject study has been run.

## Release verification

The final local verification covers:

- backend linting with Ruff;
- the full backend test suite, including exercise, runner, provider, experiment, and analytics
  behavior;
- frontend unit tests and JavaScript syntax checks;
- Python bytecode compilation and dependency consistency;
- a running-server smoke test of the application and its static assets;
- inspection of the real workspace screenshot;
- a staged-secret scan and clean Git worktree check.

GitHub Actions repeats the backend and frontend checks on every push to `main`.

## Claim audit

### Verified

- A responsive interactive Python tutorial workspace with four curated exercises.
- Three-stage deterministic hints plus explicitly requested solution explanations.
- An optional Responses-compatible provider contract tested with mocked HTTP responses.
- Anonymous random assignment to control and AI-assisted experiment conditions.
- Backend enforcement that blocks assistance for control sessions.
- Local analytics for attempts, completion, failures, assistance usage, active time, and confidence.
- A runnable usability-study plan, participant script, questionnaire, and empty results template.

### Partially verified

- Real-time AI-assisted suggestions: the end-to-end assistance experience works locally with the
  deterministic mock provider, and the external provider contract is tested without a paid call.

### Not verified and not claimed

- Results from a usability test with 15 or more students.
- Any measured learning improvement, completion-rate lift, or participant satisfaction result.
- Production-grade isolation for untrusted internet users.
- A successful request to a live paid AI provider.

## What would require outside input

A live provider verification requires the project owner to configure a valid API key privately in
the local environment. A human usability study requires participant recruitment, informed consent,
and any required institutional review. Credentials and participant records must never be committed
to this repository.
