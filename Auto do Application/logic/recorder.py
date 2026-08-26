"""
Mouse & Macro Recorder for Auto Do Application.
High-precision recording of mouse movements, drags, and clicks across all monitors.
Combines Windows native User32 hooks and pynput for 100% reliability.
"""

import time
import threading
import ctypes
from ctypes import wintypes

try:
    from pynput import mouse
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MouseRecorder:
    def __init__(self, on_status_change=None):
        self.is_recording = False
        self.actions = []
        self.start_time = 0
        self.last_time = 0
        self.last_x = None
        self.last_y = None
        
        self.on_status_change = on_status_change
        self._lock = threading.Lock()
        
        self.poll_thread = None
        self.pynput_listener = None
        
        # Click state tracker for Windows GetAsyncKeyState
        self.lbutton_down = False
        self.rbutton_down = False
        self.mbutton_down = False

    def start(self):
        with self._lock:
            if self.is_recording:
                return False
            self.actions = []
            self.start_time = time.perf_counter()
            self.last_time = self.start_time
            self.last_x = None
            self.last_y = None
            self.lbutton_down = False
            self.rbutton_down = False
            self.mbutton_down = False
            self.is_recording = True

        # Start native Windows polling thread (captures continuous movements and drag paths)
        self.poll_thread = threading.Thread(target=self._poll_worker, daemon=True)
        self.poll_thread.start()

        # Start pynput event listener if available
        if PYNPUT_AVAILABLE:
            try:
                self.pynput_listener = mouse.Listener(
                    on_click=self._on_pynput_click,
                    on_scroll=self._on_pynput_scroll
                )
                self.pynput_listener.start()
            except Exception:
                self.pynput_listener = None

        if self.on_status_change:
            self.on_status_change("Recording", 0)
        return True

    def stop(self):
        with self._lock:
            if not self.is_recording:
                return self.actions
            self.is_recording = False

        if self.pynput_listener:
            try:
                self.pynput_listener.stop()
            except Exception:
                pass
            self.pynput_listener = None

        count = len(self.actions)
        if self.on_status_change:
            self.on_status_change("Stopped", count)
        return self.actions

    def _poll_worker(self):
        user32 = ctypes.windll.user32
        pt = POINT()

        VK_LBUTTON = 0x01
        VK_RBUTTON = 0x02
        VK_MBUTTON = 0x04

        while self.is_recording:
            now = time.perf_counter()
            
            # 1. Get current global cursor position
            if user32.GetCursorPos(ctypes.byref(pt)):
                x, y = int(pt.x), int(pt.y)

                # Record movement if coordinates changed or interval elapsed
                if self.last_x is None or self.last_y is None or (x != self.last_x or y != self.last_y):
                    delay = max(0.001, now - self.last_time)
                    self.last_time = now
                    self.last_x = x
                    self.last_y = y

                    with self._lock:
                        self.actions.append({
                            "type": "move",
                            "x": x,
                            "y": y,
                            "delay": round(delay, 5)
                        })

                    if self.on_status_change and len(self.actions) % 10 == 0:
                        self.on_status_change("Recording", len(self.actions))

            # 2. Check mouse button states via native Windows API
            if not PYNPUT_AVAILABLE:
                # Left Button
                l_state = (user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0
                if l_state != self.lbutton_down:
                    self.lbutton_down = l_state
                    self._record_click(pt.x, pt.y, "left", l_state)

                # Right Button
                r_state = (user32.GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0
                if r_state != self.rbutton_down:
                    self.rbutton_down = r_state
                    self._record_click(pt.x, pt.y, "right", r_state)

                # Middle Button
                m_state = (user32.GetAsyncKeyState(VK_MBUTTON) & 0x8000) != 0
                if m_state != self.mbutton_down:
                    self.mbutton_down = m_state
                    self._record_click(pt.x, pt.y, "middle", m_state)

            # Polling frequency ~120Hz (8ms)
            time.sleep(0.008)

    def _record_click(self, x, y, button_name, pressed):
        now = time.perf_counter()
        delay = max(0.001, now - self.last_time)
        self.last_time = now

        with self._lock:
            self.actions.append({
                "type": "click",
                "x": int(x),
                "y": int(y),
                "button": button_name,
                "pressed": pressed,
                "delay": round(delay, 5)
            })

        if self.on_status_change:
            self.on_status_change("Recording", len(self.actions))

    def _on_pynput_click(self, x, y, button, pressed):
        if not self.is_recording:
            return
        btn_str = str(button).replace("Button.", "")
        self._record_click(x, y, btn_str, pressed)

    def _on_pynput_scroll(self, x, y, dx, dy):
        if not self.is_recording:
            return
        now = time.perf_counter()
        delay = max(0.001, now - self.last_time)
        self.last_time = now

        with self._lock:
            self.actions.append({
                "type": "scroll",
                "x": int(x),
                "y": int(y),
                "dx": dx,
                "dy": dy,
                "delay": round(delay, 5)
            })
