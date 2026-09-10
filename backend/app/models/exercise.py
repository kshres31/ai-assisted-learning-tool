from dataclasses import dataclass
from enum import StrEnum


class Difficulty(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"


@dataclass(frozen=True)
class ExerciseTestCase:
    name: str
    arguments: tuple[object, ...]
    expected: object
    visible: bool = False


@dataclass(frozen=True)
class Exercise:
    id: str
    title: str
    description: str
    difficulty: Difficulty
    starter_code: str
    expected_behavior: str
    function_name: str
    concept_tags: tuple[str, ...]
    test_cases: tuple[ExerciseTestCase, ...]

    def __post_init__(self) -> None:
        required_text = (
            self.id,
            self.title,
            self.description,
            self.starter_code,
            self.function_name,
        )
        if any(not value.strip() for value in required_text):
            raise ValueError("Exercise text fields cannot be blank")
        if not self.concept_tags:
            raise ValueError("Exercise requires at least one concept tag")
        if not self.test_cases:
            raise ValueError("Exercise requires at least one test case")
        if not any(test_case.visible for test_case in self.test_cases):
            raise ValueError("Exercise requires at least one visible example")
