# Architecture

The learning tool is split into a browser frontend, a typed FastAPI backend, and narrowly
defined service boundaries. This keeps HTTP parsing, learning rules, AI integration, code
execution, and analytics from becoming one large application module.

```mermaid
flowchart LR
    Browser[Vanilla JavaScript client] -->|JSON over /api| API[FastAPI routes]
    API --> Learning[Learning services]
    Learning --> Exercises[Exercise catalog]
    Learning --> AI[AI provider interface]
    Learning --> Runner[Constrained code runner]
    Learning --> Analytics[Anonymous analytics store]
    AI --> Mock[Mock provider]
    AI -. optional .-> Compatible[OpenAI-compatible provider]
    Runner --> Process[Isolated child process]
```

## Planned responsibilities

- `backend/app/api` validates HTTP input and maps service results to response models.
- `backend/app/services` will own exercise, submission, hint, and experiment workflows.
- `backend/app/ai` will hide provider-specific requests behind one interface.
- `backend/app/execution` will run student code outside the API process with strict time and
  resource limits. It is a local prototype, not a production-grade hostile-code sandbox.
- `backend/app/database` will persist anonymous sessions, attempts, hints, and completions.
- `frontend` will be a small dependency-free client so the learning interaction remains easy
  to inspect and explain.

## Safety boundary

Arbitrary student code must never be evaluated with `exec` inside a FastAPI worker. The first
runner will start a separate Python process with a timeout, a temporary working directory, a
restricted environment, and input-size limits. Those controls reduce accidental damage but do
not provide the isolation required for an internet-facing deployment. A production version
would use locked-down containers or dedicated sandbox workers with operating-system resource
controls and no network access.

## Privacy boundary

Experiment sessions will use random identifiers rather than names or email addresses. The
application will record only learning events required for the designed study. No study has been
conducted and no participant results are claimed.
