import asyncio
from pathlib import Path

from app.database.analytics_repository import AnalyticsRepository
from app.dependencies import get_experiment_service
from app.main import create_app
from app.models.experiment import ExperimentCondition
from app.services.experiment_service import ExperimentService
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


def configured_app(tmp_path: Path, condition: ExperimentCondition) -> FastAPI:
    service = ExperimentService(
        AnalyticsRepository(tmp_path / f"{condition}.db"),
        condition_picker=lambda: condition,
        id_factory=lambda: f"anonymous-{condition}-session",
    )
    application = create_app()
    application.dependency_overrides[get_experiment_service] = lambda: service
    return application


def test_ai_assisted_session_records_end_to_end_analytics(tmp_path: Path) -> None:
    async def run_flow() -> None:
        app = configured_app(tmp_path, ExperimentCondition.AI_ASSISTED)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await client.post("/api/sessions")
            session = created.json()
            headers = {"X-Session-ID": session["session_id"]}

            submission = await client.post(
                "/api/exercises/double-number/submit",
                headers=headers,
                json={
                    "code": "def double_number(number):\n    return number * 2\n",
                    "duration_seconds": 18.25,
                },
            )
            hint = await client.post(
                "/api/exercises/double-number/hint",
                headers=headers,
                json={"level": 1},
            )
            confidence = await client.post(
                f"/api/sessions/{session['session_id']}/confidence",
                json={"rating": 4},
            )
            analytics = await client.get(
                f"/api/sessions/{session['session_id']}/analytics"
            )

        assert created.status_code == 201
        assert session["condition"] == "ai_assisted"
        assert session["assistance_enabled"] is True
        assert submission.status_code == 200
        assert hint.status_code == 200
        assert confidence.status_code == 204
        assert analytics.json() == {
            "session_id": session["session_id"],
            "condition": "ai_assisted",
            "attempts": 1,
            "successful_submissions": 1,
            "failed_attempts": 0,
            "exercises_completed": 1,
            "hints_requested": 1,
            "explanations_requested": 0,
            "time_spent_seconds": 18.25,
            "average_confidence": 4.0,
        }

    asyncio.run(run_flow())


def test_control_session_cannot_request_ai_assistance(tmp_path: Path) -> None:
    async def run_flow() -> None:
        app = configured_app(tmp_path, ExperimentCondition.CONTROL)
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await client.post("/api/sessions")
            session_id = created.json()["session_id"]
            hint = await client.post(
                "/api/exercises/double-number/hint",
                headers={"X-Session-ID": session_id},
                json={"level": 1},
            )
            analytics = await client.get(f"/api/sessions/{session_id}/analytics")

        assert hint.status_code == 403
        assert hint.json()["detail"] == (
            "AI assistance is disabled for this experiment condition"
        )
        assert analytics.json()["hints_requested"] == 0

    asyncio.run(run_flow())
