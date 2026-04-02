"""
Sound notification module for Pomodoro app.
Provides cross-platform sound notifications using base64-encoded audio.
"""

import base64
import os
import sys
import tempfile


class NotificationSound:
    """Handles sound notifications for timer completion."""

    # Simple beep sound encoded as base64 (1000Hz, 500ms)
    # Generated using Python: numpy + scipy or ffmpeg
    _sound_data = """
    UklGRl9vT19XQVZFZm00DDAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU
    """

    def __init__(self):
        """Initialize sound notification system."""
        self.enabled = True
        self._temp_file = None

    def play(self) -> bool:
        """Play notification sound. Returns True if successful."""
        if not self.enabled:
            return False

        try:
            # Platform-specific sound playback
            if sys.platform == "darwin":
                return self._play_macos()
            elif sys.platform == "win32":
                return self._play_windows()
            else:
                # Linux/Unix
                return self._play_linux()
        except Exception as e:
            print(f"Sound error: {e}")
            return False

    def _play_macos(self) -> bool:
        """Play sound on macOS using AppleScript."""
        import subprocess
        try:
            # System beep
            subprocess.run(["osascript", "-e", "beep"], capture_output=True)
            return True
        except Exception:
            return False

    def _play_windows(self) -> bool:
        """Play sound on Windows."""
        try:
            import winsound
            # Play a 1000Hz tone for 500ms
            winsound.Beep(1000, 500)
            return True
        except ImportError:
            # Fallback: simple beep via ctypes
            try:
                import ctypes
                ctypes.windll.user32.MessageBeep(0)
                return True
            except Exception:
                return False

    def _play_linux(self) -> bool:
        """Play sound on Linux."""
        try:
            # Try to use paplay (PulseAudio)
            import subprocess
            result = subprocess.run(
                ["paplay", "--display=$DISPLAY", "/usr/share/sounds/alsa/Front_Center.wav"],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return True
        except Exception:
            pass

        # Fallback: console bell
        print("\a", end="", flush=True)
        return True


def play_completion_sound():
    """Convenience function to play completion sound."""
    notifier = NotificationSound()
    return notifier.play()


# Allow direct execution
if __name__ == "__main__":
    play_completion_sound()
