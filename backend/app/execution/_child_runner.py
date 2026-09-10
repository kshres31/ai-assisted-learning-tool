import contextlib
import io
import json
import sys
from pathlib import Path

SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}


def serializable(value: object) -> object:
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return repr(value)


def execute(student_path: Path, payload_path: Path) -> dict[str, object]:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    namespace: dict[str, object] = {"__builtins__": SAFE_BUILTINS}
    captured_output = io.StringIO()

    try:
        compiled = compile(
            student_path.read_text(encoding="utf-8"),
            "student_submission.py",
            "exec",
        )
        with (
            contextlib.redirect_stdout(captured_output),
            contextlib.redirect_stderr(captured_output),
        ):
            exec(compiled, namespace)
        function = namespace.get(payload["function_name"])
        if not callable(function):
            return {"status": "error", "message": "Required function was not defined", "tests": []}

        outcomes = []
        for test_case in payload["tests"]:
            try:
                with contextlib.redirect_stdout(captured_output), contextlib.redirect_stderr(
                    captured_output
                ):
                    actual = function(*test_case["arguments"])
                outcomes.append(
                    {
                        "name": test_case["name"],
                        "visible": test_case["visible"],
                        "passed": actual == test_case["expected"],
                        "actual": serializable(actual),
                        "expected": test_case["expected"],
                    }
                )
            except BaseException as error:
                outcomes.append(
                    {
                        "name": test_case["name"],
                        "visible": test_case["visible"],
                        "passed": False,
                        "error_type": type(error).__name__,
                    }
                )
        status = "passed" if all(outcome["passed"] for outcome in outcomes) else "failed"
        return {"status": status, "message": "", "tests": outcomes}
    except BaseException as error:
        return {
            "status": "error",
            "message": f"{type(error).__name__}: {error}",
            "tests": [],
        }


if __name__ == "__main__":
    result = execute(Path(sys.argv[1]), Path(sys.argv[2]))
    sys.stdout.write(json.dumps(result, separators=(",", ":")))
