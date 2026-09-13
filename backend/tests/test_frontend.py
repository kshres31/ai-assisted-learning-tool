import asyncio

from app.main import create_app
from httpx import ASGITransport, AsyncClient


def test_frontend_workspace_and_javascript_are_served() -> None:
    async def request_assets() -> tuple[int, str, int, str]:
        transport = ASGITransport(app=create_app())
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            page = await client.get("/")
            script = await client.get("/js/state.js")
        return page.status_code, page.text, script.status_code, script.text

    page_status, page_content, script_status, script_content = asyncio.run(request_assets())

    assert page_status == 200
    assert "TraceLab" in page_content
    assert 'id="code-editor"' in page_content
    assert script_status == 200
    assert "export class ActiveTimer" in script_content
