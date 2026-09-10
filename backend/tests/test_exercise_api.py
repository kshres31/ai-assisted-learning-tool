import asyncio

from app.main import create_app
from httpx import ASGITransport, AsyncClient, Response


def request(path: str) -> Response:
    async def send() -> Response:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get(path)

    return asyncio.run(send())


def test_lists_and_filters_exercises() -> None:
    response = request("/api/exercises?difficulty=beginner&tag=loops")

    assert response.status_code == 200
    assert [exercise["id"] for exercise in response.json()] == ["sum-even-numbers"]


def test_returns_detail_without_hidden_tests() -> None:
    response = request("/api/exercises/first-duplicate")

    assert response.status_code == 200
    body = response.json()
    assert body["function_name"] == "first_duplicate"
    assert body["visible_tests"] == [
        {
            "name": "duplicate order",
            "arguments": [[2, 1, 3, 1, 2]],
            "expected": 1,
        }
    ]
    assert "test_cases" not in body


def test_returns_clear_not_found_and_validation_responses() -> None:
    missing = request("/api/exercises/not-real")
    invalid_filter = request("/api/exercises?difficulty=expert")

    assert missing.status_code == 404
    assert missing.json() == {"detail": "Exercise not found"}
    assert invalid_filter.status_code == 422
