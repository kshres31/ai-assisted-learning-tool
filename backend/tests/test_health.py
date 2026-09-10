import asyncio

from app.main import create_app
from httpx import ASGITransport, AsyncClient


def test_health_endpoint_reports_service_status() -> None:
    async def request_health() -> tuple[int, dict[str, str]]:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/health")
        return response.status_code, response.json()

    status_code, body = asyncio.run(request_health())

    assert status_code == 200
    assert body == {
        "status": "ok",
        "service": "ai-assisted-learning-tool",
    }
