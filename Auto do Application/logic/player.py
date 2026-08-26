"""
Mouse & Macro Player for Auto Do Application.
Replays recorded cursor movements, clicks, and scrolls with sub-millisecond precision.
Supports native Windows User32 and pynput.
"""

import time
import threading
import ctypes

try:
    from pynput import mouse
    from pynput.mouse import Button
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


class MousePlayer:
    def __init__(self, on_status_change=None, on_finished=None):
        self.is_playing = False
        self.should_stop = False
        self.play_thread = None
        self.on_status_change = on_status_change
        self.on_finished = on_finished
        self.controller = mouse.Controller() if PYNPUT_AVAILABLE else None

    def play(self, actions, loop_count=1, speed_multiplier=1.0):
        if not actions or self.is_playing:
            return False
        
        self.is_playing = True
        self.should_stop = False
        self.play_thread = threading.Thread(
            target=self._run_playback,
            args=(actions, loop_count, speed_multiplier),
            daemon=True
        )
        self.play_thread.start()
        return True

    def stop(self):
        if not self.is_playing:
            return False
        self.should_stop = True
        self.is_playing = False
        if self.on_status_change:
            self.on_status_change("Ready", 0)
        return True

    def _run_playback(self, actions, loop_count, speed_multiplier):
        current_loop = 0
        speed = max(0.1, speed_multiplier)
        user32 = ctypes.windll.user32

        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004
        MOUSEEVENTF_RIGHTDOWN = 0x0008
        MOUSEEVENTF_RIGHTUP = 0x0010
        MOUSEEVENTF_MIDDLEDOWN = 0x0020
        MOUSEEVENTF_MIDDLEUP = 0x0040

        try:
            while not self.should_stop:
                current_loop += 1
                if self.on_status_change:
                    if loop_count == 0:
                        self.on_status_change(f"Playing (Loop {current_loop} - Infinite ∞)", len(actions))
                    else:
                        self.on_status_change(f"Playing (Loop {current_loop}/{loop_count})", len(actions))

                for action in actions:
                    if self.should_stop:
                        break

                    delay = action.get("delay", 0) / speed
                    if delay > 0:
                        time.sleep(delay)

                    act_type = action.get("type")
                    x = int(action.get("x", 0))
                    y = int(action.get("y", 0))

                    if act_type == "move":
                        if self.controller:
                            self.controller.position = (x, y)
                        else:
                            user32.SetCursorPos(x, y)

                    elif act_type == "click":
                        btn_name = str(action.get("button", "left")).lower()
                        pressed = action.get("pressed", True)

                        if self.controller:
                            self.controller.position = (x, y)
                            btn = Button.right if "right" in btn_name else (Button.middle if "middle" in btn_name else Button.left)
                            if pressed:
                                self.controller.press(btn)
                            else:
                                self.controller.release(btn)
                        else:
                            user32.SetCursorPos(x, y)
                            if "right" in btn_name:
                                dwFlags = MOUSEEVENTF_RIGHTDOWN if pressed else MOUSEEVENTF_RIGHTUP
                            elif "middle" in btn_name:
                                dwFlags = MOUSEEVENTF_MIDDLEDOWN if pressed else MOUSEEVENTF_MIDDLEUP
                            else:
                                dwFlags = MOUSEEVENTF_LEFTDOWN if pressed else MOUSEEVENTF_LEFTUP
                            user32.mouse_event(dwFlags, 0, 0, 0, 0)

                    elif act_type == "scroll":
                        dx = action.get("dx", 0)
                        dy = action.get("dy", 0)
                        if self.controller:
                            self.controller.position = (x, y)
                            self.controller.scroll(dx, dy)
                        else:
                            user32.SetCursorPos(x, y)
                            user32.mouse_event(0x0800, 0, 0, int(dy * 120), 0)

                if loop_count != 0 and current_loop >= loop_count:
                    break

        finally:
            self.is_playing = False
            self.should_stop = False
            if self.on_status_change:
                self.on_status_change("Ready", len(actions))
            if self.on_finished:
                self.on_finished()
