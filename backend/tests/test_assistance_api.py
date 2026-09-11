import asyncio

from app.main import create_app
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
