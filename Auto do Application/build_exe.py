"""
PyInstaller Build Script for Auto Do Windows Application
Creates a standalone, portable .exe with custom icon and no terminal window.
"""

import os
import sys
import subprocess

def build():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, "design", "assets", "icon.ico")
    main_py = os.path.join(current_dir, "main.py")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--icon={icon_path}",
        "--name=AutoDo",
        f"--add-data={os.path.join(current_dir, 'design', 'assets')};design/assets",
        main_py
    ]

    print("Building standalone executable...")
    print("Running command:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=current_dir)
    if result.returncode == 0:
        print("\nSUCCESS! Executable built at: dist/AutoDo.exe")
    else:
        print("\nBuild failed with return code:", result.returncode)

if __name__ == "__main__":
    build()
