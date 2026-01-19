"""API tests for exchange endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.api
class TestExchangeEndpoints:
    """Test cases for exchange API endpoints."""

    async def test_create_exchange(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
        sample_exchange_data: dict,
    ) -> None:
        """Should create a new exchange."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Create exchange
        exchange_data = {**sample_exchange_data, "conversation_id": conv_id}
        response = await async_client.post("/api/exchanges", json=exchange_data)
        assert response.status_code == 201
        data = response.json()
        assert data["user_message"] == sample_exchange_data["user_message"]
        assert data["assistant_message"] == sample_exchange_data["assistant_message"]
        assert data["model"] == sample_exchange_data["model"]
        assert data["input_tokens"] == sample_exchange_data["input_tokens"]
        assert data["output_tokens"] == sample_exchange_data["output_tokens"]
        assert data["conversation_id"] == conv_id
        assert "id" in data
        assert "created_at" in data

    async def test_create_exchange_minimal(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should create exchange with only required fields."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Create minimal exchange
        exchange_data = {
            "user_message": "Hello",
            "assistant_message": "Hi there!",
            "conversation_id": conv_id,
        }
        response = await async_client.post("/api/exchanges", json=exchange_data)
        assert response.status_code == 201
        data = response.json()
        assert data["model"] is None
        assert data["input_tokens"] is None
        assert data["output_tokens"] is None

    async def test_create_exchange_invalid_conversation(
        self, async_client: AsyncClient, sample_exchange_data: dict
    ) -> None:
        """Should return 404 when creating exchange for non-existent conversation."""
        exchange_data = {**sample_exchange_data, "conversation_id": 99999}
        response = await async_client.post("/api/exchanges", json=exchange_data)
        assert response.status_code == 404
        assert "conversation" in response.json()["detail"].lower()

    async def test_create_exchange_empty_message(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should reject exchange with empty messages."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Try to create exchange with empty user message
        response = await async_client.post(
            "/api/exchanges",
            json={
                "user_message": "",
                "assistant_message": "Response",
                "conversation_id": conv_id,
            },
        )
        assert response.status_code == 422

    async def test_get_exchange(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
        sample_exchange_data: dict,
    ) -> None:
        """Should get an exchange by ID."""
        # Create session, conversation, and exchange
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        exchange_data = {**sample_exchange_data, "conversation_id": conv_id}
        create_response = await async_client.post("/api/exchanges", json=exchange_data)
        exchange_id = create_response.json()["id"]

        # Get the exchange
        response = await async_client.get(f"/api/exchanges/{exchange_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == exchange_id
        assert data["user_message"] == sample_exchange_data["user_message"]

    async def test_get_exchange_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 for non-existent exchange."""
        response = await async_client.get("/api/exchanges/99999")
        assert response.status_code == 404

    async def test_list_exchanges_by_conversation(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should list exchanges for a conversation."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Create multiple exchanges
        for i in range(3):
            await async_client.post(
                "/api/exchanges",
                json={
                    "user_message": f"Message {i}",
                    "assistant_message": f"Response {i}",
                    "conversation_id": conv_id,
                },
            )

        response = await async_client.get(f"/api/exchanges/by-conversation/{conv_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 3

    async def test_list_exchanges_by_conversation_not_found(
        self, async_client: AsyncClient
    ) -> None:
        """Should return 404 for non-existent conversation."""
        response = await async_client.get("/api/exchanges/by-conversation/99999")
        assert response.status_code == 404

    async def test_list_exchanges_ordered_by_created_at(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should return exchanges ordered by creation time (oldest first)."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Create exchanges in order
        for i in range(3):
            await async_client.post(
                "/api/exchanges",
                json={
                    "user_message": f"Message {i}",
                    "assistant_message": f"Response {i}",
                    "conversation_id": conv_id,
                },
            )

        response = await async_client.get(f"/api/exchanges/by-conversation/{conv_id}")
        data = response.json()
        # Should be ordered oldest first
        assert data["items"][0]["user_message"] == "Message 0"
        assert data["items"][2]["user_message"] == "Message 2"

    async def test_list_exchanges_pagination(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
    ) -> None:
        """Should paginate exchange list."""
        # Create session and conversation
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        # Create 5 exchanges
        for i in range(5):
            await async_client.post(
                "/api/exchanges",
                json={
                    "user_message": f"Message {i}",
                    "assistant_message": f"Response {i}",
                    "conversation_id": conv_id,
                },
            )

        response = await async_client.get(
            f"/api/exchanges/by-conversation/{conv_id}?page=1&page_size=2"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5

    async def test_delete_exchange(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
        sample_exchange_data: dict,
    ) -> None:
        """Should delete an exchange."""
        # Create session, conversation, and exchange
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        exchange_data = {**sample_exchange_data, "conversation_id": conv_id}
        create_response = await async_client.post("/api/exchanges", json=exchange_data)
        exchange_id = create_response.json()["id"]

        # Delete the exchange
        response = await async_client.delete(f"/api/exchanges/{exchange_id}")
        assert response.status_code == 204

        # Verify it's deleted
        get_response = await async_client.get(f"/api/exchanges/{exchange_id}")
        assert get_response.status_code == 404

    async def test_delete_exchange_not_found(self, async_client: AsyncClient) -> None:
        """Should return 404 when deleting non-existent exchange."""
        response = await async_client.delete("/api/exchanges/99999")
        assert response.status_code == 404

    async def test_cascade_delete_conversation_deletes_exchanges(
        self,
        async_client: AsyncClient,
        sample_session_data: dict,
        sample_conversation_data: dict,
        sample_exchange_data: dict,
    ) -> None:
        """Should delete exchanges when parent conversation is deleted."""
        # Create session, conversation, and exchange
        session_response = await async_client.post(
            "/api/sessions", json=sample_session_data
        )
        session_id = session_response.json()["id"]

        conv_data = {**sample_conversation_data, "session_id": session_id}
        conv_response = await async_client.post("/api/conversations", json=conv_data)
        conv_id = conv_response.json()["id"]

        exchange_data = {**sample_exchange_data, "conversation_id": conv_id}
        create_response = await async_client.post("/api/exchanges", json=exchange_data)
        exchange_id = create_response.json()["id"]

        # Delete the conversation
        await async_client.delete(f"/api/conversations/{conv_id}")

        # Verify exchange is also deleted
        get_response = await async_client.get(f"/api/exchanges/{exchange_id}")
        assert get_response.status_code == 404
