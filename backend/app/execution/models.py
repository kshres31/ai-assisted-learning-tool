from dataclasses import dataclass
from enum import StrEnum


class ExecutionStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    REJECTED = "rejected"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class TestOutcome:
    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class ExecutionResult:
    status: ExecutionStatus
    outcomes: tuple[TestOutcome, ...] = ()
    message: str = ""

    @property
    def passed(self) -> bool:
        return self.status is ExecutionStatus.PASSED
