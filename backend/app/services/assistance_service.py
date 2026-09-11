from dataclasses import dataclass
from enum import StrEnum

from app.ai.provider import ProviderSelection
from app.services.exercise_catalog import ExerciseCatalog


class AssistanceKind(StrEnum):
    HINT = "hint"
    EXPLANATION = "explanation"


@dataclass(frozen=True)
class AssistanceReply:
    kind: AssistanceKind
    content: str
    provider: str
    level: int | None = None
    fallback_reason: str | None = None


class AssistanceService:
    def __init__(self, catalog: ExerciseCatalog, selection: ProviderSelection) -> None:
        self._catalog = catalog
        self._selection = selection

    async def hint(self, exercise_id: str, code: str, level: int) -> AssistanceReply:
        exercise = self._catalog.get(exercise_id)
        content = await self._selection.provider.generate_hint(exercise, code, level)
        return AssistanceReply(
            kind=AssistanceKind.HINT,
            content=content,
            provider=self._selection.provider.name,
            level=level,
            fallback_reason=self._selection.fallback_reason,
        )

    async def explain(self, exercise_id: str, code: str) -> AssistanceReply:
        exercise = self._catalog.get(exercise_id)
        content = await self._selection.provider.explain_solution(exercise, code)
        return AssistanceReply(
            kind=AssistanceKind.EXPLANATION,
            content=content,
            provider=self._selection.provider.name,
            fallback_reason=self._selection.fallback_reason,
        )
