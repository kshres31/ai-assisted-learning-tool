from app.content.exercises import EXERCISES
from app.execution.models import ExecutionStatus
from app.execution.runner import ConstrainedPythonRunner

EXERCISE = EXERCISES[0]


def test_runner_passes_correct_submission_and_scrubs_hidden_details() -> None:
    result = ConstrainedPythonRunner().run(
        EXERCISE,
        "def double_number(number):\n    return number * 2\n",
    )

    assert result.status is ExecutionStatus.PASSED
    assert result.passed is True
    assert [outcome.name for outcome in result.outcomes] == [
        "positive number",
        "Hidden test 1",
        "Hidden test 2",
    ]


def test_runner_returns_visible_failure_without_revealing_hidden_values() -> None:
    result = ConstrainedPythonRunner().run(
        EXERCISE,
        "def double_number(number):\n    return number + 2\n",
    )

    assert result.status is ExecutionStatus.FAILED
    assert result.outcomes[0].message == "Expected 8, received 6"
    assert result.outcomes[1].message == "Hidden test failed"
    assert "-6" not in result.outcomes[1].message


def test_runner_rejects_unsafe_syntax_before_starting_process() -> None:
    runner = ConstrainedPythonRunner()

    imported = runner.run(
        EXERCISE,
        "import os\ndef double_number(number):\n    return number * 2\n",
    )
    file_access = runner.run(EXERCISE, "def double_number(number):\n    return open('x')\n")

    assert imported.status is ExecutionStatus.REJECTED
    assert "Import" in imported.message
    assert file_access.status is ExecutionStatus.REJECTED
    assert file_access.message == "Call to 'open' is not allowed"


def test_runner_stops_submission_after_timeout() -> None:
    result = ConstrainedPythonRunner(timeout_seconds=0.5).run(
        EXERCISE,
        "def double_number(number):\n    while True:\n        pass\n",
    )

    assert result.status is ExecutionStatus.TIMEOUT
