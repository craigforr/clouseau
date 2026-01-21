"""Integration tests for Anthropic provider with real API.

These tests are skipped unless ANTHROPIC_API_KEY is set in the environment.
Run with: ANTHROPIC_API_KEY=your-key pytest tests/integration/ -v
"""

import os

import pytest

from app.services.llm_providers.anthropic import AnthropicProvider
from app.services.llm_providers.base import LLMMessage, ProviderConfig


# Skip all tests in this module if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY environment variable not set",
)


@pytest.fixture
def provider() -> AnthropicProvider:
    """Create provider with real API key."""
    config = ProviderConfig(
        name="anthropic-integration-test",
        model="claude-3-5-haiku-20241022",  # Use cheapest model for tests
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        max_tokens=100,  # Keep responses short for cost
        temperature=0.0,  # Deterministic
    )
    return AnthropicProvider(config)


class TestAnthropicIntegration:
    """Integration tests with real Anthropic API."""

    @pytest.mark.asyncio
    async def test_send_message_real_api(self, provider: AnthropicProvider) -> None:
        """Should get real response from Claude API."""
        messages = [
            LLMMessage(role="user", content="Reply with exactly: INTEGRATION_TEST_OK"),
        ]

        response = await provider.send_message(messages)

        assert response.content is not None
        assert len(response.content) > 0
        assert response.input_tokens > 0
        assert response.output_tokens > 0
        assert "claude" in response.model.lower()

    @pytest.mark.asyncio
    async def test_stream_message_real_api(self, provider: AnthropicProvider) -> None:
        """Should stream real response from Claude API."""
        messages = [
            LLMMessage(role="user", content="Count from 1 to 3, one number per line."),
        ]

        chunks = []
        async for chunk in provider.stream_message(messages):
            chunks.append(chunk)

        full_response = "".join(chunks)
        assert len(full_response) > 0
        assert "1" in full_response

    @pytest.mark.asyncio
    async def test_send_message_with_system(self, provider: AnthropicProvider) -> None:
        """Should handle system message correctly."""
        messages = [
            LLMMessage(role="system", content="You are a helpful assistant. Always start responses with 'HELLO:'"),
            LLMMessage(role="user", content="Say hi"),
        ]

        response = await provider.send_message(messages)

        assert response.content is not None
        assert len(response.content) > 0
