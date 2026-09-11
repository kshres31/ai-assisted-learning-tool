from dataclasses import dataclass
from enum import StrEnum

from app.ai.provider import ProviderSelection
from app.services.exercise_catalog import ExerciseCatalog
from app.services.experiment_service import ExperimentService


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
    def __init__(
        self,
        catalog: ExerciseCatalog,
        selection: ProviderSelection,
        experiment: ExperimentService,
    ) -> None:
        self._catalog = catalog
        self._selection = selection
        self._experiment = experiment

    async def hint(
        self,
        exercise_id: str,
        code: str,
        level: int,
        session_id: str | None = None,
    ) -> AssistanceReply:
        exercise = self._catalog.get(exercise_id)
        if session_id is not None:
            self._experiment.ensure_assistance_available(session_id)
        content = await self._selection.provider.generate_hint(exercise, code, level)
        if session_id is not None:
            self._experiment.record_hint(session_id, exercise_id, level)
        return AssistanceReply(
            kind=AssistanceKind.HINT,
            content=content,
            provider=self._selection.provider.name,
            level=level,
            fallback_reason=self._selection.fallback_reason,
        )

    async def explain(
        self,
        exercise_id: str,
        code: str,
        session_id: str | None = None,
    ) -> AssistanceReply:
        exercise = self._catalog.get(exercise_id)
        if session_id is not None:
            self._experiment.ensure_assistance_available(session_id)
        content = await self._selection.provider.explain_solution(exercise, code)
        if session_id is not None:
            self._experiment.record_explanation(session_id, exercise_id)
        return AssistanceReply(
            kind=AssistanceKind.EXPLANATION,
            content=content,
            provider=self._selection.provider.name,
            fallback_reason=self._selection.fallback_reason,
        )
