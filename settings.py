"""
Settings module for Pomodoro app.
Handles loading and saving configuration to JSON file.
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages application settings stored in a JSON file."""

    DEFAULT_WORK_DURATION = 25
    DEFAULT_SHORT_BREAK = 5
    DEFAULT_LONG_BREAK = 15
    AUTO_START_ENABLED = True
    SOUND_ENABLED = True

    def __init__(self, config_file: str = "config.json"):
        """Initialize settings with default values and load from file if exists."""
        self.config_file = Path(config_file)
        self.work_duration = self.DEFAULT_WORK_DURATION
        self.short_break_duration = self.DEFAULT_SHORT_BREAK
        self.long_break_duration = self.DEFAULT_LONG_BREAK
        self.auto_start_enabled = self.AUTO_START_ENABLED
        self.sound_enabled = self.SOUND_ENABLED

    def load(self) -> None:
        """Load settings from JSON file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.work_duration = data.get("work_duration", self.DEFAULT_WORK_DURATION)
                    self.short_break_duration = data.get("short_break_duration", self.DEFAULT_SHORT_BREAK)
                    self.long_break_duration = data.get("long_break_duration", self.DEFAULT_LONG_BREAK)
                    self.auto_start_enabled = data.get("auto_start_enabled", self.AUTO_START_ENABLED)
                    self.sound_enabled = data.get("sound_enabled", self.SOUND_ENABLED)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, use defaults
                pass

    def save(self) -> None:
        """Save current settings to JSON file."""
        data = {
            "work_duration": self.work_duration,
            "short_break_duration": self.short_break_duration,
            "long_break_duration": self.long_break_duration,
            "auto_start_enabled": self.auto_start_enabled,
            "sound_enabled": self.sound_enabled
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.work_duration = self.DEFAULT_WORK_DURATION
        self.short_break_duration = self.DEFAULT_SHORT_BREAK
        self.long_break_duration = self.DEFAULT_LONG_BREAK
        self.auto_start_enabled = self.AUTO_START_ENABLED
        self.sound_enabled = self.SOUND_ENABLED
