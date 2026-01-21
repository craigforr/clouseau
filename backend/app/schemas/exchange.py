"""Pydantic schemas for Exchange API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExchangeBase(BaseModel):
    """Base schema for exchange data."""

    user_message: str = Field(..., min_length=1, description="User's message")
    assistant_message: str = Field(..., min_length=1, description="Assistant's response")
    model: Optional[str] = Field(None, max_length=100, description="Model used")
    input_tokens: Optional[int] = Field(None, ge=0, description="Input token count")
    output_tokens: Optional[int] = Field(None, ge=0, description="Output token count")


class ExchangeCreate(ExchangeBase):
    """Schema for creating a new exchange."""

    conversation_id: int = Field(..., description="ID of the parent conversation")


class ExchangeResponse(ExchangeBase):
    """Schema for exchange response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    created_at: datetime


class ExchangeListResponse(BaseModel):
    """Schema for paginated exchange list response."""

    items: list[ExchangeResponse]
    total: int
    page: int
    page_size: int
