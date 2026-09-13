import asyncio
import json

import httpx
import pytest
from app.ai.factory import select_ai_provider
from app.ai.openai_compatible_provider import OpenAICompatibleProvider
from app.ai.provider import AIProviderError
from app.content.exercises import EXERCISES


def test_mock_provider_progresses_from_concept_to_code_observation() -> None:
    provider = select_ai_provider("mock").provider
    exercise = EXERCISES[0]

    first_hint = asyncio.run(provider.generate_hint(exercise, exercise.starter_code, 1))
    third_hint = asyncio.run(provider.generate_hint(exercise, exercise.starter_code, 3))

    assert "arithmetic relationship" in first_hint
    assert "contains `pass`" in third_hint
    assert "return number * 2" not in first_hint


def test_provider_selection_falls_back_transparently() -> None:
    selection = select_ai_provider("not-configured")

    assert selection.provider.name == "mock"
    assert selection.fallback_reason is not None
    assert "not-configured" in selection.fallback_reason


def test_openai_provider_requires_complete_configuration() -> None:
    selection = select_ai_provider(
        "openai-compatible",
        api_base_url="https://api.example.test/v1",
        api_key="",
        model="example-model",
    )

    assert selection.provider.name == "mock"
    assert selection.fallback_reason is not None
    assert "AI_API_KEY" in selection.fallback_reason


def test_complete_configuration_selects_openai_provider() -> None:
    selection = select_ai_provider(
        "openai-compatible",
        api_base_url="https://api.example.test/v1",
        api_key="test-key",
        model="example-model",
    )

    assert isinstance(selection.provider, OpenAICompatibleProvider)
    assert selection.fallback_reason is None


def test_openai_provider_sends_stateless_staged_prompt_without_hidden_tests() -> None:
    exercise = EXERCISES[0]

    def respond(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.url == "https://api.example.test/v1/responses"
        assert request.headers["Authorization"] == "Bearer test-key"
        assert body["model"] == "example-model"
        assert body["store"] is False
        assert "Hint level 2" in body["input"]
        assert "student_code_untrusted" in body["input"]
        assert "negative number" not in body["input"]
        assert exercise.solution_explanation not in body["input"]
        return httpx.Response(
            200,
            json={
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": "Use the function parameter in one arithmetic expression.",
                            }
                        ],
                    }
                ]
            },
        )

    provider = OpenAICompatibleProvider(
        api_base_url="https://api.example.test/v1",
        api_key="test-key",
        model="example-model",
        transport=httpx.MockTransport(respond),
    )

    hint = asyncio.run(provider.generate_hint(exercise, exercise.starter_code, 2))

    assert hint == "Use the function parameter in one arithmetic expression."


def test_openai_provider_normalizes_network_failures() -> None:
    provider = OpenAICompatibleProvider(
        api_base_url="https://api.example.test/v1",
        api_key="test-key",
        model="example-model",
        transport=httpx.MockTransport(lambda request: httpx.Response(503)),
    )

    with pytest.raises(AIProviderError, match="provider request failed"):
        asyncio.run(provider.generate_hint(EXERCISES[0], "", 1))
