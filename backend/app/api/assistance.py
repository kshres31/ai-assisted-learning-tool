from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from app.dependencies import AssistanceServiceDependency
from app.schemas.assistance import AssistanceResponse, ExplainRequest, HintRequest
from app.services.exercise_catalog import ExerciseNotFoundError
from app.services.experiment_service import AssistanceUnavailableError, SessionNotFoundError

router = APIRouter(prefix="/exercises", tags=["assistance"])


@router.post("/{exercise_id}/hint", response_model=AssistanceResponse)
async def request_hint(
    exercise_id: str,
    request: HintRequest,
    service: AssistanceServiceDependency,
    session_id: Annotated[
        str | None,
        Header(alias="X-Session-ID", min_length=8, max_length=100),
    ] = None,
) -> AssistanceResponse:
    try:
        reply = await service.hint(exercise_id, request.code, request.level, session_id)
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
    except AssistanceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error
    return AssistanceResponse.from_domain(reply)


@router.post("/{exercise_id}/explain", response_model=AssistanceResponse)
async def request_explanation(
    exercise_id: str,
    request: ExplainRequest,
    service: AssistanceServiceDependency,
    session_id: Annotated[
        str | None,
        Header(alias="X-Session-ID", min_length=8, max_length=100),
    ] = None,
) -> AssistanceResponse:
    try:
        reply = await service.explain(exercise_id, request.code, session_id)
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
    except AssistanceUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error
    return AssistanceResponse.from_domain(reply)
