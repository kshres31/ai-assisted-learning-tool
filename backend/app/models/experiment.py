from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ExperimentCondition(StrEnum):
    CONTROL = "control"
    AI_ASSISTED = "ai_assisted"


@dataclass(frozen=True)
class LearningSession:
    id: str
    condition: ExperimentCondition
    started_at: datetime

    @property
    def assistance_enabled(self) -> bool:
        return self.condition is ExperimentCondition.AI_ASSISTED


@dataclass(frozen=True)
class LearningAnalytics:
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
