"""Tests for database models - TDD approach."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as DBSession

from app.db.base import Base
from app.models.session import Session
from app.models.conversation import Conversation
from app.models.exchange import Exchange


@pytest.fixture
def engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(engine):
    """Create database session for testing."""
    with DBSession(engine) as session:
        yield session
        session.rollback()


class TestSessionModel:
    """Test cases for Session model."""

    def test_create_session(self, db_session: DBSession) -> None:
        """Should create a session with required fields."""
        session = Session(name="Test Session")
        db_session.add(session)
        db_session.commit()

        assert session.id is not None
        assert session.name == "Test Session"
        assert session.created_at is not None

    def test_session_has_description(self, db_session: DBSession) -> None:
        """Session should have optional description field."""
        session = Session(name="Test", description="A test session")
        db_session.add(session)
        db_session.commit()

        assert session.description == "A test session"

    def test_session_has_timestamps(self, db_session: DBSession) -> None:
        """Session should have created_at and updated_at timestamps."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        assert isinstance(session.created_at, datetime)
        assert isinstance(session.updated_at, datetime)

    def test_session_has_conversations_relationship(self, db_session: DBSession) -> None:
        """Session should have relationship to conversations."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        assert hasattr(session, "conversations")
        assert session.conversations == []


class TestConversationModel:
    """Test cases for Conversation model."""

    def test_create_conversation(self, db_session: DBSession) -> None:
        """Should create a conversation with required fields."""
        session = Session(name="Test Session")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(
            session_id=session.id,
            title="Test Conversation"
        )
        db_session.add(conversation)
        db_session.commit()

        assert conversation.id is not None
        assert conversation.session_id == session.id
        assert conversation.title == "Test Conversation"

    def test_conversation_belongs_to_session(self, db_session: DBSession) -> None:
        """Conversation should belong to a session."""
        session = Session(name="Test Session")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(
            session_id=session.id,
            title="Test"
        )
        db_session.add(conversation)
        db_session.commit()

        assert conversation.session == session
        assert conversation in session.conversations

    def test_conversation_has_exchanges_relationship(self, db_session: DBSession) -> None:
        """Conversation should have relationship to exchanges."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(session_id=session.id, title="Test")
        db_session.add(conversation)
        db_session.commit()

        assert hasattr(conversation, "exchanges")
        assert conversation.exchanges == []


class TestExchangeModel:
    """Test cases for Exchange model."""

    def test_create_exchange(self, db_session: DBSession) -> None:
        """Should create an exchange with required fields."""
        session = Session(name="Test Session")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(session_id=session.id, title="Test")
        db_session.add(conversation)
        db_session.commit()

        exchange = Exchange(
            conversation_id=conversation.id,
            user_message="Hello",
            assistant_message="Hi there!"
        )
        db_session.add(exchange)
        db_session.commit()

        assert exchange.id is not None
        assert exchange.user_message == "Hello"
        assert exchange.assistant_message == "Hi there!"

    def test_exchange_belongs_to_conversation(self, db_session: DBSession) -> None:
        """Exchange should belong to a conversation."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(session_id=session.id, title="Test")
        db_session.add(conversation)
        db_session.commit()

        exchange = Exchange(
            conversation_id=conversation.id,
            user_message="Test",
            assistant_message="Response"
        )
        db_session.add(exchange)
        db_session.commit()

        assert exchange.conversation == conversation
        assert exchange in conversation.exchanges

    def test_exchange_has_token_counts(self, db_session: DBSession) -> None:
        """Exchange should track token counts."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(session_id=session.id, title="Test")
        db_session.add(conversation)
        db_session.commit()

        exchange = Exchange(
            conversation_id=conversation.id,
            user_message="Test",
            assistant_message="Response",
            input_tokens=10,
            output_tokens=20
        )
        db_session.add(exchange)
        db_session.commit()

        assert exchange.input_tokens == 10
        assert exchange.output_tokens == 20

    def test_exchange_has_model_info(self, db_session: DBSession) -> None:
        """Exchange should store model information."""
        session = Session(name="Test")
        db_session.add(session)
        db_session.commit()

        conversation = Conversation(session_id=session.id, title="Test")
        db_session.add(conversation)
        db_session.commit()

        exchange = Exchange(
            conversation_id=conversation.id,
            user_message="Test",
            assistant_message="Response",
            model="claude-3-sonnet"
        )
        db_session.add(exchange)
        db_session.commit()

        assert exchange.model == "claude-3-sonnet"
