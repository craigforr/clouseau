"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Clouseau",
    description="An inspector for LLM interactions",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
