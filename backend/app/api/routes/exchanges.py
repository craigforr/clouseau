"""Exchange management routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schemas import (
    ExchangeCreate,
    ExchangeListResponse,
    ExchangeResponse,
)
from app.services.session_service import SessionService

router = APIRouter(prefix="/exchanges", tags=["exchanges"])


def get_session_service(db: AsyncSession = Depends(get_async_db)) -> SessionService:
    """Dependency to get session service."""
    return SessionService(db)


@router.post(
    "",
    response_model=ExchangeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new exchange",
)
async def create_exchange(
    data: ExchangeCreate,
    service: SessionService = Depends(get_session_service),
) -> ExchangeResponse:
    """Create a new exchange (user message + assistant response) within a conversation."""
    exchange = await service.create_exchange(data)
    if not exchange:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {data.conversation_id} not found",
        )
    return ExchangeResponse.model_validate(exchange)


@router.get(
    "/by-conversation/{conversation_id}",
    response_model=ExchangeListResponse,
    summary="List exchanges by conversation",
)
async def list_exchanges_by_conversation(
    conversation_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    service: SessionService = Depends(get_session_service),
) -> ExchangeListResponse:
    """Get a paginated list of exchanges for a conversation."""
    # Verify conversation exists
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {conversation_id} not found",
        )

    exchanges, total = await service.get_exchanges_by_conversation(
        conversation_id=conversation_id, page=page, page_size=page_size
    )
    return ExchangeListResponse(
        items=[ExchangeResponse.model_validate(e) for e in exchanges],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{exchange_id}",
    response_model=ExchangeResponse,
    summary="Get an exchange by ID",
)
async def get_exchange(
    exchange_id: int,
    service: SessionService = Depends(get_session_service),
) -> ExchangeResponse:
    """Get a specific exchange by its ID."""
    exchange = await service.get_exchange(exchange_id)
    if not exchange:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exchange with id {exchange_id} not found",
        )
    return ExchangeResponse.model_validate(exchange)


@router.delete(
    "/{exchange_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an exchange",
)
async def delete_exchange(
    exchange_id: int,
    service: SessionService = Depends(get_session_service),
) -> None:
    """Delete an exchange."""
    deleted = await service.delete_exchange(exchange_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exchange with id {exchange_id} not found",
        )
