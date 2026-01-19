"""Pydantic schemas for Session API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SessionBase(BaseModel):
    """Base schema for session data."""

    name: str = Field(..., min_length=1, max_length=255, description="Session name")
    description: Optional[str] = Field(None, description="Optional session description")


class SessionCreate(SessionBase):
    """Schema for creating a new session."""

    pass


class SessionUpdate(BaseModel):
    """Schema for updating a session."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class SessionResponse(SessionBase):
    """Schema for session response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class SessionListResponse(BaseModel):
    """Schema for paginated session list response."""

    items: list[SessionResponse]
    total: int
    page: int
    page_size: int
