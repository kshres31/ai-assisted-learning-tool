from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.content.exercises import EXERCISES
from app.services.exercise_catalog import ExerciseCatalog


@lru_cache
def get_exercise_catalog() -> ExerciseCatalog:
    return ExerciseCatalog(EXERCISES)


ExerciseCatalogDependency = Annotated[ExerciseCatalog, Depends(get_exercise_catalog)]
