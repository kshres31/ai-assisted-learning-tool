from pydantic import BaseModel, JsonValue

from app.models.exercise import Exercise


class ExerciseSummary(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    concept_tags: list[str]

    @classmethod
    def from_domain(cls, exercise: Exercise) -> "ExerciseSummary":
        return cls(
            id=exercise.id,
            title=exercise.title,
            description=exercise.description,
            difficulty=exercise.difficulty,
            concept_tags=list(exercise.concept_tags),
        )


class VisibleTestCase(BaseModel):
    name: str
    arguments: list[JsonValue]
    expected: JsonValue


class ExerciseDetail(ExerciseSummary):
    starter_code: str
    expected_behavior: str
    function_name: str
    visible_tests: list[VisibleTestCase]

    @classmethod
    def from_domain(cls, exercise: Exercise) -> "ExerciseDetail":
        return cls(
            **ExerciseSummary.from_domain(exercise).model_dump(),
            starter_code=exercise.starter_code,
            expected_behavior=exercise.expected_behavior,
            function_name=exercise.function_name,
            visible_tests=[
                VisibleTestCase(
                    name=test_case.name,
                    arguments=list(test_case.arguments),
                    expected=test_case.expected,
                )
                for test_case in exercise.test_cases
                if test_case.visible
            ],
        )
