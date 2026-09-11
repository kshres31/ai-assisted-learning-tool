from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from app.models.experiment import ExperimentCondition, LearningAnalytics, LearningSession


class SessionResponse(BaseModel):
    session_id: str
    condition: ExperimentCondition
    assistance_enabled: bool
    started_at: datetime

    @classmethod
    def from_domain(cls, session: LearningSession) -> "SessionResponse":
        return cls(
            session_id=session.id,
            condition=session.condition,
            assistance_enabled=session.assistance_enabled,
            started_at=session.started_at,
        )


class ConfidenceRequest(BaseModel):
    rating: Annotated[int, Field(ge=1, le=5)]


class AnalyticsResponse(BaseModel):
    session_id: str
    condition: ExperimentCondition
    attempts: int
    successful_submissions: int
    failed_attempts: int
    exercises_completed: int
    hints_requested: int
    explanations_requested: int
    time_spent_seconds: float
    average_confidence: float | None

    @classmethod
    def from_domain(cls, analytics: LearningAnalytics) -> "AnalyticsResponse":
        return cls(
            session_id=analytics.session_id,
            condition=analytics.condition,
            attempts=analytics.attempts,
            successful_submissions=analytics.successful_submissions,
            failed_attempts=analytics.failed_attempts,
            exercises_completed=analytics.exercises_completed,
            hints_requested=analytics.hints_requested,
            explanations_requested=analytics.explanations_requested,
            time_spent_seconds=analytics.time_spent_seconds,
            average_confidence=analytics.average_confidence,
        )
