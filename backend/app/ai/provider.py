from dataclasses import dataclass
from typing import Protocol

from app.models.exercise import Exercise


class AIProvider(Protocol):
    @property
    def name(self) -> str: ...

    async def generate_hint(self, exercise: Exercise, code: str, level: int) -> str: ...

    async def explain_solution(self, exercise: Exercise, code: str) -> str: ...


@dataclass(frozen=True)
class ProviderSelection:
    provider: AIProvider
    fallback_reason: str | None = None
