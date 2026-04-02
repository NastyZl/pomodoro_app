# Pomodoro Timer

Desktop Pomodoro timer application built with Python and Tkinter.

## Features

- **Work mode** (default 25 minutes)
- **Short break** (default 5 minutes)
- **Long break** (default 15 minutes, after 4 work cycles)
- Auto-switching between modes
- Start/Pause/Resume and Reset controls
- Customizable duration settings
- Sound notifications
- Pomodoro counter
- Settings persistence (saved to config.json)

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

No installation needed! The app uses Python's built-in Tkinter library.

## Usage

1. Navigate to the project directory:
```bash
cd pomodoro-app
```

2. Run the application:
```bash
python main.py
```

Or simply:
```bash
python3 main.py
```

## Project Structure

```
pomodoro-app/
├── main.py          # Entry point
├── pomodoro_timer.py  # Core timer logic
├── gui.py           # Tkinter interface
├── settings.py      # Settings management
├── config.json      # Auto-saved configuration
└── README.md        # This file
```

## Controls

- **Start** - Begin the current mode
- **Pause** / **Resume** - Temporarily stop or continue the timer
- **Reset** - Reset to initial state
- **Mode buttons** - Switch between Work, Short Break, and Long Break

## Settings

You can customize duration settings in the app window. Changes are saved to `config.json` automatically when you close the application.
