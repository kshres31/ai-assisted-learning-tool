import os
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.ai.factory import select_ai_provider
from app.ai.provider import ProviderSelection
from app.content.exercises import EXERCISES
from app.execution.runner import ConstrainedPythonRunner
from app.services.assistance_service import AssistanceService
from app.services.exercise_catalog import ExerciseCatalog
from app.services.submission_service import SubmissionService


@lru_cache
def get_exercise_catalog() -> ExerciseCatalog:
    return ExerciseCatalog(EXERCISES)


ExerciseCatalogDependency = Annotated[ExerciseCatalog, Depends(get_exercise_catalog)]


@lru_cache
def get_python_runner() -> ConstrainedPythonRunner:
    return ConstrainedPythonRunner()


def get_submission_service() -> SubmissionService:
    return SubmissionService(get_exercise_catalog(), get_python_runner())


SubmissionServiceDependency = Annotated[SubmissionService, Depends(get_submission_service)]


@lru_cache
def get_ai_provider_selection() -> ProviderSelection:
    return select_ai_provider(os.getenv("AI_PROVIDER"))


def get_assistance_service() -> AssistanceService:
    return AssistanceService(get_exercise_catalog(), get_ai_provider_selection())


AssistanceServiceDependency = Annotated[AssistanceService, Depends(get_assistance_service)]
