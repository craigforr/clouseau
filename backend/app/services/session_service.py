"""Session management service."""

from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation
from app.models.exchange import Exchange
from app.models.session import Session
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.schemas.exchange import ExchangeCreate
from app.schemas.session import SessionCreate, SessionUpdate


class SessionService:
    """Service for managing sessions, conversations, and exchanges."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize service with database session."""
        self.db = db

    # Session operations
    async def create_session(self, data: SessionCreate) -> Session:
        """Create a new session."""
        session = Session(name=data.name, description=data.description)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: int) -> Optional[Session]:
        """Get a session by ID."""
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()

    async def get_sessions(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[Sequence[Session], int]:
        """Get paginated list of sessions."""
        # Get total count
        count_result = await self.db.execute(select(func.count(Session.id)))
        total = count_result.scalar_one()

        # Get paginated results
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Session)
            .order_by(Session.updated_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        sessions = result.scalars().all()
        return sessions, total

    async def update_session(
        self, session_id: int, data: SessionUpdate
    ) -> Optional[Session]:
        """Update a session."""
        session = await self.get_session(session_id)
        if not session:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(session, field, value)

        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session."""
        session = await self.get_session(session_id)
        if not session:
            return False

        await self.db.delete(session)
        await self.db.commit()
        return True

    # Conversation operations
    async def create_conversation(self, data: ConversationCreate) -> Optional[Conversation]:
        """Create a new conversation in a session."""
        # Verify session exists
        session = await self.get_session(data.session_id)
        if not session:
            return None

        conversation = Conversation(session_id=data.session_id, title=data.title)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get a conversation by ID."""
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def get_conversations_by_session(
        self, session_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[Sequence[Conversation], int]:
        """Get paginated list of conversations for a session."""
        # Get total count
        count_result = await self.db.execute(
            select(func.count(Conversation.id)).where(
                Conversation.session_id == session_id
            )
        )
        total = count_result.scalar_one()

        # Get paginated results
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.session_id == session_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        conversations = result.scalars().all()
        return conversations, total

    async def update_conversation(
        self, conversation_id: int, data: ConversationUpdate
    ) -> Optional[Conversation]:
        """Update a conversation."""
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)

        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation."""
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            return False

        await self.db.delete(conversation)
        await self.db.commit()
        return True

    # Exchange operations
    async def create_exchange(self, data: ExchangeCreate) -> Optional[Exchange]:
        """Create a new exchange in a conversation."""
        # Verify conversation exists
        conversation = await self.get_conversation(data.conversation_id)
        if not conversation:
            return None

        exchange = Exchange(
            conversation_id=data.conversation_id,
            user_message=data.user_message,
            assistant_message=data.assistant_message,
            model=data.model,
            input_tokens=data.input_tokens,
            output_tokens=data.output_tokens,
        )
        self.db.add(exchange)
        await self.db.commit()
        await self.db.refresh(exchange)
        return exchange

    async def get_exchange(self, exchange_id: int) -> Optional[Exchange]:
        """Get an exchange by ID."""
        result = await self.db.execute(
            select(Exchange).where(Exchange.id == exchange_id)
        )
        return result.scalar_one_or_none()

    async def get_exchanges_by_conversation(
        self, conversation_id: int, page: int = 1, page_size: int = 50
    ) -> tuple[Sequence[Exchange], int]:
        """Get paginated list of exchanges for a conversation."""
        # Get total count
        count_result = await self.db.execute(
            select(func.count(Exchange.id)).where(
                Exchange.conversation_id == conversation_id
            )
        )
        total = count_result.scalar_one()

        # Get paginated results (ordered by creation time, oldest first)
        offset = (page - 1) * page_size
        result = await self.db.execute(
            select(Exchange)
            .where(Exchange.conversation_id == conversation_id)
            .order_by(Exchange.created_at.asc())
            .offset(offset)
            .limit(page_size)
        )
        exchanges = result.scalars().all()
        return exchanges, total

    async def delete_exchange(self, exchange_id: int) -> bool:
        """Delete an exchange."""
        exchange = await self.get_exchange(exchange_id)
        if not exchange:
            return False

        await self.db.delete(exchange)
        await self.db.commit()
        return True
