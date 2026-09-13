from app.ai.mock_provider import MockAIProvider
from app.ai.openai_compatible_provider import OpenAICompatibleProvider
from app.ai.provider import ProviderSelection


def select_ai_provider(
    configured_name: str | None,
    *,
    api_base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
) -> ProviderSelection:
    normalized_name = (configured_name or "mock").strip().casefold()
    if normalized_name == "mock":
        return ProviderSelection(MockAIProvider())
    if normalized_name in {"openai", "openai-compatible"}:
        settings = {
            "AI_API_BASE_URL": api_base_url,
            "AI_API_KEY": api_key,
            "AI_MODEL": model,
        }
        missing = [name for name, value in settings.items() if not value or not value.strip()]
        if missing:
            return ProviderSelection(
                MockAIProvider(),
                fallback_reason=(
                    "OpenAI-compatible provider is not configured; missing "
                    f"{', '.join(missing)}. Using the offline mock"
                ),
            )
        return ProviderSelection(
            OpenAICompatibleProvider(
                api_base_url=api_base_url or "",
                api_key=api_key or "",
                model=model or "",
            )
        )
    return ProviderSelection(
        MockAIProvider(),
        fallback_reason=(
            f"Provider '{normalized_name}' is unavailable in this build; using the offline mock"
        ),
    )
