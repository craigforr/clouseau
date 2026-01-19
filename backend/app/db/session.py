"""Database session management."""

from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# Default database URL (SQLite for development)
DATABASE_URL = "sqlite:///./clouseau.db"
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./clouseau.db"

# Sync engine and session (for migrations and some operations)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session (for API operations)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Session:
    """Get synchronous database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for FastAPI dependency injection."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Test database configuration
_test_engine: Optional[object] = None
_test_session_maker: Optional[async_sessionmaker] = None


def configure_test_db(db_url: str = "sqlite+aiosqlite:///:memory:") -> None:
    """Configure test database (in-memory SQLite)."""
    global _test_engine, _test_session_maker, async_engine, AsyncSessionLocal

    _test_engine = create_async_engine(
        db_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    _test_session_maker = async_sessionmaker(
        _test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async_engine = _test_engine
    AsyncSessionLocal = _test_session_maker


async def init_db() -> None:
    """Initialize database tables."""
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """Drop all database tables."""
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
