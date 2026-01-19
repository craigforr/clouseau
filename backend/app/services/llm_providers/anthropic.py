"""Anthropic Claude provider implementation."""

from typing import AsyncGenerator, List, Optional

from anthropic import Anthropic

from app.services.llm_providers.base import (
    BaseLLMProvider,
    LLMMessage,
    LLMResponse,
    ModelInfo,
    ProviderConfig,
)


# Model context window sizes
MODEL_CONTEXT_SIZES = {
    "claude-3-5-sonnet-20241022": 200000,
    "claude-3-5-haiku-20241022": 200000,
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "claude-3-haiku-20240307": 200000,
}

DEFAULT_CONTEXT_SIZE = 200000


class AnthropicProvider(BaseLLMProvider):
    """LLM provider for Anthropic Claude models.

    Supports all Claude 3.x models with streaming and vision capabilities.
    """

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize Anthropic provider.

        Args:
            config: Provider configuration with API key
        """
        super().__init__(config)
        self._client = Anthropic(api_key=config.api_key)

    async def send_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send messages to Claude and get a response.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters (max_tokens, temperature, etc.)

        Returns:
            LLMResponse containing Claude's response
        """
        # Extract system message if present
        system_message: Optional[str] = None
        api_messages = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content,
                })

        # Build request parameters
        request_params = {
            "model": self.config.model,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "messages": api_messages,
        }

        if system_message:
            request_params["system"] = system_message

        if self.config.temperature is not None:
            request_params["temperature"] = self.config.temperature

        # Make the API call
        response = self._client.messages.create(**request_params)

        # Extract response content
        content = ""
        if response.content:
            content = response.content[0].text

        return LLMResponse(
            content=content,
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            stop_reason=response.stop_reason,
        )

    async def stream_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream messages from Claude.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters

        Yields:
            String chunks of the response as they arrive
        """
        # Extract system message if present
        system_message: Optional[str] = None
        api_messages = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content,
                })

        # Build request parameters
        request_params = {
            "model": self.config.model,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "messages": api_messages,
        }

        if system_message:
            request_params["system"] = system_message

        if self.config.temperature is not None:
            request_params["temperature"] = self.config.temperature

        # Stream the response
        with self._client.messages.stream(**request_params) as stream:
            for event in stream:
                if event.type == "content_block_delta":
                    yield event.delta.text

    def count_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Uses a simple estimation of ~4 characters per token.
        For more accurate counts, use the Anthropic tokenizer.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 characters per token
        # Claude models use a similar tokenization to GPT models
        return max(1, len(text) // 4)

    def get_model_info(self) -> ModelInfo:
        """Get information about the current Claude model.

        Returns:
            ModelInfo object with model details
        """
        context_size = MODEL_CONTEXT_SIZES.get(
            self.config.model, DEFAULT_CONTEXT_SIZE
        )

        return ModelInfo(
            name=self.config.model,
            provider="anthropic",
            max_context_tokens=context_size,
            supports_streaming=True,
            supports_vision=True,
            supports_function_calling=True,
        )

    def validate_config(self) -> bool:
        """Validate the provider configuration.

        Returns:
            True if configuration is valid (has API key)
        """
        return bool(self.config.api_key)
