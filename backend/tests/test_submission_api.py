import asyncio

from app.main import create_app
from httpx import ASGITransport, AsyncClient, Response


def submit(exercise_id: str, code: str) -> Response:
    async def send() -> Response:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                f"/api/exercises/{exercise_id}/submit",
                json={"code": code},
            )

    return asyncio.run(send())


def test_submission_endpoint_runs_all_tests() -> None:
    response = submit("double-number", "def double_number(number):\n    return number * 2\n")

    assert response.status_code == 200
    assert response.json()["status"] == "passed"
    assert response.json()["tests_passed"] == 3
    assert response.json()["tests_total"] == 3


def test_submission_endpoint_handles_unknown_exercise_and_invalid_code() -> None:
    missing = submit("not-real", "def answer():\n    return 1\n")
    rejected = submit("double-number", "import pathlib")

    assert missing.status_code == 404
    assert rejected.status_code == 200
    assert rejected.json()["status"] == "rejected"


def test_submission_endpoint_limits_code_size() -> None:
    response = submit("double-number", "x" * 8_001)

    assert response.status_code == 422
