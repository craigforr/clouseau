"""Settings file parser."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

from app.services.config import ConfigParser


class HotkeySettings(BaseModel):
    """Hotkey configuration."""

    toggle_context: str = "ctrl+k"
    toggle_api_log: str = "ctrl+l"
    toggle_stats: str = "ctrl+s"
    toggle_help: str = "ctrl+h"
    next_exchange: str = "down"
    prev_exchange: str = "up"
    quit: str = "ctrl+c"


class CLISettings(BaseModel):
    """CLI interface settings."""

    color_mode: str = "dark"
    fallback_mono: bool = True
    show_context_by_default: bool = False
    show_stats_by_default: bool = True
    default_tiles_visible: List[str] = Field(default_factory=lambda: ["chat", "stats"])
    hotkeys: HotkeySettings = Field(default_factory=HotkeySettings)
    output_format: str = "pretty"
    max_scroll_lines: int = 1000
    syntax_highlighting: bool = True


class TokenUsageColors(BaseModel):
    """Token usage color thresholds."""

    low: int = 70
    medium: int = 90


class GUISettings(BaseModel):
    """GUI (web interface) settings."""

    theme: str = "auto"
    default_theme_fallback: str = "dark"
    show_line_numbers: bool = True
    syntax_highlighting: bool = True
    auto_save_session_name: bool = True
    default_tab: str = "chat"
    token_bar_always_visible: bool = True
    token_usage_colors: TokenUsageColors = Field(default_factory=TokenUsageColors)
    auto_scroll: bool = True
    code_font: str = "monospace"
    font_size: str = "14px"


class SearchSettings(BaseModel):
    """Search settings."""

    fuzzy_threshold: float = 0.7
    max_results: int = 100
    highlight_matches: bool = True
    history_size: int = 50
    case_sensitive: bool = False
    allow_regex: bool = True


class GeneralSettings(BaseModel):
    """General application settings."""

    data_directory: Optional[str] = None
    auto_export_on_close: bool = False
    default_export_format: str = "yaml"
    auto_save_interval: int = 30
    max_history_size: int = 1000
    log_level: str = "INFO"
    log_file: Optional[str] = None
    telemetry_enabled: bool = False


class ModelSettings(BaseModel):
    """Model-specific settings."""

    default_system_prompt: str = "You are a helpful AI assistant."
    default_max_tokens: int = 4096
    default_temperature: float = 1.0
    retry_on_failure: bool = True
    max_retries: int = 3
    request_timeout: int = 60


class PerformanceSettings(BaseModel):
    """Performance settings."""

    cache_responses: bool = True
    cache_ttl: int = 3600
    max_cache_size: int = 100
    compress_data: bool = True


class PrivacySettings(BaseModel):
    """Privacy settings."""

    redact_api_keys: bool = True
    anonymize_telemetry: bool = True
    store_full_history: bool = True


class AppSettings(BaseModel):
    """Application settings."""

    version: str = "1.0"
    cli: CLISettings = Field(default_factory=CLISettings)
    gui: GUISettings = Field(default_factory=GUISettings)
    search: SearchSettings = Field(default_factory=SearchSettings)
    general: GeneralSettings = Field(default_factory=GeneralSettings)
    models: ModelSettings = Field(default_factory=ModelSettings)
    performance: PerformanceSettings = Field(default_factory=PerformanceSettings)
    privacy: PrivacySettings = Field(default_factory=PrivacySettings)


class SettingsParser:
    """Parser for YAML settings files."""

    def __init__(self) -> None:
        self._config_parser = ConfigParser()

    def parse(self, settings_path: Path) -> AppSettings:
        """Parse settings file.

        Args:
            settings_path: Path to the settings file

        Returns:
            Parsed AppSettings object

        Raises:
            FileNotFoundError: If settings file doesn't exist
            ValueError: If YAML is invalid
        """
        if not settings_path.exists():
            raise FileNotFoundError(f"Settings file not found: {settings_path}")

        content = settings_path.read_text()
        content = self._config_parser.substitute_env_vars(content)

        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in settings file: {e}")

        if data is None:
            data = {}

        settings_data = data.get("clouseau_settings", {})
        return AppSettings(**settings_data)
