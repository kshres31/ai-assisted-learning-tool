from app.execution.models import ExecutionResult
from app.execution.runner import ConstrainedPythonRunner
from app.services.exercise_catalog import ExerciseCatalog
from app.services.experiment_service import ExperimentService


class SubmissionService:
    def __init__(
        self,
        catalog: ExerciseCatalog,
        runner: ConstrainedPythonRunner,
        experiment: ExperimentService,
    ) -> None:
        self._catalog = catalog
        self._runner = runner
        self._experiment = experiment

    def submit(
        self,
        exercise_id: str,
        code: str,
        *,
        session_id: str | None = None,
        duration_seconds: float = 0,
    ) -> ExecutionResult:
        exercise = self._catalog.get(exercise_id)
        result = self._runner.run(exercise, code)
        if session_id is not None:
            self._experiment.record_submission(
                session_id,
                exercise_id,
                result.passed,
                duration_seconds,
            )
        return result
