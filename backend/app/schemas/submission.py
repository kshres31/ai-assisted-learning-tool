from typing import Annotated

from pydantic import BaseModel, Field

from app.execution.models import ExecutionResult


class SubmissionRequest(BaseModel):
    code: Annotated[str, Field(min_length=1, max_length=8_000)]


class TestOutcomeResponse(BaseModel):
    name: str
    passed: bool
    message: str


class SubmissionResponse(BaseModel):
    status: str
    passed: bool
    tests_passed: int
    tests_total: int
    message: str
    test_results: list[TestOutcomeResponse]

    @classmethod
    def from_domain(cls, result: ExecutionResult) -> "SubmissionResponse":
        return cls(
            status=result.status,
            passed=result.passed,
            tests_passed=sum(outcome.passed for outcome in result.outcomes),
            tests_total=len(result.outcomes),
            message=result.message,
            test_results=[
                TestOutcomeResponse(
                    name=outcome.name,
                    passed=outcome.passed,
                    message=outcome.message,
                )
                for outcome in result.outcomes
            ],
        )
