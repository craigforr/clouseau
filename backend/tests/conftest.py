"""Pytest configuration and fixtures."""

import asyncio
import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.session import get_async_db

# Import all models to register them with SQLAlchemy metadata
from app.models.session import Session  # noqa: F401
from app.models.conversation import Conversation  # noqa: F401
from app.models.exchange import Exchange  # noqa: F401

# Import app AFTER models are registered
from app.main import app


# Use a temporary file for the test database to avoid connection sharing issues
_test_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
_test_db_file.close()
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{_test_db_file.name}"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=NullPool,  # NullPool doesn't keep connections, preventing hangs
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_async_db():
    """Override database dependency for tests."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Override the dependency at module load time
app.dependency_overrides[get_async_db] = override_get_async_db


def pytest_sessionfinish(session, exitstatus):
    """Clean up test database file after all tests complete."""
    try:
        os.unlink(_test_db_file.name)
    except OSError:
        pass


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up and tear down test database for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for FastAPI."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncClient:
    """Async test client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session() -> AsyncSession:
    """Get a test database session."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def sample_session_data() -> dict:
    """Sample session data for testing."""
    return {
        "name": "Test Session",
        "description": "A test session",
    }


@pytest.fixture
def sample_conversation_data() -> dict:
    """Sample conversation data for testing."""
    return {
        "title": "Test Conversation",
    }


@pytest.fixture
def sample_exchange_data() -> dict:
    """Sample exchange data for testing."""
    return {
        "user_message": "Hello, how are you?",
        "assistant_message": "I'm doing well, thank you for asking!",
        "model": "claude-3-opus",
        "input_tokens": 10,
        "output_tokens": 15,
    }
