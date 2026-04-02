"""
GUI module for Pomodoro app.
Contains the Tkinter-based graphical interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class PomodoroGUI:
    """
    GUI for Pomodoro timer application.

    Features:
    - Timer display in mm:ss format
    - Start/Pause/Resume and Reset buttons
    - Mode selection via buttons or tabs
    - Duration input fields (optional)
    - Pomodoro counter
    - Sound toggle
    """

    def __init__(self, timer):
        """Initialize GUI with PomodoroTimer instance."""
        self.timer = timer

        # Create main window
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Center window on screen
        self._center_window()

        # Configure styles
        self._configure_styles()

        # Create UI elements
        self._create_widgets()

        # Start GUI update loop
        self._update_display()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _center_window(self) -> None:
        """Center window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _configure_styles(self) -> None:
        """Configure ttk styles for consistent appearance."""
        style = ttk.Style()
        style.theme_use("clam")

        # Colors
        colors = {
            "work": "#e74c3c",           # Red
            "short_break": "#27ae60",    # Green
            "long_break": "#3498db"      # Blue
        }

        self.mode_colors = colors

        for mode, color in colors.items():
            style.configure(f"{mode}.TFrame", background=color)
            style.configure(f"{mode}.TLabel", background=color, foreground="white")

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Mode display
        self.mode_label = tk.Label(
            main_frame,
            text="Work",
            font=("Helvetica", 24, "bold"),
            bg=self.mode_colors["work"],
            fg="white",
            padx=20,
            pady=10
        )
        self.mode_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Timer display
        self.timer_label = tk.Label(
            main_frame,
            text=self.timer.formatted_time,
            font=("Helvetica", 48, "bold"),
            fg="#333"
        )
        self.timer_label.grid(row=1, column=0, columnspan=3, pady=(0, 30))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=3, pady=(0, 30))

        # Start/Pause button
        self.action_button = ttk.Button(
            buttons_frame,
            text="Start",
            command=self._on_action_button_click
        )
        self.action_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        reset_button = ttk.Button(
            buttons_frame,
            text="Reset",
            command=self._on_reset_button_click
        )
        reset_button.pack(side=tk.LEFT, padx=5)

        # Pomodoro counter
        pomodoro_frame = ttk.Frame(main_frame)
        pomodoro_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))

        self.pomodoro_label = tk.Label(
            pomodoro_frame,
            text=f"Pomodoros: {self.timer.pomodoro_count}",
            font=("Helvetica", 14),
            fg="#666"
        )
        self.pomodoro_label.pack()

        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))

        # Mode duration inputs
        row = 0

        # Work duration
        tk.Label(settings_frame, text="Work (min):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.work_entry = ttk.Entry(settings_frame, width=10)
        self.work_entry.insert(0, str(self.timer.work_duration // 60))
        self.work_entry.grid(row=row, column=1, padx=5, pady=5)

        # Short break duration
        row += 1
        tk.Label(settings_frame, text="Short Break (min):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.short_break_entry = ttk.Entry(settings_frame, width=10)
        self.short_break_entry.insert(0, str(self.timer.short_break_duration // 60))
        self.short_break_entry.grid(row=row, column=1, padx=5, pady=5)

        # Long break duration
        row += 1
        tk.Label(settings_frame, text="Long Break (min):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.long_break_entry = ttk.Entry(settings_frame, width=10)
        self.long_break_entry.insert(0, str(self.timer.long_break_duration // 60))
        self.long_break_entry.grid(row=row, column=1, padx=5, pady=5)

        # Save settings button
        row += 1
        save_button = ttk.Button(
            settings_frame,
            text="Save Settings",
            command=self._on_save_settings
        )
        save_button.grid(row=row, column=0, columnspan=2, pady=10)

        # Sound toggle
        sound_frame = ttk.Frame(main_frame)
        sound_frame.grid(row=5, column=0, columnspan=3)

        self.sound_var = tk.BooleanVar(value=True)
        sound_check = ttk.Checkbutton(
            sound_frame,
            text="Enable Sound",
            variable=self.sound_var,
            command=self._on_sound_toggle
        )
        sound_check.pack(pady=10)

        # Mode selection buttons
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=6, column=0, columnspan=3)

        tk.Label(mode_frame, text="Switch Mode:").pack(pady=(10, 5))

        ttk.Button(
            mode_frame,
            text="Work",
            command=lambda: self._on_mode_change("work")
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            mode_frame,
            text="Short Break",
            command=lambda: self._on_mode_change("short_break")
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            mode_frame,
            text="Long Break",
            command=lambda: self._on_mode_change("long_break")
        ).pack(side=tk.LEFT, padx=5)

    def _update_display(self) -> None:
        """Update display elements based on timer state."""
        # Update timer label
        self.timer_label.config(text=self.timer.formatted_time)

        # Update mode label and color
        mode_texts = {
            "work": "Work",
            "short_break": "Short Break",
            "long_break": "Long Break"
        }
        self.mode_label.config(
            text=mode_texts[self.timer.current_mode],
            bg=self.mode_colors[self.timer.current_mode]
        )

        # Update action button text
        if self.timer.is_running:
            if self.timer.is_paused:
                self.action_button.config(text="Resume")
            else:
                self.action_button.config(text="Pause")
        else:
            self.action_button.config(text="Start")

        # Update pomodoro counter
        self.pomodoro_label.config(text=f"Pomodoros: {self.timer.pomodoro_count}")

        # Schedule next update (100ms)
        self.root.after(100, self._update_display)

    def _on_action_button_click(self) -> None:
        """Handle action button click."""
        if self.timer.is_running:
            if self.timer.is_paused:
                self.timer.resume()
            else:
                self.timer.pause()
        else:
            self.timer.start()

    def _on_reset_button_click(self) -> None:
        """Handle reset button click."""
        if messagebox.askyesno("Reset Timer", "Are you sure you want to reset the timer?"):
            self.timer.reset()

    def _on_save_settings(self) -> None:
        """Handle save settings button click."""
        try:
            work = int(self.work_entry.get())
            short_break = int(self.short_break_entry.get())
            long_break = int(self.long_break_entry.get())

            # Stop timer before changing durations
            self.timer.stop()

            self.timer.set_work_duration(work)
            self.timer.set_short_break_duration(short_break)
            self.timer.set_long_break_duration(long_break)

            # Reset timer with new durations
            self.timer.reset()

            messagebox.showinfo("Settings Saved", "Timer settings have been updated.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for durations.")

    def _on_mode_change(self, mode: str) -> None:
        """Handle mode change button click."""
        self.timer.stop()
        self.timer.switch_mode(mode)

    def _on_sound_toggle(self) -> None:
        """Handle sound toggle."""
        if self.timer.settings:
            self.timer.settings.sound_enabled = self.sound_var.get()

    def _on_closing(self) -> None:
        """Handle window closing event."""
        if self.timer.settings:
            # Update settings with current values before saving
            self.timer.settings.work_duration = self.timer.work_duration // 60
            self.timer.settings.short_break_duration = self.timer.short_break_duration // 60
            self.timer.settings.long_break_duration = self.timer.long_break_duration // 60
            self.timer.settings.sound_enabled = self.sound_var.get()
            self.timer.settings.save()
        self.root.destroy()

    def run(self) -> None:
        """Start the GUI main loop."""
        self.root.mainloop()
