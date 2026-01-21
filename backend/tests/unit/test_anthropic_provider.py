"""Tests for Anthropic LLM provider."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.llm_providers.anthropic import AnthropicProvider
from app.services.llm_providers.base import (
    LLMMessage,
    LLMResponse,
    ModelInfo,
    ProviderConfig,
)


@pytest.fixture
def provider_config() -> ProviderConfig:
    """Create test provider configuration."""
    return ProviderConfig(
        name="test-anthropic",
        model="claude-3-5-sonnet-20241022",
        api_key="test-api-key",
        max_tokens=4096,
        temperature=1.0,
        timeout=60,
    )


@pytest.fixture
def provider(provider_config: ProviderConfig) -> AnthropicProvider:
    """Create test provider instance."""
    return AnthropicProvider(provider_config)


class TestAnthropicProviderInit:
    """Test AnthropicProvider initialization."""

    def test_init_with_api_key(self, provider_config: ProviderConfig) -> None:
        """Should initialize with API key from config."""
        provider = AnthropicProvider(provider_config)
        assert provider.config == provider_config

    def test_init_creates_client(self, provider_config: ProviderConfig) -> None:
        """Should create Anthropic client on init."""
        with patch("app.services.llm_providers.anthropic.Anthropic") as mock_client:
            provider = AnthropicProvider(provider_config)
            mock_client.assert_called_once_with(api_key="test-api-key")


class TestSendMessage:
    """Test send_message method."""

    @pytest.mark.asyncio
    async def test_send_message_returns_response(
        self, provider: AnthropicProvider
    ) -> None:
        """Should return LLMResponse with content."""
        messages = [LLMMessage(role="user", content="Hello, Claude!")]

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello! How can I help you?")]
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.usage.input_tokens = 10
        mock_response.usage.output_tokens = 8
        mock_response.stop_reason = "end_turn"

        with patch.object(
            provider._client.messages, "create", return_value=mock_response
        ):
            response = await provider.send_message(messages)

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello! How can I help you?"
        assert response.model == "claude-3-5-sonnet-20241022"
        assert response.input_tokens == 10
        assert response.output_tokens == 8

    @pytest.mark.asyncio
    async def test_send_message_formats_messages(
        self, provider: AnthropicProvider
    ) -> None:
        """Should format messages correctly for Anthropic API."""
        messages = [
            LLMMessage(role="system", content="You are a helpful assistant."),
            LLMMessage(role="user", content="Hi there!"),
        ]

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello!")]
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.usage.input_tokens = 15
        mock_response.usage.output_tokens = 5
        mock_response.stop_reason = "end_turn"

        with patch.object(
            provider._client.messages, "create", return_value=mock_response
        ) as mock_create:
            await provider.send_message(messages)

        # Verify system message is passed as system parameter
        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs["system"] == "You are a helpful assistant."
        # Verify user message is in messages list
        assert len(call_kwargs["messages"]) == 1
        assert call_kwargs["messages"][0]["role"] == "user"
        assert call_kwargs["messages"][0]["content"] == "Hi there!"


class TestStreamMessage:
    """Test stream_message method."""

    @pytest.mark.asyncio
    async def test_stream_message_yields_chunks(
        self, provider: AnthropicProvider
    ) -> None:
        """Should yield content chunks from streaming response."""
        messages = [LLMMessage(role="user", content="Tell me a story")]

        # Create mock stream events
        mock_delta1 = MagicMock()
        mock_delta1.type = "content_block_delta"
        mock_delta1.delta.text = "Once "

        mock_delta2 = MagicMock()
        mock_delta2.type = "content_block_delta"
        mock_delta2.delta.text = "upon "

        mock_delta3 = MagicMock()
        mock_delta3.type = "content_block_delta"
        mock_delta3.delta.text = "a time..."

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.__iter__ = MagicMock(
            return_value=iter([mock_delta1, mock_delta2, mock_delta3])
        )

        with patch.object(
            provider._client.messages, "stream", return_value=mock_stream
        ):
            chunks = []
            async for chunk in provider.stream_message(messages):
                chunks.append(chunk)

        assert chunks == ["Once ", "upon ", "a time..."]


class TestCountTokens:
    """Test token counting."""

    def test_count_tokens_estimates_correctly(
        self, provider: AnthropicProvider
    ) -> None:
        """Should estimate tokens (~4 chars per token)."""
        # Short text
        assert provider.count_tokens("Hello") >= 1

        # Longer text (roughly 100 chars = ~25 tokens)
        long_text = "a" * 100
        tokens = provider.count_tokens(long_text)
        assert 20 <= tokens <= 30

    def test_count_tokens_empty_string(self, provider: AnthropicProvider) -> None:
        """Should return at least 1 for empty string."""
        assert provider.count_tokens("") >= 1


class TestGetModelInfo:
    """Test get_model_info method."""

    def test_get_model_info_returns_correct_info(
        self, provider: AnthropicProvider
    ) -> None:
        """Should return ModelInfo with correct details."""
        info = provider.get_model_info()

        assert isinstance(info, ModelInfo)
        assert info.name == "claude-3-5-sonnet-20241022"
        assert info.provider == "anthropic"
        assert info.max_context_tokens == 200000
        assert info.supports_streaming is True
        assert info.supports_vision is True
        assert info.supports_function_calling is True


class TestValidateConfig:
    """Test configuration validation."""

    def test_validate_config_valid(self, provider: AnthropicProvider) -> None:
        """Should return True for valid config."""
        assert provider.validate_config() is True

    def test_validate_config_missing_api_key(
        self, provider_config: ProviderConfig
    ) -> None:
        """Should return False when API key is missing."""
        provider_config.api_key = None
        provider = AnthropicProvider(provider_config)
        assert provider.validate_config() is False

    def test_validate_config_empty_api_key(
        self, provider_config: ProviderConfig
    ) -> None:
        """Should return False when API key is empty."""
        provider_config.api_key = ""
        provider = AnthropicProvider(provider_config)
        assert provider.validate_config() is False


class TestSendMessageBranches:
    """Test send_message edge cases for full coverage."""

    @pytest.mark.asyncio
    async def test_send_message_without_system_message(
        self, provider: AnthropicProvider
    ) -> None:
        """Should work without system message."""
        messages = [LLMMessage(role="user", content="Hello!")]

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hi there!")]
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 3
        mock_response.stop_reason = "end_turn"

        with patch.object(
            provider._client.messages, "create", return_value=mock_response
        ) as mock_create:
            response = await provider.send_message(messages)

        # Verify system is not in kwargs when no system message
        call_kwargs = mock_create.call_args.kwargs
        assert "system" not in call_kwargs
        assert response.content == "Hi there!"

    @pytest.mark.asyncio
    async def test_send_message_empty_content(
        self, provider: AnthropicProvider
    ) -> None:
        """Should handle empty response content."""
        messages = [LLMMessage(role="user", content="Hello!")]

        mock_response = MagicMock()
        mock_response.content = []
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 0
        mock_response.stop_reason = "end_turn"

        with patch.object(
            provider._client.messages, "create", return_value=mock_response
        ):
            response = await provider.send_message(messages)

        assert response.content == ""

    @pytest.mark.asyncio
    async def test_send_message_with_no_temperature(
        self, provider_config: ProviderConfig
    ) -> None:
        """Should work with temperature set to None."""
        provider_config.temperature = None
        provider = AnthropicProvider(provider_config)

        messages = [LLMMessage(role="user", content="Hello!")]

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hi!")]
        mock_response.model = "claude-3-5-sonnet-20241022"
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 2
        mock_response.stop_reason = "end_turn"

        with patch.object(
            provider._client.messages, "create", return_value=mock_response
        ) as mock_create:
            await provider.send_message(messages)

        # Verify temperature is not in kwargs when None
        call_kwargs = mock_create.call_args.kwargs
        assert "temperature" not in call_kwargs


class TestStreamMessageBranches:
    """Test stream_message edge cases for full coverage."""

    @pytest.mark.asyncio
    async def test_stream_message_without_system_message(
        self, provider: AnthropicProvider
    ) -> None:
        """Should work without system message."""
        messages = [LLMMessage(role="user", content="Hello")]

        mock_delta = MagicMock()
        mock_delta.type = "content_block_delta"
        mock_delta.delta.text = "Hi"

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_delta]))

        with patch.object(
            provider._client.messages, "stream", return_value=mock_stream
        ) as mock_stream_call:
            chunks = []
            async for chunk in provider.stream_message(messages):
                chunks.append(chunk)

        # Verify system is not in kwargs
        call_kwargs = mock_stream_call.call_args.kwargs
        assert "system" not in call_kwargs
        assert chunks == ["Hi"]

    @pytest.mark.asyncio
    async def test_stream_message_skips_non_delta_events(
        self, provider: AnthropicProvider
    ) -> None:
        """Should skip events that are not content_block_delta."""
        messages = [LLMMessage(role="user", content="Hello")]

        mock_delta1 = MagicMock()
        mock_delta1.type = "message_start"

        mock_delta2 = MagicMock()
        mock_delta2.type = "content_block_delta"
        mock_delta2.delta.text = "Hi"

        mock_delta3 = MagicMock()
        mock_delta3.type = "message_end"

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.__iter__ = MagicMock(
            return_value=iter([mock_delta1, mock_delta2, mock_delta3])
        )

        with patch.object(
            provider._client.messages, "stream", return_value=mock_stream
        ):
            chunks = []
            async for chunk in provider.stream_message(messages):
                chunks.append(chunk)

        # Only the content_block_delta should yield content
        assert chunks == ["Hi"]

    @pytest.mark.asyncio
    async def test_stream_message_with_no_temperature(
        self, provider_config: ProviderConfig
    ) -> None:
        """Should work with temperature set to None."""
        provider_config.temperature = None
        provider = AnthropicProvider(provider_config)

        messages = [LLMMessage(role="user", content="Hello")]

        mock_delta = MagicMock()
        mock_delta.type = "content_block_delta"
        mock_delta.delta.text = "Hi"

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_delta]))

        with patch.object(
            provider._client.messages, "stream", return_value=mock_stream
        ) as mock_stream_call:
            async for _ in provider.stream_message(messages):
                pass

        # Verify temperature is not in kwargs when None
        call_kwargs = mock_stream_call.call_args.kwargs
        assert "temperature" not in call_kwargs

    @pytest.mark.asyncio
    async def test_stream_message_with_system_message(
        self, provider: AnthropicProvider
    ) -> None:
        """Should pass system message to stream API."""
        messages = [
            LLMMessage(role="system", content="Be helpful"),
            LLMMessage(role="user", content="Hello"),
        ]

        mock_delta = MagicMock()
        mock_delta.type = "content_block_delta"
        mock_delta.delta.text = "Hi"

        mock_stream = MagicMock()
        mock_stream.__enter__ = MagicMock(return_value=mock_stream)
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.__iter__ = MagicMock(return_value=iter([mock_delta]))

        with patch.object(
            provider._client.messages, "stream", return_value=mock_stream
        ) as mock_stream_call:
            async for _ in provider.stream_message(messages):
                pass

        call_kwargs = mock_stream_call.call_args.kwargs
        assert call_kwargs["system"] == "Be helpful"
