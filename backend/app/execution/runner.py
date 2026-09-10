import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from app.execution.models import ExecutionResult, ExecutionStatus, TestOutcome
from app.execution.validation import UnsafeCodeError, validate_student_code
from app.models.exercise import Exercise


class ConstrainedPythonRunner:
    def __init__(self, timeout_seconds: float = 2.0) -> None:
        if timeout_seconds <= 0:
            raise ValueError("Execution timeout must be positive")
        self._timeout_seconds = timeout_seconds
        self._child_runner = Path(__file__).with_name("_child_runner.py")

    def run(self, exercise: Exercise, code: str) -> ExecutionResult:
        try:
            validate_student_code(code)
        except UnsafeCodeError as error:
            return ExecutionResult(ExecutionStatus.REJECTED, message=str(error))

        payload = {
            "function_name": exercise.function_name,
            "tests": [
                {
                    "name": test_case.name,
                    "arguments": test_case.arguments,
                    "expected": test_case.expected,
                    "visible": test_case.visible,
                }
                for test_case in exercise.test_cases
            ],
        }
        try:
            with tempfile.TemporaryDirectory(prefix="learning-tool-") as temporary_directory:
                directory = Path(temporary_directory)
                student_path = directory / "student_submission.py"
                payload_path = directory / "tests.json"
                student_path.write_text(code, encoding="utf-8")
                payload_path.write_text(json.dumps(payload), encoding="utf-8")
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(self._child_runner),
                        str(student_path),
                        str(payload_path),
                    ],
                    cwd=directory,
                    env={"PYTHONHASHSEED": "0", "PYTHONIOENCODING": "utf-8"},
                    capture_output=True,
                    text=True,
                    timeout=self._timeout_seconds,
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                ExecutionStatus.TIMEOUT,
                message="Submission exceeded the execution time limit",
            )
        except (OSError, ValueError) as error:
            return ExecutionResult(
                ExecutionStatus.ERROR,
                message=f"Runner could not start: {type(error).__name__}",
            )

        if completed.returncode != 0:
            return ExecutionResult(
                ExecutionStatus.ERROR,
                message="The isolated runner exited unexpectedly",
            )
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            return ExecutionResult(
                ExecutionStatus.ERROR,
                message="The isolated runner returned an invalid result",
            )
        return self._to_execution_result(result)

    def _to_execution_result(self, result: dict[str, object]) -> ExecutionResult:
        status = ExecutionStatus(str(result["status"]))
        outcomes = []
        hidden_index = 0
        for test_data in result.get("tests", []):
            if not bool(test_data["visible"]):
                hidden_index += 1
            outcomes.append(self._to_outcome(test_data, hidden_index))
        return ExecutionResult(status, tuple(outcomes), str(result.get("message", "")))

    def _to_outcome(self, test_data: dict[str, object], index: int) -> TestOutcome:
        visible = bool(test_data["visible"])
        passed = bool(test_data["passed"])
        name = str(test_data["name"]) if visible else f"Hidden test {index}"
        if passed:
            message = "Passed"
        elif not visible:
            message = "Hidden test failed"
        elif "error_type" in test_data:
            message = f"Raised {test_data['error_type']}"
        else:
            message = f"Expected {test_data['expected']!r}, received {test_data['actual']!r}"
        return TestOutcome(name=name, passed=passed, message=message)
