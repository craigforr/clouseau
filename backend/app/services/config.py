"""Configuration file parser with environment variable substitution."""

import os
import re
from pathlib import Path
from typing import Any, List, Optional

import yaml
from pydantic import BaseModel, Field


class LLMProviderConfig(BaseModel):
    """Configuration for an LLM provider."""

    name: str
    provider_type: str
    endpoint: str
    api_key: Optional[str] = None
    default_model: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    enabled: bool = True
    # Azure-specific
    api_version: Optional[str] = None
    deployment_name: Optional[str] = None
    # AWS-specific
    region: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    # GCP-specific
    project_id: Optional[str] = None
    location: Optional[str] = None
    credentials_path: Optional[str] = None


class AppConfig(BaseModel):
    """Application configuration."""

    llm_providers: List[LLMProviderConfig] = Field(default_factory=list)
    default_provider: Optional[str] = None


class ConfigParser:
    """Parser for YAML configuration files with environment variable substitution."""

    # Pattern for ${VAR} or ${VAR:-default}
    ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")

    def substitute_env_vars(self, content: str, strict: bool = False) -> str:
        """Substitute environment variables in content.

        Supports:
        - ${VAR} - simple substitution
        - ${VAR:-default} - with default value

        Args:
            content: String content with env var placeholders
            strict: If True, raise error for missing vars without defaults

        Returns:
            Content with env vars substituted
        """

        def replace_match(match: re.Match) -> str:
            var_name = match.group(1)
            default_value = match.group(2)

            value = os.environ.get(var_name)
            if value is not None:
                return value

            if default_value is not None:
                return default_value

            if strict:
                raise ValueError(
                    f"Environment variable '{var_name}' is not set and has no default"
                )
            return ""

        return self.ENV_VAR_PATTERN.sub(replace_match, content)

    def parse(self, config_path: Path) -> AppConfig:
        """Parse configuration file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Parsed AppConfig object

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If YAML is invalid
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        content = config_path.read_text()
        content = self.substitute_env_vars(content)

        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")

        if data is None:
            data = {}

        providers = []
        for provider_data in data.get("llm_providers", []):
            providers.append(LLMProviderConfig(**provider_data))

        return AppConfig(
            llm_providers=providers,
            default_provider=data.get("default_provider"),
        )
