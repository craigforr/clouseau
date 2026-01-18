"""Tests for configuration parser - TDD approach."""

import os
import pytest
import tempfile
from pathlib import Path

from app.services.config import ConfigParser, LLMProviderConfig, AppConfig


class TestEnvVarSubstitution:
    """Test cases for environment variable substitution."""

    def test_substitute_simple_env_var(self) -> None:
        """Should substitute ${VAR} with environment variable value."""
        os.environ["TEST_API_KEY"] = "test-key-123"
        parser = ConfigParser()
        result = parser.substitute_env_vars("api_key: ${TEST_API_KEY}")
        assert result == "api_key: test-key-123"
        del os.environ["TEST_API_KEY"]

    def test_substitute_with_default_value(self) -> None:
        """Should use default value when env var not set."""
        parser = ConfigParser()
        result = parser.substitute_env_vars("value: ${MISSING_VAR:-default}")
        assert result == "value: default"

    def test_substitute_multiple_env_vars(self) -> None:
        """Should substitute multiple env vars in same string."""
        os.environ["VAR1"] = "value1"
        os.environ["VAR2"] = "value2"
        parser = ConfigParser()
        result = parser.substitute_env_vars("${VAR1} and ${VAR2}")
        assert result == "value1 and value2"
        del os.environ["VAR1"]
        del os.environ["VAR2"]

    def test_missing_env_var_without_default_raises(self) -> None:
        """Should raise error for missing env var without default."""
        parser = ConfigParser()
        with pytest.raises(ValueError, match="Environment variable"):
            parser.substitute_env_vars("${DEFINITELY_MISSING_VAR}", strict=True)

    def test_missing_env_var_without_default_returns_empty(self) -> None:
        """Should return empty string in non-strict mode."""
        parser = ConfigParser()
        result = parser.substitute_env_vars("${DEFINITELY_MISSING_VAR}", strict=False)
        assert result == ""


class TestConfigParser:
    """Test cases for configuration file parser."""

    def test_parse_valid_config_file(self, tmp_path: Path) -> None:
        """Should parse a valid config file."""
        config_content = """
llm_providers:
  - name: "Test Provider"
    provider_type: "anthropic"
    endpoint: "https://api.test.com"
    api_key: "test-key"
    default_model: "test-model"
    enabled: true
default_provider: "Test Provider"
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        parser = ConfigParser()
        config = parser.parse(config_file)

        assert config.default_provider == "Test Provider"
        assert len(config.llm_providers) == 1
        assert config.llm_providers[0].name == "Test Provider"

    def test_parse_config_with_env_vars(self, tmp_path: Path) -> None:
        """Should parse config with environment variable substitution."""
        os.environ["TEST_KEY"] = "secret-key"
        config_content = """
llm_providers:
  - name: "Test"
    provider_type: "openai"
    endpoint: "https://api.openai.com"
    api_key: ${TEST_KEY}
    default_model: "gpt-4"
    enabled: true
default_provider: "Test"
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        parser = ConfigParser()
        config = parser.parse(config_file)

        assert config.llm_providers[0].api_key == "secret-key"
        del os.environ["TEST_KEY"]

    def test_parse_missing_file_raises(self) -> None:
        """Should raise error for missing config file."""
        parser = ConfigParser()
        with pytest.raises(FileNotFoundError):
            parser.parse(Path("/nonexistent/config.yaml"))

    def test_parse_invalid_yaml_raises(self, tmp_path: Path) -> None:
        """Should raise error for invalid YAML."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("invalid: yaml: content:")

        parser = ConfigParser()
        with pytest.raises(ValueError, match="Invalid YAML"):
            parser.parse(config_file)


class TestLLMProviderConfig:
    """Test cases for LLM provider configuration model."""

    def test_create_provider_config(self) -> None:
        """Should create provider config with required fields."""
        config = LLMProviderConfig(
            name="Test",
            provider_type="anthropic",
            endpoint="https://api.test.com",
            api_key="key",
            default_model="model",
            enabled=True
        )
        assert config.name == "Test"
        assert config.provider_type == "anthropic"

    def test_provider_config_optional_fields(self) -> None:
        """Should handle optional fields with defaults."""
        config = LLMProviderConfig(
            name="Test",
            provider_type="openai",
            endpoint="https://api.test.com",
            default_model="model",
            enabled=True
        )
        assert config.api_key is None
        assert config.max_tokens is None
        assert config.temperature is None

    def test_provider_config_with_all_fields(self) -> None:
        """Should accept all optional fields."""
        config = LLMProviderConfig(
            name="Test",
            provider_type="azure_openai",
            endpoint="https://api.test.com",
            api_key="key",
            default_model="model",
            max_tokens=4096,
            temperature=0.7,
            enabled=True,
            api_version="2024-01",
            deployment_name="deploy"
        )
        assert config.max_tokens == 4096
        assert config.temperature == 0.7
        assert config.api_version == "2024-01"
