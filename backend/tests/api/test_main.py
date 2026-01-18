"""API tests for main application."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestMainApp:
    """Test cases for main FastAPI application."""

    def test_app_title(self) -> None:
        """App should have correct title."""
        assert app.title == "Clouseau"

    def test_app_version(self) -> None:
        """App should have correct version."""
        assert app.version == "0.1.0"

    def test_app_description(self) -> None:
        """App should have correct description."""
        assert "LLM" in app.description


@pytest.mark.api
class TestAPIEndpoints:
    """Test cases for API endpoints."""

    def test_health_endpoint_exists(self, client: TestClient) -> None:
        """Health endpoint should exist and be accessible."""
        response = client.get("/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_async_health_check(self, async_client) -> None:
        """Health check should work with async client."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
