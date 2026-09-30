# DENM Auto-Do — Windows Mouse & Macro Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-indigo.svg)](https://microsoft.com/windows)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)

Effortless, sub-millisecond mouse macro automation for Windows. Capture trajectories, clicks, and delays, then replay them with pixel-perfect accuracy.

---

## 🚀 Quick Start

### 1. Direct Launch
Double-click `Launch_AutoDo.bat` in the root folder to start the application immediately.

### 2. Manual Python Launch
```bash
cd "Auto do Application"
pip install -r requirements.txt
python main.py
```

---

## ⌨️ Global Hotkeys

| Hotkey | Action |
|:---|:---|
| **`F11`** | Start Recording Mouse Coordinates & Clicks |
| **`F12`** | Stop Recording or End Playback |
| **`F10`** | Play Recorded Sequence |
| **`Esc`** | Emergency Halt |

---

## 🌐 GitHub Pages Live Hosting
The repository is pre-configured for GitHub Pages:
1. Go to repository **Settings** → **Pages**.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Choose branch `main` and folder `/ (root)`.
4. Your website will be live with full interactive simulator and direct download links to `AutoDo_Windows_v2.4.0.zip`.

---

## 📁 Repository Structure

```
├── index.html                  # GitHub Pages landing site & hero simulator
├── design/                     # Website design & CSS tokens
│   └── style.css
├── logic/                      # Website simulator logic & animations
│   ├── animations.js
│   ├── main.js
│   └── simulator.js
├── AutoDo_Windows_v2.4.0.zip   # Downloadable application package for web visitors
├── Launch_AutoDo.bat           # One-click Windows desktop launcher
└── Auto do Application/        # Python desktop automation application
    ├── main.py
    ├── Launch_AutoDo.bat
    ├── requirements.txt
    ├── README.md
    ├── build_exe.py
    ├── design/
    │   ├── theme.py
    │   ├── ui.py
    │   └── assets/
    └── logic/
        ├── hotkeys.py
        ├── player.py
        ├── recorder.py
        └── storage.py
```

---
