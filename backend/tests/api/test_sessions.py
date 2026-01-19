"""API tests for session endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.api
class TestSessionEndpoints:
    """Test cases for session API endpoints."""

    async def test_create_session(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should create a new session."""
        response = await async_client.post("/api/sessions", json=sample_session_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_session_data["name"]
        assert data["description"] == sample_session_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_session_minimal(self, async_client: AsyncClient) -> None:
        """Should create a session with only required fields."""
        response = await async_client.post(
            "/api/sessions", json={"name": "Minimal Session"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Session"
        assert data["description"] is None

    async def test_create_session_invalid_name(self, async_client: AsyncClient) -> None:
        """Should reject session with empty name."""
        response = await async_client.post("/api/sessions", json={"name": ""})
        assert response.status_code == 422

    async def test_get_session(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should get a session by ID."""
        # Create session first
        create_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = create_response.json()["id"]

        # Get the session
        response = await async_client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == session_id
        assert data["name"] == sample_session_data["name"]

    async def test_get_session_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 for non-existent session."""
        response = await async_client.get("/api/sessions/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_list_sessions_empty(self, async_client: AsyncClient) -> None:
        """Should return empty list when no sessions exist."""
        response = await async_client.get("/api/sessions")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1

    async def test_list_sessions(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should list all sessions."""
        # Create multiple sessions
        for i in range(3):
            await async_client.post(
                "/api/sessions", json={"name": f"Session {i}", "description": f"Desc {i}"}
            )

        response = await async_client.get("/api/sessions")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    async def test_list_sessions_pagination(self, async_client: AsyncClient) -> None:
        """Should paginate session list."""
        # Create 5 sessions
        for i in range(5):
            await async_client.post("/api/sessions", json={"name": f"Session {i}"})

        # Get first page
        response = await async_client.get("/api/sessions?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2

        # Get second page
        response = await async_client.get("/api/sessions?page=2&page_size=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 2

    async def test_update_session(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should update a session."""
        # Create session
        create_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = create_response.json()["id"]

        # Update the session
        update_data = {"name": "Updated Name", "description": "Updated description"}
        response = await async_client.put(
            f"/api/sessions/{session_id}", json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"

    async def test_update_session_partial(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should allow partial updates."""
        # Create session
        create_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = create_response.json()["id"]

        # Update only name
        response = await async_client.put(
            f"/api/sessions/{session_id}", json={"name": "New Name Only"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name Only"
        assert data["description"] == sample_session_data["description"]

    async def test_update_session_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 when updating non-existent session."""
        response = await async_client.put(
            "/api/sessions/99999", json={"name": "Updated"}
        )
        assert response.status_code == 404

    async def test_delete_session(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should delete a session."""
        # Create session
        create_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = create_response.json()["id"]

        # Delete the session
        response = await async_client.delete(f"/api/sessions/{session_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = await async_client.get(f"/api/sessions/{session_id}")
        assert get_response.status_code == 404

    async def test_delete_session_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 when deleting non-existent session."""
        response = await async_client.delete("/api/sessions/99999")
        assert response.status_code == 404
