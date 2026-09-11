import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

from app.models.experiment import ExperimentCondition, LearningAnalytics, LearningSession


class AnalyticsRepository:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._initialized = False
        self._initialization_lock = Lock()

    def create_session(self, session_id: str, condition: ExperimentCondition) -> LearningSession:
        self._ensure_initialized()
        started_at = datetime.now(UTC)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO experiment_sessions (id, condition, started_at)
                VALUES (?, ?, ?)
                """,
                (session_id, condition, started_at.isoformat()),
            )
        return LearningSession(session_id, condition, started_at)

    def get_session(self, session_id: str) -> LearningSession | None:
        self._ensure_initialized()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, condition, started_at FROM experiment_sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        return LearningSession(
            id=row["id"],
            condition=ExperimentCondition(row["condition"]),
            started_at=datetime.fromisoformat(row["started_at"]),
        )

    def record_submission(
        self,
        session_id: str,
        exercise_id: str,
        passed: bool,
        duration_seconds: float,
    ) -> None:
        self._record_event(
            session_id,
            exercise_id=exercise_id,
            event_type="submission",
            success=passed,
            duration_seconds=duration_seconds,
        )

    def record_hint(self, session_id: str, exercise_id: str, level: int) -> None:
        self._record_event(
            session_id,
            exercise_id=exercise_id,
            event_type="hint",
            hint_level=level,
        )

    def record_explanation(self, session_id: str, exercise_id: str) -> None:
        self._record_event(session_id, exercise_id=exercise_id, event_type="explanation")

    def record_confidence(self, session_id: str, rating: int) -> None:
        self._record_event(session_id, event_type="confidence", confidence=rating)

    def summarize(self, session_id: str) -> LearningAnalytics | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    COUNT(CASE WHEN event_type = 'submission' THEN 1 END) AS attempts,
                    COUNT(CASE WHEN event_type = 'submission' AND success = 1 THEN 1 END)
                        AS successful_submissions,
                    COUNT(CASE WHEN event_type = 'submission' AND success = 0 THEN 1 END)
                        AS failed_attempts,
                    COUNT(DISTINCT CASE WHEN event_type = 'submission' AND success = 1
                        THEN exercise_id END) AS exercises_completed,
                    COUNT(CASE WHEN event_type = 'hint' THEN 1 END) AS hints_requested,
                    COUNT(CASE WHEN event_type = 'explanation' THEN 1 END)
                        AS explanations_requested,
                    COALESCE(SUM(CASE WHEN event_type = 'submission'
                        THEN duration_seconds ELSE 0 END), 0) AS time_spent_seconds,
                    AVG(CASE WHEN event_type = 'confidence' THEN confidence END)
                        AS average_confidence
                FROM learning_events
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()
        return LearningAnalytics(
            session_id=session.id,
            condition=session.condition,
            attempts=row["attempts"],
            successful_submissions=row["successful_submissions"],
            failed_attempts=row["failed_attempts"],
            exercises_completed=row["exercises_completed"],
            hints_requested=row["hints_requested"],
            explanations_requested=row["explanations_requested"],
            time_spent_seconds=float(row["time_spent_seconds"]),
            average_confidence=(
                float(row["average_confidence"])
                if row["average_confidence"] is not None
                else None
            ),
        )

    def _record_event(
        self,
        session_id: str,
        *,
        event_type: str,
        exercise_id: str | None = None,
        success: bool | None = None,
        hint_level: int | None = None,
        duration_seconds: float | None = None,
        confidence: int | None = None,
    ) -> None:
        self._ensure_initialized()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO learning_events (
                    session_id, exercise_id, event_type, success, hint_level,
                    duration_seconds, confidence, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    exercise_id,
                    event_type,
                    success,
                    hint_level,
                    duration_seconds,
                    confidence,
                    datetime.now(UTC).isoformat(),
                ),
            )

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return
        with self._initialization_lock:
            if self._initialized:
                return
            self._database_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as connection:
                connection.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS experiment_sessions (
                        id TEXT PRIMARY KEY,
                        condition TEXT NOT NULL CHECK (condition IN ('control', 'ai_assisted')),
                        started_at TEXT NOT NULL
                    );

                    CREATE TABLE IF NOT EXISTS learning_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL
                            REFERENCES experiment_sessions(id) ON DELETE CASCADE,
                        exercise_id TEXT,
                        event_type TEXT NOT NULL CHECK (
                            event_type IN ('submission', 'hint', 'explanation', 'confidence')
                        ),
                        success INTEGER CHECK (success IN (0, 1)),
                        hint_level INTEGER CHECK (hint_level BETWEEN 1 AND 3),
                        duration_seconds REAL CHECK (
                            duration_seconds >= 0 AND duration_seconds <= 7200
                        ),
                        confidence INTEGER CHECK (confidence BETWEEN 1 AND 5),
                        created_at TEXT NOT NULL,
                        CHECK (
                            (event_type = 'submission' AND exercise_id IS NOT NULL
                                AND success IS NOT NULL AND duration_seconds IS NOT NULL
                                AND hint_level IS NULL AND confidence IS NULL)
                            OR (event_type = 'hint' AND exercise_id IS NOT NULL
                                AND success IS NULL AND duration_seconds IS NULL
                                AND hint_level IS NOT NULL AND confidence IS NULL)
                            OR (event_type = 'explanation' AND exercise_id IS NOT NULL
                                AND success IS NULL AND duration_seconds IS NULL
                                AND hint_level IS NULL AND confidence IS NULL)
                            OR (event_type = 'confidence' AND exercise_id IS NULL
                                AND success IS NULL AND duration_seconds IS NULL
                                AND hint_level IS NULL AND confidence IS NOT NULL)
                        )
                    );

                    CREATE INDEX IF NOT EXISTS idx_learning_events_session
                        ON learning_events(session_id, created_at);
                    """
                )
            self._initialized = True
