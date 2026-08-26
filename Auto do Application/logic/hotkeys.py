"""
Global Hotkey Manager for Auto Do Application.
Captures system-wide hotkeys:
  - F11: Start Recording
  - F12: End Recording / Stop
  - F10: Play
  - Esc: Emergency Halt
Uses dual native Windows GetAsyncKeyState polling + pynput.
"""

import time
import threading
import ctypes

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


class HotkeyManager:
    def __init__(self, on_record=None, on_stop=None, on_play=None, on_escape=None):
        self.on_record = on_record
        self.on_stop = on_stop
        self.on_play = on_play
        self.on_escape = on_escape
        
        self.is_running = False
        self.poll_thread = None
        self.pynput_listener = None
        
        # Debounce tracking
        self.last_pressed = {}

    def start(self):
        self.is_running = True
        
        # 1. Native Windows GetAsyncKeyState Worker (Ultra reliable system-wide hook)
        self.poll_thread = threading.Thread(target=self._native_poll_worker, daemon=True)
        self.poll_thread.start()

        # 2. Pynput GlobalHotKeys
        if PYNPUT_AVAILABLE:
            try:
                hotkeys = {
                    "<f11>": self._handle_record,
                    "<f12>": self._handle_stop,
                    "<f10>": self._handle_play,
                    "<esc>": self._handle_escape,
                }
                self.pynput_listener = keyboard.GlobalHotKeys(hotkeys)
                self.pynput_listener.start()
            except Exception:
                self.pynput_listener = None
        return True

    def stop(self):
        self.is_running = False
        if self.pynput_listener:
            try:
                self.pynput_listener.stop()
            except Exception:
                pass
            self.pynput_listener = None

    def _native_poll_worker(self):
        user32 = ctypes.windll.user32
        
        VK_F11 = 0x7A  # F11
        VK_F12 = 0x7B  # F12
        VK_F10 = 0x79  # F10
        VK_ESCAPE = 0x1B # Esc

        key_map = {
            VK_F11: self._handle_record,
            VK_F12: self._handle_stop,
            VK_F10: self._handle_play,
            VK_ESCAPE: self._handle_escape
        }

        # Track key states to fire once on down
        states = {k: False for k in key_map}

        while self.is_running:
            for vk, handler in key_map.items():
                is_down = (user32.GetAsyncKeyState(vk) & 0x8000) != 0
                if is_down and not states[vk]:
                    states[vk] = True
                    # If pynput is NOT active, fire handler directly to prevent duplicate events
                    if not PYNPUT_AVAILABLE or not self.pynput_listener:
                        handler()
                elif not is_down and states[vk]:
                    states[vk] = False

            time.sleep(0.015)

    def _handle_record(self):
        now = time.time()
        if now - self.last_pressed.get("record", 0) > 0.25:
            self.last_pressed["record"] = now
            if self.on_record:
                self.on_record()

    def _handle_stop(self):
        now = time.time()
        if now - self.last_pressed.get("stop", 0) > 0.25:
            self.last_pressed["stop"] = now
            if self.on_stop:
                self.on_stop()

    def _handle_play(self):
        now = time.time()
        if now - self.last_pressed.get("play", 0) > 0.25:
            self.last_pressed["play"] = now
            if self.on_play:
                self.on_play()

    def _handle_escape(self):
        now = time.time()
        if now - self.last_pressed.get("escape", 0) > 0.25:
            self.last_pressed["escape"] = now
            if self.on_escape:
                self.on_escape()
