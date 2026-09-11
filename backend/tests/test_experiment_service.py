from pathlib import Path

import pytest
from app.database.analytics_repository import AnalyticsRepository
from app.models.experiment import ExperimentCondition
from app.services.experiment_service import AssistanceUnavailableError, ExperimentService


def test_condition_picker_assigns_each_new_anonymous_session(tmp_path: Path) -> None:
    conditions = iter((ExperimentCondition.CONTROL, ExperimentCondition.AI_ASSISTED))
    identifiers = iter(("anonymous-session-a", "anonymous-session-b"))
    service = ExperimentService(
        AnalyticsRepository(tmp_path / "analytics.db"),
        condition_picker=lambda: next(conditions),
        id_factory=lambda: next(identifiers),
    )

    first = service.create_session()
    second = service.create_session()

    assert first.condition is ExperimentCondition.CONTROL
    assert first.assistance_enabled is False
    assert second.condition is ExperimentCondition.AI_ASSISTED
    assert second.assistance_enabled is True


def test_analytics_summarize_learning_events_without_identity_data(tmp_path: Path) -> None:
    service = ExperimentService(
        AnalyticsRepository(tmp_path / "analytics.db"),
        condition_picker=lambda: ExperimentCondition.AI_ASSISTED,
        id_factory=lambda: "anonymous-session-analytics",
    )
    session = service.create_session()

    service.record_submission(session.id, "double-number", False, 12.5)
    service.record_submission(session.id, "double-number", True, 7.5)
    service.record_hint(session.id, "double-number", 2)
    service.record_explanation(session.id, "double-number")
    service.record_confidence(session.id, 4)
    service.record_confidence(session.id, 5)

    analytics = service.analytics(session.id)

    assert analytics.attempts == 2
    assert analytics.successful_submissions == 1
    assert analytics.failed_attempts == 1
    assert analytics.exercises_completed == 1
    assert analytics.hints_requested == 1
    assert analytics.explanations_requested == 1
    assert analytics.time_spent_seconds == 20
    assert analytics.average_confidence == 4.5


def test_control_condition_rejects_assistance(tmp_path: Path) -> None:
    service = ExperimentService(
        AnalyticsRepository(tmp_path / "analytics.db"),
        condition_picker=lambda: ExperimentCondition.CONTROL,
        id_factory=lambda: "anonymous-session-control",
    )
    session = service.create_session()

    with pytest.raises(AssistanceUnavailableError):
        service.record_hint(session.id, "double-number", 1)
