"""Tests for settings parser - TDD approach."""

import os
import pytest
from pathlib import Path

from app.services.settings import SettingsParser, AppSettings, CLISettings, GUISettings


class TestSettingsParser:
    """Test cases for settings file parser."""

    def test_parse_valid_settings_file(self, tmp_path: Path) -> None:
        """Should parse a valid settings file."""
        settings_content = """
clouseau_settings:
  version: "1.0"
  cli:
    color_mode: "dark"
    show_context_by_default: true
  gui:
    theme: "light"
"""
        settings_file = tmp_path / "settings.yaml"
        settings_file.write_text(settings_content)

        parser = SettingsParser()
        settings = parser.parse(settings_file)

        assert settings.version == "1.0"
        assert settings.cli.color_mode == "dark"
        assert settings.gui.theme == "light"

    def test_parse_settings_with_env_vars(self, tmp_path: Path) -> None:
        """Should parse settings with environment variable substitution."""
        os.environ["TEST_DATA_DIR"] = "/data/test"
        settings_content = """
clouseau_settings:
  version: "1.0"
  general:
    data_directory: ${TEST_DATA_DIR}
"""
        settings_file = tmp_path / "settings.yaml"
        settings_file.write_text(settings_content)

        parser = SettingsParser()
        settings = parser.parse(settings_file)

        assert settings.general.data_directory == "/data/test"
        del os.environ["TEST_DATA_DIR"]

    def test_parse_missing_file_raises(self) -> None:
        """Should raise error for missing settings file."""
        parser = SettingsParser()
        with pytest.raises(FileNotFoundError):
            parser.parse(Path("/nonexistent/settings.yaml"))

    def test_parse_with_defaults(self, tmp_path: Path) -> None:
        """Should use default values for missing settings."""
        settings_content = """
clouseau_settings:
  version: "1.0"
"""
        settings_file = tmp_path / "settings.yaml"
        settings_file.write_text(settings_content)

        parser = SettingsParser()
        settings = parser.parse(settings_file)

        # Should have default values
        assert settings.cli is not None
        assert settings.gui is not None


class TestCLISettings:
    """Test cases for CLI settings model."""

    def test_create_cli_settings_with_defaults(self) -> None:
        """Should create CLI settings with default values."""
        settings = CLISettings()
        assert settings.color_mode == "dark"
        assert settings.fallback_mono is True
        assert settings.syntax_highlighting is True

    def test_create_cli_settings_custom(self) -> None:
        """Should accept custom CLI settings."""
        settings = CLISettings(
            color_mode="light",
            show_context_by_default=True,
            max_scroll_lines=500
        )
        assert settings.color_mode == "light"
        assert settings.show_context_by_default is True
        assert settings.max_scroll_lines == 500


class TestGUISettings:
    """Test cases for GUI settings model."""

    def test_create_gui_settings_with_defaults(self) -> None:
        """Should create GUI settings with default values."""
        settings = GUISettings()
        assert settings.theme == "auto"
        assert settings.auto_scroll is True

    def test_create_gui_settings_custom(self) -> None:
        """Should accept custom GUI settings."""
        settings = GUISettings(
            theme="dark",
            font_size="16px",
            show_line_numbers=False
        )
        assert settings.theme == "dark"
        assert settings.font_size == "16px"
        assert settings.show_line_numbers is False
