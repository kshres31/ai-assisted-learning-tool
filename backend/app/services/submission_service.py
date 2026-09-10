from app.execution.models import ExecutionResult
from app.execution.runner import ConstrainedPythonRunner
from app.services.exercise_catalog import ExerciseCatalog


class SubmissionService:
    def __init__(self, catalog: ExerciseCatalog, runner: ConstrainedPythonRunner) -> None:
        self._catalog = catalog
        self._runner = runner

    def submit(self, exercise_id: str, code: str) -> ExecutionResult:
        exercise = self._catalog.get(exercise_id)
        return self._runner.run(exercise, code)
