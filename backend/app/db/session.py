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


def get_db() -> Session:  # pragma: no cover
    """Get synchronous database session (used for migrations)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:  # pragma: no cover
    """Get async database session for FastAPI dependency injection."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:  # pragma: no cover
    """Initialize database tables."""
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:  # pragma: no cover
    """Drop all database tables."""
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
