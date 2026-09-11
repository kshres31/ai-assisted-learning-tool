from fastapi import APIRouter, HTTPException, status

from app.dependencies import ExperimentServiceDependency
from app.schemas.experiment import AnalyticsResponse, ConfidenceRequest, SessionResponse
from app.services.experiment_service import SessionNotFoundError

router = APIRouter(prefix="/sessions", tags=["experiment"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(service: ExperimentServiceDependency) -> SessionResponse:
    return SessionResponse.from_domain(service.create_session())


@router.post("/{session_id}/confidence", status_code=status.HTTP_204_NO_CONTENT)
def record_confidence(
    session_id: str,
    request: ConfidenceRequest,
    service: ExperimentServiceDependency,
) -> None:
    try:
        service.record_confidence(session_id, request.rating)
    except SessionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        ) from error


@router.get("/{session_id}/analytics", response_model=AnalyticsResponse)
def get_analytics(
    session_id: str,
    service: ExperimentServiceDependency,
) -> AnalyticsResponse:
    try:
        return AnalyticsResponse.from_domain(service.analytics(session_id))
    except SessionNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        ) from error
