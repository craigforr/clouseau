"""Tests for health check endpoint."""

import pytest
from fastapi.testclient import TestClient


class TestHealthCheck:
    """Test cases for health check endpoint."""

    def test_health_check_returns_200(self, client: TestClient) -> None:
        """Health check endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self, client: TestClient) -> None:
        """Health check endpoint should return healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_check_response_format(self, client: TestClient) -> None:
        """Health check response should have correct format."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert isinstance(data["status"], str)
