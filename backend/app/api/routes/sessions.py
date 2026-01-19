"""Session management routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schemas import (
    SessionCreate,
    SessionListResponse,
    SessionResponse,
    SessionUpdate,
)
from app.services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_session_service(db: AsyncSession = Depends(get_async_db)) -> SessionService:
    """Dependency to get session service."""
    return SessionService(db)


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new session",
)
async def create_session(
    data: SessionCreate,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    """Create a new session for tracking LLM interactions."""
    session = await service.create_session(data)
    return SessionResponse.model_validate(session)


@router.get(
    "",
    response_model=SessionListResponse,
    summary="List all sessions",
)
async def list_sessions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: SessionService = Depends(get_session_service),
) -> SessionListResponse:
    """Get a paginated list of all sessions."""
    sessions, total = await service.get_sessions(page=page, page_size=page_size)
    return SessionListResponse(
        items=[SessionResponse.model_validate(s) for s in sessions],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Get a session by ID",
)
async def get_session(
    session_id: int,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    """Get a specific session by its ID."""
    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )
    return SessionResponse.model_validate(session)


@router.put(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Update a session",
)
async def update_session(
    session_id: int,
    data: SessionUpdate,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    """Update an existing session."""
    session = await service.update_session(session_id, data)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )
    return SessionResponse.model_validate(session)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a session",
)
async def delete_session(
    session_id: int,
    service: SessionService = Depends(get_session_service),
) -> None:
    """Delete a session and all its conversations and exchanges."""
    deleted = await service.delete_session(session_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )
