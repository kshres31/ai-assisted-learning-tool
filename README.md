# AI-Assisted Learning Tool

An in-progress, local-first coding practice platform for Python exercises. The project is being
built to explore a specific learning question: can staged, explanation-focused assistance help
students debug without immediately giving away the answer?

The current milestone includes a typed FastAPI service and a curated catalog of four exercises.
Students can browse or filter exercise summaries, retrieve starter code plus visible examples, and
submit solutions to a constrained child-process runner. Hidden evaluation cases stay inside the
domain model and are scrubbed from submission responses. AI assistance, analytics, experiment, and
frontend workflows will be added in later milestones. No usability study has been conducted and no
participant outcomes are claimed.

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
- The planned local analytics store is not suitable for collecting identifying research data.
- The A/B experiment and usability study are designs, not completed research.

## License

MIT
