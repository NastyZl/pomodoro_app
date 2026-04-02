"""
Pomodoro Timer module.
Contains the core logic for timer management and mode switching.
"""

import threading
import time


class PomodoroTimer:
    """
    Core timer logic for Pomodoro technique.

    Modes:
    - WORK: Working mode (default 25 minutes)
    - SHORT_BREAK: Short break after work (default 5 minutes)
    - LONG_BREAK: Long break after 4 work cycles (default 15 minutes)

    State machine:
    IDLE -> RUNNING -> [COMPLETED -> NEXT_MODE] or [PAUSED -> RUNNING]
    """

    # Mode constants
    MODE_WORK = "work"
    MODE_SHORT_BREAK = "short_break"
    MODE_LONG_BREAK = "long_break"

    def __init__(self, settings=None):
        """Initialize timer with optional settings object."""
        self.settings = settings

        # Mode durations in seconds (loaded from settings if provided)
        if self.settings:
            self.work_duration = self.settings.work_duration * 60
            self.short_break_duration = self.settings.short_break_duration * 60
            self.long_break_duration = self.settings.long_break_duration * 60
        else:
            self.work_duration = 25 * 60
            self.short_break_duration = 5 * 60
            self.long_break_duration = 15 * 60

        # State variables
        self.current_mode = self.MODE_WORK
        self.time_left = self.work_duration
        self.is_running = False
        self.is_paused = False
        self.pomodoro_count = 0
        self.work_cycles_completed = 0

        # Thread control
        self._timer_thread = None
        self._stop_event = threading.Event()

    @property
    def mode_duration(self) -> int:
        """Return duration of current mode in seconds."""
        if self.current_mode == self.MODE_WORK:
            return self.work_duration
        elif self.current_mode == self.MODE_SHORT_BREAK:
            return self.short_break_duration
        else:
            return self.long_break_duration

    @property
    def formatted_time(self) -> str:
        """Return formatted time as mm:ss."""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes:02d}:{seconds:02d}"

    def start(self) -> bool:
        """Start the timer. Returns True if started successfully."""
        if self.is_running:
            return False

        self.is_running = True
        self.is_paused = False
        self._stop_event.clear()
        self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self._timer_thread.start()
        return True

    def pause(self) -> bool:
        """Pause the timer. Returns True if paused successfully."""
        if not self.is_running or self.is_paused:
            return False

        self.is_paused = True
        return True

    def resume(self) -> bool:
        """Resume the timer from paused state. Returns True if resumed."""
        if not self.is_running or not self.is_paused:
            return False

        self.is_paused = False
        self._stop_event.clear()
        # Create new thread to continue timer
        self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self._timer_thread.start()
        return True

    def reset(self) -> None:
        """Reset timer to initial state."""
        self.stop()
        self.current_mode = self.MODE_WORK
        self.time_left = self.work_duration
        self.is_running = False
        self.is_paused = False
        self.pomodoro_count = 0
        self.work_cycles_completed = 0

    def stop(self) -> None:
        """Stop the timer."""
        self.is_running = False
        self._stop_event.set()

    def switch_mode(self, mode: str) -> None:
        """Switch to specified mode and reset timer."""
        valid_modes = [self.MODE_WORK, self.MODE_SHORT_BREAK, self.MODE_LONG_BREAK]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")

        self.stop()
        self.current_mode = mode
        if mode == self.MODE_WORK:
            self.time_left = self.work_duration
        elif mode == self.MODE_SHORT_BREAK:
            self.time_left = self.short_break_duration
        else:
            self.time_left = self.long_break_duration

    def set_work_duration(self, minutes: int) -> None:
        """Set work duration in minutes."""
        if minutes <= 0:
            raise ValueError("Duration must be positive")
        self.work_duration = minutes * 60

    def set_short_break_duration(self, minutes: int) -> None:
        """Set short break duration in minutes."""
        if minutes <= 0:
            raise ValueError("Duration must be positive")
        self.short_break_duration = minutes * 60

    def set_long_break_duration(self, minutes: int) -> None:
        """Set long break duration in minutes."""
        if minutes <= 0:
            raise ValueError("Duration must be positive")
        self.long_break_duration = minutes * 60

    def _run_timer(self) -> None:
        """Background thread function that runs the countdown."""
        while self.is_running and not self._stop_event.is_set():
            if not self.is_paused:
                if self.time_left > 0:
                    self.time_left -= 1
                    time.sleep(1)
                else:
                    # Timer completed
                    self._handle_timer_complete()
            else:
                time.sleep(0.1)

    def _handle_timer_complete(self) -> None:
        """Handle timer completion and switch to next mode."""
        self.is_running = False

        # Play completion sound
        self._play_completion_sound()

        # Determine next mode and update pomodoro count
        if self.current_mode == self.MODE_WORK:
            self.work_cycles_completed += 1
            self.pomodoro_count += 1

            # After 4 work cycles, take long break; otherwise short break
            if self.work_cycles_completed % 4 == 0:
                self.current_mode = self.MODE_LONG_BREAK
                self.time_left = self.long_break_duration
            else:
                self.current_mode = self.MODE_SHORT_BREAK
                self.time_left = self.short_break_duration
        else:
            # After any break, start new work cycle
            self.current_mode = self.MODE_WORK
            self.time_left = self.work_duration

        # Auto-start next mode if enabled
        if self.settings and self.settings.auto_start_enabled:
            self.is_running = True
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
            self._timer_thread.start()

    def _play_completion_sound(self) -> None:
        """Play completion sound if enabled."""
        if self.settings and not self.settings.sound_enabled:
            return

        # Platform-specific sound
        import sys
        if sys.platform == "darwin":
            # macOS beep using applescript
            import subprocess
            try:
                subprocess.run(["osascript", "-e", "beep"], capture_output=True)
            except Exception:
                pass
        elif sys.platform == "win32":
            # Windows beep
            import winsound
            winsound.Beep(1000, 500)
        else:
            # Linux/Unix - try aplay or paplay
            import subprocess
            import os
            sound_file = os.path.join(os.path.dirname(__file__), "notification.wav")
            if os.path.exists(sound_file):
                try:
                    subprocess.run(["aplay", sound_file], capture_output=True)
                except Exception:
                    print("\a", end="")  # Fallback bell
            else:
                print("\a", end="")  # Simple bell
