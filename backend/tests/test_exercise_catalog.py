import pytest
from app.content.exercises import EXERCISES
from app.models.exercise import Difficulty
from app.services.exercise_catalog import ExerciseCatalog, ExerciseNotFoundError


def test_catalog_filters_by_difficulty_and_case_insensitive_tag() -> None:
    catalog = ExerciseCatalog(EXERCISES)

    beginner_ids = [exercise.id for exercise in catalog.list(difficulty=Difficulty.BEGINNER)]
    loop_ids = [exercise.id for exercise in catalog.list(tag="LOOPS")]

    assert beginner_ids == ["double-number", "sum-even-numbers"]
    assert loop_ids == ["sum-even-numbers", "word-frequencies", "first-duplicate"]


def test_catalog_rejects_unknown_exercise() -> None:
    catalog = ExerciseCatalog(EXERCISES)

    with pytest.raises(ExerciseNotFoundError):
        catalog.get("missing-exercise")
