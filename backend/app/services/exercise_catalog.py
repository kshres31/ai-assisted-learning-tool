from collections.abc import Iterable

from app.models.exercise import Difficulty, Exercise


class ExerciseNotFoundError(LookupError):
    pass


class ExerciseCatalog:
    def __init__(self, exercises: Iterable[Exercise]) -> None:
        self._exercises = tuple(exercises)
        self._by_id = {exercise.id: exercise for exercise in self._exercises}
        if len(self._by_id) != len(self._exercises):
            raise ValueError("Exercise IDs must be unique")

    def list(
        self,
        difficulty: Difficulty | None = None,
        tag: str | None = None,
    ) -> tuple[Exercise, ...]:
        normalized_tag = tag.casefold().strip() if tag else None
        return tuple(
            exercise
            for exercise in self._exercises
            if (difficulty is None or exercise.difficulty == difficulty)
            and (
                normalized_tag is None
                or normalized_tag in {concept.casefold() for concept in exercise.concept_tags}
            )
        )

    def get(self, exercise_id: str) -> Exercise:
        try:
            return self._by_id[exercise_id]
        except KeyError as error:
            raise ExerciseNotFoundError(exercise_id) from error
