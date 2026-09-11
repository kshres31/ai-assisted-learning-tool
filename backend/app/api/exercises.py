from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Query, status

from app.dependencies import ExerciseCatalogDependency, SubmissionServiceDependency
from app.models.exercise import Difficulty
from app.schemas.exercise import ExerciseDetail, ExerciseSummary
from app.schemas.submission import SubmissionRequest, SubmissionResponse
from app.services.exercise_catalog import ExerciseNotFoundError
from app.services.experiment_service import SessionNotFoundError

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("", response_model=list[ExerciseSummary])
def list_exercises(
    catalog: ExerciseCatalogDependency,
    difficulty: Annotated[Difficulty | None, Query()] = None,
    tag: Annotated[str | None, Query(min_length=1, max_length=40)] = None,
) -> list[ExerciseSummary]:
    return [
        ExerciseSummary.from_domain(exercise)
        for exercise in catalog.list(difficulty=difficulty, tag=tag)
    ]


@router.get("/{exercise_id}", response_model=ExerciseDetail)
def get_exercise(exercise_id: str, catalog: ExerciseCatalogDependency) -> ExerciseDetail:
    try:
        exercise = catalog.get(exercise_id)
    except ExerciseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        ) from error
    return ExerciseDetail.from_domain(exercise)


@router.post("/{exercise_id}/submit", response_model=SubmissionResponse)
def submit_exercise(
    exercise_id: str,
    submission: SubmissionRequest,
    service: SubmissionServiceDependency,
    session_id: Annotated[
        str | None,
        Header(alias="X-Session-ID", min_length=8, max_length=100),
    ] = None,
) -> SubmissionResponse:
    try:
        result = service.submit(
            exercise_id,
            submission.code,
            session_id=session_id,
            duration_seconds=submission.duration_seconds,
        )
    except ExerciseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        ) from error
    except SessionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        ) from error
    return SubmissionResponse.from_domain(result)
