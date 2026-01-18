"""Tests for LLM provider base class and mock provider - TDD approach."""

import pytest
from typing import AsyncGenerator

from app.services.llm_providers.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    ModelInfo,
    ProviderConfig,
)
from app.services.llm_providers.mock import MockLLMProvider


class TestLLMMessage:
    """Test cases for LLM message model."""

    def test_create_user_message(self) -> None:
        """Should create a user message."""
        message = LLMMessage(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"

    def test_create_assistant_message(self) -> None:
        """Should create an assistant message."""
        message = LLMMessage(role="assistant", content="Hi there!")
        assert message.role == "assistant"
        assert message.content == "Hi there!"

    def test_create_system_message(self) -> None:
        """Should create a system message."""
        message = LLMMessage(role="system", content="You are helpful.")
        assert message.role == "system"


class TestLLMResponse:
    """Test cases for LLM response model."""

    def test_create_response(self) -> None:
        """Should create a response with all fields."""
        response = LLMResponse(
            content="Hello!",
            model="test-model",
            input_tokens=10,
            output_tokens=5,
            stop_reason="end_turn"
        )
        assert response.content == "Hello!"
        assert response.model == "test-model"
        assert response.input_tokens == 10
        assert response.output_tokens == 5

    def test_response_total_tokens(self) -> None:
        """Should calculate total tokens."""
        response = LLMResponse(
            content="Test",
            model="model",
            input_tokens=100,
            output_tokens=50
        )
        assert response.total_tokens == 150


class TestProviderConfig:
    """Test cases for provider configuration."""

    def test_create_provider_config(self) -> None:
        """Should create provider config."""
        config = ProviderConfig(
            name="Test Provider",
            api_key="test-key",
            model="test-model",
            endpoint="https://api.test.com"
        )
        assert config.name == "Test Provider"
        assert config.api_key == "test-key"

    def test_provider_config_defaults(self) -> None:
        """Should have sensible defaults."""
        config = ProviderConfig(
            name="Test",
            model="model"
        )
        assert config.max_tokens == 4096
        assert config.temperature == 1.0


class TestBaseLLMProvider:
    """Test cases for base LLM provider abstract class."""

    def test_cannot_instantiate_base_class(self) -> None:
        """Should not be able to instantiate abstract base class."""
        config = ProviderConfig(name="Test", model="model")
        with pytest.raises(TypeError):
            BaseLLMProvider(config)  # type: ignore

    def test_subclass_must_implement_send_message(self) -> None:
        """Subclass must implement send_message."""
        # This is implicitly tested by MockLLMProvider implementation
        pass


class TestMockLLMProvider:
    """Test cases for mock LLM provider."""

    def test_create_mock_provider(self) -> None:
        """Should create a mock provider."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)
        assert provider.config.name == "Mock"

    @pytest.mark.asyncio
    async def test_send_message(self) -> None:
        """Should return a mock response."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        messages = [LLMMessage(role="user", content="Hello")]
        response = await provider.send_message(messages)

        assert response.content is not None
        assert response.model == "mock-model"
        assert response.input_tokens > 0
        assert response.output_tokens > 0

    @pytest.mark.asyncio
    async def test_stream_message(self) -> None:
        """Should stream mock response chunks."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        messages = [LLMMessage(role="user", content="Hello")]
        chunks = []
        async for chunk in provider.stream_message(messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert all(isinstance(c, str) for c in chunks)

    def test_count_tokens(self) -> None:
        """Should estimate token count."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        count = provider.count_tokens("Hello, world!")
        assert count > 0
        assert isinstance(count, int)

    def test_get_model_info(self) -> None:
        """Should return model information."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        info = provider.get_model_info()
        assert info.name == "mock-model"
        assert info.provider == "mock"
        assert info.max_context_tokens > 0

    def test_validate_config_success(self) -> None:
        """Should validate valid config."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        assert provider.validate_config() is True

    @pytest.mark.asyncio
    async def test_send_message_with_custom_response(self) -> None:
        """Should use custom response when set."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)
        provider.set_response("Custom response!")

        messages = [LLMMessage(role="user", content="Hello")]
        response = await provider.send_message(messages)

        assert response.content == "Custom response!"

    @pytest.mark.asyncio
    async def test_send_message_tracks_history(self) -> None:
        """Should track message history."""
        config = ProviderConfig(name="Mock", model="mock-model")
        provider = MockLLMProvider(config)

        messages = [LLMMessage(role="user", content="Test message")]
        await provider.send_message(messages)

        assert len(provider.message_history) == 1
        # message_history is a list of (messages, response) tuples
        # messages is a list of LLMMessage
        assert provider.message_history[0][0][0].content == "Test message"
