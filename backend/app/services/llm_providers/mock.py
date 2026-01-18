"""Mock LLM provider for testing."""

from typing import AsyncGenerator, List, Optional, Tuple

from app.services.llm_providers.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    ModelInfo,
    ProviderConfig,
)


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing purposes.

    This provider returns configurable responses without making
    actual API calls, useful for testing and development.
    """

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize mock provider.

        Args:
            config: Provider configuration
        """
        super().__init__(config)
        self._custom_response: Optional[str] = None
        self._message_history: List[Tuple[List[LLMMessage], LLMResponse]] = []

    def set_response(self, response: str) -> None:
        """Set a custom response to return.

        Args:
            response: The response text to return
        """
        self._custom_response = response

    @property
    def message_history(self) -> List[Tuple[List[LLMMessage], LLMResponse]]:
        """Get history of messages sent to this provider."""
        return self._message_history

    async def send_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Return a mock response.

        Args:
            messages: List of messages
            **kwargs: Additional parameters (ignored)

        Returns:
            Mock LLMResponse
        """
        # Calculate mock token counts
        input_tokens = sum(self.count_tokens(m.content) for m in messages)

        # Generate response content
        if self._custom_response:
            content = self._custom_response
        else:
            content = f"Mock response to: {messages[-1].content[:50]}"

        output_tokens = self.count_tokens(content)

        response = LLMResponse(
            content=content,
            model=self.config.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            stop_reason="end_turn",
        )

        # Track history
        self._message_history.append((messages, response))

        return response

    async def stream_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream mock response chunks.

        Args:
            messages: List of messages
            **kwargs: Additional parameters (ignored)

        Yields:
            Mock response chunks
        """
        if self._custom_response:
            content = self._custom_response
        else:
            content = f"Mock streaming response to: {messages[-1].content[:50]}"

        # Simulate streaming by yielding word by word
        words = content.split()
        for word in words:
            yield word + " "

    def count_tokens(self, text: str) -> int:
        """Estimate token count (roughly 4 chars per token).

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 characters per token
        return max(1, len(text) // 4)

    def get_model_info(self) -> ModelInfo:
        """Get mock model information.

        Returns:
            ModelInfo for the mock model
        """
        return ModelInfo(
            name=self.config.model,
            provider="mock",
            max_context_tokens=100000,
            supports_streaming=True,
            supports_vision=False,
            supports_function_calling=False,
        )

    def validate_config(self) -> bool:
        """Validate configuration (always valid for mock).

        Returns:
            Always True for mock provider
        """
        return True
