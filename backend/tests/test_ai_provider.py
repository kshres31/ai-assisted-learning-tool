import asyncio

from app.ai.factory import select_ai_provider
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
