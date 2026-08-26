"""
Auto Do - Windows Mouse & Macro Automation Application
Main Entrypoint
"""

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk  # type: ignore
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

# Ensure current folder is in Python path for modular imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from design.theme import Theme
from design.ui import AutoDoUI
from logic.recorder import MouseRecorder
from logic.player import MousePlayer
from logic.storage import MacroStorage
from logic.hotkeys import HotkeyManager


class AutoDoApp:
    def __init__(self):
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
        
        self.actions = []
        self.recorder = MouseRecorder(on_status_change=self.on_record_status)
        self.player = MousePlayer(
            on_status_change=self.on_play_status,
            on_finished=self.on_play_finished
        )
        self.hotkeys = HotkeyManager(
            on_record=self.handle_record,
            on_stop=self.handle_stop,
            on_play=self.handle_play,
            on_escape=self.handle_stop
        )

        self.ui = AutoDoUI(self.root, self)
        
        # Start global hotkeys
        self.hotkeys.start()

        # Handle clean exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def run(self):
        self.root.mainloop()

    def _set_button_color(self, btn, color):
        if not btn:
            return
        if hasattr(btn, "configure"):
            try:
                btn.configure(fg_color=color)
            except Exception:
                try:
                    btn.configure(bg=color)
                except Exception:
                    pass

    def handle_record(self):
        if self.player.is_playing:
            self.player.stop()

        if not self.recorder.is_recording:
            success = self.recorder.start()
            if success:
                self.ui.set_status("Status: Recording... (Move & Click freely)", "#fb6f6f")
                self._set_button_color(self.ui.btn_record, "#ef4444")
        else:
            self.handle_stop()

    def handle_stop(self):
        if self.recorder.is_recording:
            self.actions = self.recorder.stop()
            count = len(self.actions)
            self.ui.set_status(f"Status: Ready ({count} actions recorded)", "#4ade80")
            self._set_button_color(self.ui.btn_record, "#fb6f6f")
        elif self.player.is_playing:
            self.player.stop()
            self.ui.set_status(f"Status: Stopped playback", "#94a3b8")
            self._set_button_color(self.ui.btn_play, "#4ade80")
        else:
            self.ui.set_status("Status: Ready", "#94a3b8")

    def handle_play(self):
        if self.recorder.is_recording:
            self.handle_stop()

        if not self.actions:
            self.ui.set_status("Status: No actions to play. Record or load first.", "#fb6f6f")
            return

        if not self.player.is_playing:
            loops = self.ui.get_loop_count()
            loop_desc = "Infinite Loops ∞" if loops == 0 else (f"1 loop" if loops == 1 else f"{loops} loops")
            self.ui.set_status(f"Status: Playing ({loop_desc})...", "#4ade80")
            self._set_button_color(self.ui.btn_play, "#22c55e")
            self.player.play(self.actions, loop_count=loops)
        else:
            self.handle_stop()

    def handle_save(self):
        if not self.actions:
            messagebox.showinfo("Save Macro", "No actions recorded yet. Please record a macro first.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Macro Files", "*.json"), ("All Files", "*.*")],
            title="Save Auto Do Macro Profile"
        )
        if filepath:
            success, msg = MacroStorage.save_to_file(filepath, self.actions)
            if success:
                self.ui.set_status("Status: Macro saved successfully", "#4ade80")
            else:
                self.ui.set_status(f"Status: {msg}", "#fb6f6f")

    def handle_load(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Macro Files", "*.json"), ("All Files", "*.*")],
            title="Load Auto Do Macro Profile"
        )
        if filepath:
            actions, msg = MacroStorage.load_from_file(filepath)
            if actions is not None:
                self.actions = actions
                self.ui.set_status(f"Status: Loaded {len(actions)} actions", "#4ade80")
            else:
                self.ui.set_status(f"Status: {msg}", "#fb6f6f")

    def on_record_status(self, status, count):
        self.root.after(0, lambda: self.ui.set_status(f"Status: Recording ({count} actions)...", "#fb6f6f"))

    def on_play_status(self, status, count):
        self.root.after(0, lambda: self.ui.set_status(f"Status: {status}...", "#4ade80"))

    def on_play_finished(self):
        self.root.after(0, lambda: self.ui.set_status("Status: Ready", "#94a3b8"))
        self.root.after(0, lambda: self._set_button_color(self.ui.btn_play, "#4ade80"))

    def on_close(self):
        self.recorder.stop()
        self.player.stop()
        self.hotkeys.stop()
        self.root.destroy()


if __name__ == "__main__":
    app = AutoDoApp()
    app.run()
