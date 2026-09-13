import asyncio
from pathlib import Path

from app.ai.provider import AIProviderError, ProviderSelection
from app.content.exercises import EXERCISES
from app.database.analytics_repository import AnalyticsRepository
from app.dependencies import get_assistance_service
from app.main import create_app
from app.models.exercise import Exercise
from app.services.assistance_service import AssistanceService
from app.services.exercise_catalog import ExerciseCatalog
from app.services.experiment_service import ExperimentService
from httpx import ASGITransport, AsyncClient, Response


def post(path: str, body: dict[str, object]) -> Response:
    async def send() -> Response:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(path, json=body)

    return asyncio.run(send())


def test_hint_endpoint_returns_requested_level_from_offline_provider() -> None:
    response = post(
        "/api/exercises/sum-even-numbers/hint",
        {"code": "def sum_even_numbers(numbers):\n    return 0", "level": 2},
    )

    assert response.status_code == 200
    assert response.json()["kind"] == "hint"
    assert response.json()["level"] == 2
    assert response.json()["provider"] == "mock"
    assert response.json()["fallback_reason"] is None


def test_explanation_requires_explicit_endpoint_request() -> None:
    hint = post("/api/exercises/double-number/hint", {"level": 1})
    explanation = post("/api/exercises/double-number/explain", {"code": ""})

    assert hint.json()["kind"] == "hint"
    assert "Returning matters" not in hint.json()["content"]
    assert explanation.json()["kind"] == "explanation"
    assert "Returning matters" in explanation.json()["content"]
    assert explanation.json()["level"] is None


def test_assistance_endpoints_validate_level_and_exercise() -> None:
    invalid_level = post("/api/exercises/double-number/hint", {"level": 4})
    missing = post("/api/exercises/not-real/hint", {"level": 1})

    assert invalid_level.status_code == 422
    assert missing.status_code == 404


def test_provider_failure_returns_clean_gateway_error(tmp_path: Path) -> None:
    class FailingProvider:
        @property
        def name(self) -> str:
            return "failing-test-provider"

        async def generate_hint(self, exercise: Exercise, code: str, level: int) -> str:
            raise AIProviderError("sensitive upstream detail")

        async def explain_solution(self, exercise: Exercise, code: str) -> str:
            raise AIProviderError("sensitive upstream detail")

    experiment = ExperimentService(AnalyticsRepository(tmp_path / "analytics.db"))
    service = AssistanceService(
        ExerciseCatalog(EXERCISES),
        ProviderSelection(FailingProvider()),
        experiment,
    )
    application = create_app()
    application.dependency_overrides[get_assistance_service] = lambda: service

    async def request_hint() -> Response:
        transport = ASGITransport(app=application)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/api/exercises/double-number/hint", json={"level": 1})

    response = asyncio.run(request_hint())

    assert response.status_code == 502
    assert response.json() == {"detail": "Assistance provider unavailable"}
