"""Abstract base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional

from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    """A message in an LLM conversation."""

    role: str  # "user", "assistant", or "system"
    content: str


class LLMResponse(BaseModel):
    """Response from an LLM provider."""

    content: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: Optional[str] = None

    @property
    def total_tokens(self) -> int:
        """Total tokens used in this response."""
        return self.input_tokens + self.output_tokens


class ModelInfo(BaseModel):
    """Information about an LLM model."""

    name: str
    provider: str
    max_context_tokens: int
    supports_streaming: bool = True
    supports_vision: bool = False
    supports_function_calling: bool = False


class ProviderConfig(BaseModel):
    """Configuration for an LLM provider."""

    name: str
    model: str
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 1.0
    timeout: int = 60


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers.

    All LLM provider implementations must inherit from this class
    and implement the required abstract methods.
    """

    def __init__(self, config: ProviderConfig) -> None:
        """Initialize the provider with configuration.

        Args:
            config: Provider configuration
        """
        self.config = config

    @abstractmethod
    async def send_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> LLMResponse:
        """Send messages to the LLM and get a response.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Returns:
            LLMResponse containing the model's response
        """
        pass

    @abstractmethod
    async def stream_message(
        self,
        messages: List[LLMMessage],
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream messages from the LLM.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional provider-specific parameters

        Yields:
            String chunks of the response as they arrive
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        pass

    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Get information about the current model.

        Returns:
            ModelInfo object with model details
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider configuration.

        Returns:
            True if configuration is valid
        """
        pass
