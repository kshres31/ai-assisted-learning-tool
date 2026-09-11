import os
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends

from app.ai.factory import select_ai_provider
from app.ai.provider import ProviderSelection
from app.content.exercises import EXERCISES
from app.database.analytics_repository import AnalyticsRepository
from app.execution.runner import ConstrainedPythonRunner
from app.services.assistance_service import AssistanceService
from app.services.exercise_catalog import ExerciseCatalog
from app.services.experiment_service import ExperimentService
from app.services.submission_service import SubmissionService


@lru_cache
def get_exercise_catalog() -> ExerciseCatalog:
    return ExerciseCatalog(EXERCISES)


ExerciseCatalogDependency = Annotated[ExerciseCatalog, Depends(get_exercise_catalog)]


@lru_cache
def get_python_runner() -> ConstrainedPythonRunner:
    return ConstrainedPythonRunner()


PythonRunnerDependency = Annotated[ConstrainedPythonRunner, Depends(get_python_runner)]


@lru_cache
def get_analytics_repository() -> AnalyticsRepository:
    database_path = Path(os.getenv("LEARNING_DB_PATH", "data/learning.db"))
    return AnalyticsRepository(database_path)


AnalyticsRepositoryDependency = Annotated[
    AnalyticsRepository,
    Depends(get_analytics_repository),
]


def get_experiment_service(repository: AnalyticsRepositoryDependency) -> ExperimentService:
    return ExperimentService(repository)


ExperimentServiceDependency = Annotated[ExperimentService, Depends(get_experiment_service)]


def get_submission_service(
    catalog: ExerciseCatalogDependency,
    runner: PythonRunnerDependency,
    experiment: ExperimentServiceDependency,
) -> SubmissionService:
    return SubmissionService(catalog, runner, experiment)


SubmissionServiceDependency = Annotated[SubmissionService, Depends(get_submission_service)]


@lru_cache
def get_ai_provider_selection() -> ProviderSelection:
    return select_ai_provider(os.getenv("AI_PROVIDER"))


def get_assistance_service(
    catalog: ExerciseCatalogDependency,
    experiment: ExperimentServiceDependency,
) -> AssistanceService:
    return AssistanceService(catalog, get_ai_provider_selection(), experiment)


AssistanceServiceDependency = Annotated[AssistanceService, Depends(get_assistance_service)]
