"""Pydantic schemas for Conversation API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ConversationBase(BaseModel):
    """Base schema for conversation data."""

    title: str = Field(..., min_length=1, max_length=255, description="Conversation title")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""

    session_id: int = Field(..., description="ID of the parent session")


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)


class ConversationResponse(ConversationBase):
    """Schema for conversation response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    created_at: datetime
    updated_at: datetime


class ConversationListResponse(BaseModel):
    """Schema for paginated conversation list response."""

    items: list[ConversationResponse]
    total: int
    page: int
    page_size: int
