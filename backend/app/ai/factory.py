from app.ai.mock_provider import MockAIProvider
from app.ai.provider import ProviderSelection


def select_ai_provider(configured_name: str | None) -> ProviderSelection:
    normalized_name = (configured_name or "mock").strip().casefold()
    if normalized_name == "mock":
        return ProviderSelection(MockAIProvider())
    return ProviderSelection(
        MockAIProvider(),
        fallback_reason=(
            f"Provider '{normalized_name}' is unavailable in this build; using the offline mock"
        ),
    )
