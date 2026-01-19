"""API tests for conversation endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.api
class TestConversationEndpoints:
    """Test cases for conversation API endpoints."""

    async def test_create_conversation(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should create a new conversation."""
        # Create session first
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        # Create conversation
        conv_data = {**sample_conversation_data, "session_id": session_id}
        response = await async_client.post("/api/conversations", json=conv_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_conversation_data["title"]
        assert data["session_id"] == session_id
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_conversation_invalid_session(
        self, async_client: AsyncClient, sample_conversation_data: dict
    ) -> None:
        """Should return 404 when creating conversation for non-existent session."""
        conv_data = {**sample_conversation_data, "session_id": 99999}
        response = await async_client.post("/api/conversations", json=conv_data)
        assert response.status_code == 404
        assert "session" in response.json()["detail"].lower()

    async def test_create_conversation_invalid_title(
        self, async_client: AsyncClient, sample_session_data: dict
    ) -> None:
        """Should reject conversation with empty title."""
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        response = await async_client.post(
            "/api/conversations", json={"title": "", "session_id": session_id}
        )
        assert response.status_code == 422

    async def test_get_conversation(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should get a conversation by ID."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        create_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = create_response.json()["id"]

        # Get the conversation
        response = await async_client.get(f"/api/conversations/{conv_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conv_id
        assert data["title"] == sample_conversation_data["title"]

    async def test_get_conversation_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 for non-existent conversation."""
        response = await async_client.get("/api/conversations/99999")
        assert response.status_code == 404

    async def test_list_conversations_by_session(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
    ) -> None:
        """Should list conversations for a session."""
        # Create session
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        # Create multiple conversations
        for i in range(3):
            await async_client.post(
                "/api/conversations",
                json={"title": f"Conv {i}", "session_id": session_id},
            )

        response = await async_client.get(f"/api/conversations/by-session/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    async def test_list_conversations_by_session_not_found(
        self, async_client: AsyncClient
    ) -> None:
        """Should return 404 for non-existent session."""
        response = await async_client.get("/api/conversations/by-session/99999")
        assert response.status_code == 404

    async def test_list_conversations_pagination(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
    ) -> None:
        """Should paginate conversation list."""
        # Create session and conversations
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        for i in range(5):
            await async_client.post(
                "/api/conversations",
                json={"title": f"Conv {i}", "session_id": session_id},
            )

        response = await async_client.get(
            f"/api/conversations/by-session/{session_id}?page=1&page_size=2"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5

    async def test_update_conversation(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should update a conversation."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        create_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = create_response.json()["id"]

        # Update the conversation
        response = await async_client.put(
            f"/api/conversations/{conv_id}", json={"title": "Updated Title"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    async def test_update_conversation_not_found(
        self, async_client: AsyncClient
    ) -> None:
        """Should return 404 when updating non-existent conversation."""
        response = await async_client.put(
            "/api/conversations/99999", json={"title": "Updated"}
        )
        assert response.status_code == 404

    async def test_delete_conversation(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should delete a conversation."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        create_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = create_response.json()["id"]

        # Delete the conversation
        response = await async_client.delete(f"/api/conversations/{conv_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = await async_client.get(f"/api/conversations/{conv_id}")
        assert get_response.status_code == 404

    async def test_delete_conversation_not_found(
        self, async_client: AsyncClient
    ) -> None:
        """Should return 404 when deleting non-existent conversation."""
        response = await async_client.delete("/api/conversations/99999")
        assert response.status_code == 404

    async def test_cascade_delete_session_deletes_conversations(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should delete conversations when parent session is deleted."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        create_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = create_response.json()["id"]

        # Delete the session
        await async_client.delete(f"/api/sessions/{session_id}")

        # Verify conversation is also deleted
        get_response = await async_client.get(f"/api/conversations/{conv_id}")
        assert get_response.status_code == 404
