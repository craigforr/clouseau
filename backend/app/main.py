"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import conversations, exchanges, sessions
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    """Application lifespan handler."""
    # Initialize database tables on startup
    await init_db()
    yield


app = FastAPI(
    title="Clouseau",
    description="An inspector for LLM interactions",
    version="0.1.0",
    lifespan=lifespan,
)

# Register API routers
app.include_router(sessions.router, prefix="/api")
app.include_router(conversations.router, prefix="/api")
app.include_router(exchanges.router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
