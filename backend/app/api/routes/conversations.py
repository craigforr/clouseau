"""Conversation management routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schemas import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
    ConversationUpdate,
)
from app.services.session_service import SessionService

router = APIRouter(prefix="/conversations", tags=["conversations"])


def get_session_service(db: AsyncSession = Depends(get_async_db)) -> SessionService:
    """Dependency to get session service."""
    return SessionService(db)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conversation",
)
async def create_conversation(
    data: ConversationCreate,
    service: SessionService = Depends(get_session_service),
) -> ConversationResponse:
    """Create a new conversation within a session."""
    conversation = await service.create_conversation(data)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {data.session_id} not found",
        )
    return ConversationResponse.model_validate(conversation)


@router.get(
    "/by-session/{session_id}",
    response_model=ConversationListResponse,
    summary="List conversations by session",
)
async def list_conversations_by_session(
    session_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    service: SessionService = Depends(get_session_service),
) -> ConversationListResponse:
    """Get a paginated list of conversations for a session."""
    # Verify session exists
    session = await service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found",
        )

    conversations, total = await service.get_conversations_by_session(
        session_id=session_id, page=page, page_size=page_size
    )
    return ConversationListResponse(
        items=[ConversationResponse.model_validate(c) for c in conversations],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get a conversation by ID",
)
async def get_conversation(
    conversation_id: int,
    service: SessionService = Depends(get_session_service),
) -> ConversationResponse:
    """Get a specific conversation by its ID."""
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found",
        )
    return ConversationResponse.model_validate(conversation)


@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Update a conversation",
)
async def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    service: SessionService = Depends(get_session_service),
) -> ConversationResponse:
    """Update an existing conversation."""
    conversation = await service.update_conversation(conversation_id, data)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found",
        )
    return ConversationResponse.model_validate(conversation)


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conversation",
)
async def delete_conversation(
    conversation_id: int,
    service: SessionService = Depends(get_session_service),
) -> None:
    """Delete a conversation and all its exchanges."""
    deleted = await service.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found",
        )
