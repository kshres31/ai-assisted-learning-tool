from fastapi import APIRouter, HTTPException, status

from app.dependencies import AssistanceServiceDependency
from app.schemas.assistance import AssistanceResponse, ExplainRequest, HintRequest
from app.services.exercise_catalog import ExerciseNotFoundError

router = APIRouter(prefix="/exercises", tags=["assistance"])


@router.post("/{exercise_id}/hint", response_model=AssistanceResponse)
async def request_hint(
    exercise_id: str,
    request: HintRequest,
    service: AssistanceServiceDependency,
) -> AssistanceResponse:
    try:
        reply = await service.hint(exercise_id, request.code, request.level)
    except ExerciseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        ) from error
    return AssistanceResponse.from_domain(reply)


@router.post("/{exercise_id}/explain", response_model=AssistanceResponse)
async def request_explanation(
    exercise_id: str,
    request: ExplainRequest,
    service: AssistanceServiceDependency,
) -> AssistanceResponse:
    try:
        reply = await service.explain(exercise_id, request.code)
    except ExerciseNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        ) from error
    return AssistanceResponse.from_domain(reply)
