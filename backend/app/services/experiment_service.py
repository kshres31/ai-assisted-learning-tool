import secrets
import sqlite3
from collections.abc import Callable

from app.database.analytics_repository import AnalyticsRepository
from app.models.experiment import ExperimentCondition, LearningAnalytics, LearningSession


class SessionNotFoundError(LookupError):
    pass


class AssistanceUnavailableError(PermissionError):
    pass


class SessionIdGenerationError(RuntimeError):
    pass


class ExperimentService:
    def __init__(
        self,
        repository: AnalyticsRepository,
        *,
        condition_picker: Callable[[], ExperimentCondition] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._repository = repository
        self._condition_picker = condition_picker or self._pick_condition
        self._id_factory = id_factory or self._generate_session_id

    def create_session(self) -> LearningSession:
        condition = self._condition_picker()
        for _ in range(3):
            try:
                return self._repository.create_session(self._id_factory(), condition)
            except sqlite3.IntegrityError:
                continue
        raise SessionIdGenerationError("Could not generate a unique anonymous session ID")

    def get_session(self, session_id: str) -> LearningSession:
        session = self._repository.get_session(session_id)
        if session is None:
            raise SessionNotFoundError(session_id)
        return session

    def ensure_assistance_available(self, session_id: str) -> LearningSession:
        session = self.get_session(session_id)
        if not session.assistance_enabled:
            raise AssistanceUnavailableError(
                "AI assistance is disabled for this experiment condition"
            )
        return session

    def record_submission(
        self,
        session_id: str,
        exercise_id: str,
        passed: bool,
        duration_seconds: float,
    ) -> None:
        self.get_session(session_id)
        self._repository.record_submission(
            session_id,
            exercise_id,
            passed,
            duration_seconds,
        )

    def record_hint(self, session_id: str, exercise_id: str, level: int) -> None:
        self.ensure_assistance_available(session_id)
        self._repository.record_hint(session_id, exercise_id, level)

    def record_explanation(self, session_id: str, exercise_id: str) -> None:
        self.ensure_assistance_available(session_id)
        self._repository.record_explanation(session_id, exercise_id)

    def record_confidence(self, session_id: str, rating: int) -> None:
        self.get_session(session_id)
        self._repository.record_confidence(session_id, rating)

    def analytics(self, session_id: str) -> LearningAnalytics:
        analytics = self._repository.summarize(session_id)
        if analytics is None:
            raise SessionNotFoundError(session_id)
        return analytics

    @staticmethod
    def _pick_condition() -> ExperimentCondition:
        return secrets.choice(tuple(ExperimentCondition))

    @staticmethod
    def _generate_session_id() -> str:
        return secrets.token_urlsafe(18)
