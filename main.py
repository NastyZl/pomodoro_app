#!/usr/bin/env python3
"""
Pomodoro Timer - Main Entry Point

A desktop Pomodoro timer application using Tkinter.

Usage:
    python main.py
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pomodoro_timer import PomodoroTimer
from gui import PomodoroGUI
from settings import Settings
from notification import NotificationSound

# Global sound instance for pause/sound management
sound_notifier = NotificationSound()


def main():
    """Main entry point for the Pomodoro application."""
    # Load settings
    settings = Settings()
    settings.load()

    # Create timer with settings
    timer = PomodoroTimer(settings=settings)

    # Create GUI and run
    app = PomodoroGUI(timer)
    app.run()


if __name__ == "__main__":
    main()
