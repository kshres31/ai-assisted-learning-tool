# AI-Assisted Learning Tool

An in-progress, local-first coding practice platform for Python exercises. The project is being
built to explore a specific learning question: can staged, explanation-focused assistance help
students debug without immediately giving away the answer?

The current milestone includes a typed FastAPI service and a curated catalog of four exercises.
Students can browse or filter exercise summaries, retrieve starter code plus visible examples, and
submit solutions to a constrained child-process runner. Hidden evaluation cases stay inside the
domain model and are scrubbed from submission responses. Three staged hint levels and explicit
solution explanations run through a modular offline provider. Anonymous A/B sessions assign and
enforce control or assisted conditions while local SQLite analytics record only learning events. A
compatible external provider and frontend workflows will be added in later milestones. No
usability study has been conducted and no participant outcomes are claimed.

## Planned learning flow

1. Browse a small curated exercise catalog.
2. Edit and submit Python code against predefined tests.
3. Inspect concise test failures.
4. Request progressively more specific hints when the assigned condition permits them.
5. Review a solution explanation only after explicitly requesting it.

## Architecture

FastAPI owns the REST boundary and generates interactive API documentation from typed models.
Application services will own learning rules, while provider and execution interfaces will isolate
the two highest-risk integrations: external AI calls and untrusted code execution. See
[`docs/architecture.md`](docs/architecture.md) for the component diagram and safety boundary.

## Local setup

Requires Python 3.12 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Run the API:

```powershell
$env:PYTHONPATH = "backend"
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the generated API documentation.

Current endpoints:

- `GET /api/health`
- `GET /api/exercises`
- `GET /api/exercises?difficulty=beginner&tag=loops`
- `GET /api/exercises/{exercise_id}`
- `POST /api/exercises/{exercise_id}/submit`
- `POST /api/exercises/{exercise_id}/hint`
- `POST /api/exercises/{exercise_id}/explain`
- `POST /api/sessions`
- `POST /api/sessions/{session_id}/confidence`
- `GET /api/sessions/{session_id}/analytics`

Example submission body:

```json
{
  "code": "def double_number(number):\n    return number * 2\n"
}
```

## Code-execution boundary

Submissions are limited to 8 KB and checked for blocked syntax and attributes. Accepted code runs
with restricted built-ins in a separate isolated Python process, temporary directory, sanitized
environment, and two-second timeout. Hidden test inputs and expected values are removed from API
responses.

This is deliberate defense in depth for a local educational prototype, not a secure sandbox for
hostile internet users. It does not provide container-level memory, filesystem, process, or network
isolation. A public deployment must move execution to locked-down disposable containers or a
dedicated sandbox service.

## AI assistance

`AIProvider` separates learning workflows from provider-specific behavior. The current
`MockAIProvider` is deterministic, offline, and requires no API key. It supplies conceptual,
technique-focused, and likely-bug hints; a solution explanation is returned only through the
explicit `/explain` endpoint. Provider identity and fallback reasons remain visible in responses.
See [`docs/ai-design.md`](docs/ai-design.md) for the design and privacy rules.

## Experiment and analytics

`POST /api/sessions` creates a random anonymous identifier and assigns either the `control` or
`ai_assisted` condition. In experiment mode, send that identifier as the `X-Session-ID` header on
submission and assistance requests. The backend rejects hints and explanations for control
sessions, so the condition is more than a visual toggle. Requests without the header remain
available as ordinary practice mode and are not included in study analytics.

SQLite records outcomes and durations, but not submitted code or identifying profile fields. The
submission `duration_seconds` value is client-reported active time and is capped at two hours per
attempt. See [`docs/experiment-design.md`](docs/experiment-design.md) for the planned procedure,
metrics, limitations, and ethics. This is study infrastructure; it is not evidence that a study
has taken place.

Run the checks:

```powershell
ruff check backend
pytest
```

## Environment and secrets

Copy `.env.example` to `.env` only when provider configuration is needed. `.env` is ignored by
Git. The default mock provider will require no key, paid account, or network connection.

## Current limitations

- Exercises are bundled in Python; an authoring/import format has not been added yet.
- The child-process runner is intentionally local-only and not a production security boundary.
- The current assistance provider is a deterministic mock, not an external language model.
- The local analytics store is not suitable for collecting identifying research data.
- The A/B experiment and usability study are designs, not completed research.

## License

MIT
