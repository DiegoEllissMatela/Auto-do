# DENM Auto-Do — Windows Mouse & Macro Automation

A lightweight, high-precision mouse automation and macro recorder tool for Windows built with Python and Tkinter.

![Auto Do](design/assets/icon.png)

---

## 🚀 Features

- **Sub-Millisecond Accuracy**: Captures exact mouse movements, delays, and click events.
- **Global Hotkeys**: Control automation even when other apps or full-screen games are in focus.
- **JSON Macro Profiles**: Save and load custom macro routines to share with teammates.
- **Modern Dark UI**: Exact replica of the dark-mode aesthetic with custom titlebar and action buttons.
- **Standalone Portable Executable**: Zero-dependency executable packaging with PyInstaller.

---

## 📋 Requirements

- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Python**: Python 3.8+

---

## ⚙️ Installation

1. Open PowerShell or Command Prompt in this directory (`Auto do Application`):

```bash
cd "Auto do Application"
```

2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Option A: One-Click Launcher (Recommended for Windows)
Simply double-click the **`Launch_AutoDo.bat`** file inside this directory or from the website:
- Automatically validates Python.
- Launches the Auto Do application instantly in background windowed mode.

### Option B: From Command Line
Run the entry script:
```bash
python main.py
```

---

## ⌨️ Global Hotkeys

| Key | Action | Description |
| :--- | :--- | :--- |
| **`F11`** | **Record** | Starts recording mouse movements, drag paths, and clicks in real-time. |
| **`F12`** | **Stop / End** | Concludes the active recording or halts active playback. |
| **`F10`** | **Play** | Replays the recorded macro sequence with exact sub-millisecond timing. |
| **`Esc`** | **Emergency Halt** | Instantly stops any active playback or recording. |

---

## 📦 Building a Standalone `.exe` (Optional)

You can package the application into a standalone portable `.exe` with the bundled `$ ` brand icon:

```bash
python build_exe.py
```

The output executable will be created in the `dist/` folder:
```text
dist/AutoDo.exe
```

---

## 📁 Project Architecture

The codebase separates visual design and underlying engine logic:

```text
Auto do Application/
├── design/                   # Visuals & UI Presentation
│   ├── theme.py              # Dark theme tokens, font definitions, and colors
│   ├── ui.py                 # Tkinter window layout and widget event bindings
│   └── assets/               # Brand logo and icon assets (.png, .ico)
├── logic/                    # Core Automation Engine
│   ├── recorder.py           # Mouse trajectory and click listener
│   ├── player.py             # Coordinate playback engine
│   ├── storage.py            # JSON macro save & load manager
│   └── hotkeys.py            # Global system-wide hotkey hooks
├── main.py                   # Application entrypoint
├── build_exe.py              # PyInstaller executable packager
├── requirements.txt          # Python dependencies
└── README.md                 # User guide & documentation
```

---

## 👤 Author & Credits

- Created by **Ayziel**
- Version: `v2.4.0`
