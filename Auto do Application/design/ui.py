"""
Modern UI Layout and Window Design for Auto Do Application.
Built with CustomTkinter for rounded buttons, smooth dark surfaces, and exact visual match to design.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import customtkinter as ctk  # type: ignore
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

try:
    from .theme import Theme
except (ImportError, ValueError):
    from design.theme import Theme


class AutoDoUI:
    def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller

        # Window configuration
        self.root.title("Auto Do")
        self.root.geometry("440x430")
        self.root.minsize(420, 410)
        self.root.resizable(False, False)

        if CTK_AVAILABLE:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            if isinstance(self.root, ctk.CTk):
                self.root.configure(fg_color="#12131a")
            else:
                self.root.configure(bg="#12131a")
        else:
            self.root.configure(bg="#12131a")

        # Set App Icon if exists
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        ico_path = os.path.join(assets_dir, "icon.ico")
        png_path = os.path.join(assets_dir, "icon.png")

        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass
        elif os.path.exists(png_path):
            try:
                img = tk.PhotoImage(file=png_path)
                self.root.iconphoto(True, img)
            except Exception:
                pass

        self._create_layout()

    def _create_layout(self):
        # Main Outer Container with padding
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            self.main_container = ctk.CTkFrame(self.root, fg_color="#12131a", corner_radius=0)
            self.main_container.pack(fill="both", expand=True, padx=22, pady=20)
        else:
            self.main_container = tk.Frame(self.root, bg="#12131a", padx=22, pady=20)
            self.main_container.pack(fill=tk.BOTH, expand=True)

        # 1. Status Label
        self.status_var = tk.StringVar(value="Status: Ready")
        if CTK_AVAILABLE:
            self.status_lbl = ctk.CTkLabel(
                self.main_container,
                textvariable=self.status_var,
                font=("Segoe UI", 13, "bold"),
                text_color="#94a3b8",
                anchor="w"
            )
            self.status_lbl.pack(fill="x", pady=(0, 14))
        else:
            self.status_lbl = tk.Label(
                self.main_container,
                textvariable=self.status_var,
                font=("Segoe UI", 11, "bold"),
                bg="#12131a",
                fg="#94a3b8",
                anchor="w"
            )
            self.status_lbl.pack(fill=tk.X, pady=(0, 14))

        # 2. Row 1: Record & Stop Buttons
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            row1_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
            row1_frame.pack(fill="x", pady=5)

            self.btn_record = ctk.CTkButton(
                row1_frame,
                text="⏺  Record",
                fg_color="#fb6f6f",
                hover_color="#f85b5b",
                text_color="#ffffff",
                corner_radius=14,
                height=46,
                font=("Segoe UI", 13, "bold"),
                command=self.app.handle_record
            )
            self.btn_record.pack(side="left", fill="both", expand=True, padx=(0, 6))

            self.btn_stop = ctk.CTkButton(
                row1_frame,
                text="⏹  Stop",
                fg_color="#5b5bd6",
                hover_color="#4e4ec7",
                text_color="#ffffff",
                corner_radius=14,
                height=46,
                font=("Segoe UI", 13, "bold"),
                command=self.app.handle_stop
            )
            self.btn_stop.pack(side="right", fill="both", expand=True, padx=(6, 0))
        else:
            row1_frame = tk.Frame(self.main_container, bg="#12131a")
            row1_frame.pack(fill=tk.X, pady=5)
            self.btn_record = tk.Button(row1_frame, text="⏺  Record", bg="#fb6f6f", fg="#ffffff", relief=tk.FLAT, font=("Segoe UI", 11, "bold"), command=self.app.handle_record)
            self.btn_record.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6), ipady=8)
            self.btn_stop = tk.Button(row1_frame, text="⏹  Stop", bg="#5b5bd6", fg="#ffffff", relief=tk.FLAT, font=("Segoe UI", 11, "bold"), command=self.app.handle_stop)
            self.btn_stop.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0), ipady=8)

        # 3. Row 2: Centered Play Button
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            row2_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
            row2_frame.pack(fill="x", pady=8)

            self.btn_play = ctk.CTkButton(
                row2_frame,
                text="▶   Play",
                fg_color="#4ade80",
                hover_color="#3ee079",
                text_color="#0b381b",
                corner_radius=14,
                height=52,
                font=("Segoe UI", 15, "bold"),
                command=self.app.handle_play
            )
            self.btn_play.pack(fill="x", padx=30)
        else:
            row2_frame = tk.Frame(self.main_container, bg="#12131a")
            row2_frame.pack(fill=tk.X, pady=8)
            self.btn_play = tk.Button(row2_frame, text="▶   Play", bg="#4ade80", fg="#0b381b", relief=tk.FLAT, font=("Segoe UI", 13, "bold"), command=self.app.handle_play)
            self.btn_play.pack(fill=tk.X, padx=30, ipady=10)

        # 4. Row: Loops & Repeat Settings Pill Container
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            loop_frame = ctk.CTkFrame(
                self.main_container,
                fg_color="#181924",
                border_width=1,
                border_color="#2b2d3d",
                corner_radius=10,
                height=42
            )
            loop_frame.pack(fill="x", pady=(4, 10), ipady=4)

            loop_lbl = ctk.CTkLabel(
                loop_frame,
                text="Loops:",
                font=("Segoe UI", 11, "bold"),
                text_color="#94a3b8"
            )
            loop_lbl.pack(side="left", padx=(14, 6))

            self.loop_count_var = tk.StringVar(value="1")
            self.loop_entry = ctk.CTkEntry(
                loop_frame,
                textvariable=self.loop_count_var,
                width=46,
                height=26,
                corner_radius=6,
                fg_color="#101118",
                border_color="#373a4d",
                text_color="#ffffff",
                font=("Segoe UI", 11, "bold"),
                justify="center"
            )
            self.loop_entry.pack(side="left", padx=(0, 10))

            self.infinite_var = tk.BooleanVar(value=False)
            self.infinite_cb = ctk.CTkCheckBox(
                loop_frame,
                text="Repeat Infinitely (∞)",
                variable=self.infinite_var,
                command=self._on_infinite_toggle,
                font=("Segoe UI", 11, "normal"),
                text_color="#cbd5e1",
                fg_color="#5b5bd6",
                hover_color="#4f46e5",
                corner_radius=5,
                border_color="#474b63"
            )
            self.infinite_cb.pack(side="right", padx=(0, 14))
        else:
            loop_frame = tk.Frame(self.main_container, bg="#181924", padx=12, pady=6)
            loop_frame.pack(fill=tk.X, pady=(4, 10))
            loop_lbl = tk.Label(loop_frame, text="Loops:", bg="#181924", fg="#94a3b8", font=("Segoe UI", 9, "bold"))
            loop_lbl.pack(side=tk.LEFT, padx=(4, 6))
            self.loop_count_var = tk.StringVar(value="1")
            self.loop_entry = tk.Entry(loop_frame, textvariable=self.loop_count_var, width=5, bg="#101118", fg="#ffffff", font=("Segoe UI", 9, "bold"), justify="center")
            self.loop_entry.pack(side=tk.LEFT, padx=(0, 10))
            self.infinite_var = tk.BooleanVar(value=False)
            self.infinite_cb = tk.Checkbutton(loop_frame, text="Repeat Infinitely (∞)", variable=self.infinite_var, command=self._on_infinite_toggle, bg="#181924", fg="#ffffff", selectcolor="#101118")
            self.infinite_cb.pack(side=tk.RIGHT, padx=(0, 8))

        # 5. Row 3: Save & Load Buttons
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            row3_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
            row3_frame.pack(fill="x", pady=5)

            self.btn_save = ctk.CTkButton(
                row3_frame,
                text="💾  Save",
                fg_color="#5b5bd6",
                hover_color="#4e4ec7",
                text_color="#ffffff",
                corner_radius=14,
                height=46,
                font=("Segoe UI", 13, "bold"),
                command=self.app.handle_save
            )
            self.btn_save.pack(side="left", fill="both", expand=True, padx=(0, 6))

            self.btn_load = ctk.CTkButton(
                row3_frame,
                text="📁  Load",
                fg_color="#5b5bd6",
                hover_color="#4e4ec7",
                text_color="#ffffff",
                corner_radius=14,
                height=46,
                font=("Segoe UI", 13, "bold"),
                command=self.app.handle_load
            )
            self.btn_load.pack(side="right", fill="both", expand=True, padx=(6, 0))
        else:
            row3_frame = tk.Frame(self.main_container, bg="#12131a")
            row3_frame.pack(fill=tk.X, pady=5)
            self.btn_save = tk.Button(row3_frame, text="💾  Save", bg="#5b5bd6", fg="#ffffff", relief=tk.FLAT, font=("Segoe UI", 11, "bold"), command=self.app.handle_save)
            self.btn_save.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6), ipady=8)
            self.btn_load = tk.Button(row3_frame, text="📁  Load", bg="#5b5bd6", fg="#ffffff", relief=tk.FLAT, font=("Segoe UI", 11, "bold"), command=self.app.handle_load)
            self.btn_load.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0), ipady=8)

        # 6. Footer: CreatedByAyziel & Circular Help Button
        if CTK_AVAILABLE and isinstance(self.root, ctk.CTk):
            footer_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
            footer_frame.pack(fill="x", side="bottom", pady=(12, 0))

            author_lbl = ctk.CTkLabel(
                footer_frame,
                text="CreatedByAyziel",
                font=("Segoe UI", 10, "italic"),
                text_color="#505569"
            )
            author_lbl.pack(side="left", anchor="s", pady=(8, 0))

            self.btn_help = ctk.CTkButton(
                footer_frame,
                text="?",
                font=("Segoe UI", 13, "bold"),
                fg_color="#5b5bd6",
                hover_color="#4e4ec7",
                text_color="#ffffff",
                width=38,
                height=38,
                corner_radius=19,
                command=self.show_help_dialog
            )
            self.btn_help.pack(side="right")
        else:
            footer_frame = tk.Frame(self.main_container, bg="#12131a")
            footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(12, 0))
            author_lbl = tk.Label(footer_frame, text="CreatedByAyziel", font=("Segoe UI", 9, "italic"), bg="#12131a", fg="#505569")
            author_lbl.pack(side=tk.LEFT, anchor="s")
            self.btn_help = tk.Button(footer_frame, text="?", font=("Segoe UI", 11, "bold"), bg="#5b5bd6", fg="#ffffff", relief=tk.FLAT, width=3, command=self.show_help_dialog)
            self.btn_help.pack(side=tk.RIGHT)

    def _on_infinite_toggle(self):
        if self.infinite_var.get():
            if hasattr(self.loop_entry, "configure"):
                self.loop_entry.configure(state="disabled")
            self.set_status("Status: Ready (Infinite Loops Enabled ∞)", "#4ade80")
        else:
            if hasattr(self.loop_entry, "configure"):
                self.loop_entry.configure(state="normal")
            self.set_status("Status: Ready", "#94a3b8")

    def get_loop_count(self):
        if self.infinite_var.get():
            return 0  # 0 represents infinite looping
        try:
            val = int(self.loop_count_var.get().strip())
            return max(1, val)
        except (ValueError, AttributeError):
            return 1

    def set_status(self, text, color=None):
        self.status_var.set(text)
        if CTK_AVAILABLE and hasattr(self.status_lbl, "configure"):
            self.status_lbl.configure(text_color=color or "#94a3b8")
        elif hasattr(self.status_lbl, "configure"):
            self.status_lbl.configure(fg=color or "#94a3b8")

    def show_help_dialog(self):
        if CTK_AVAILABLE:
            help_win = ctk.CTkToplevel(self.root)
            help_win.title("Auto Do Guide")
            help_win.geometry("380x310")
            help_win.configure(fg_color="#181924")
            help_win.resizable(False, False)
            help_win.attributes("-topmost", True)

            header = ctk.CTkLabel(
                help_win,
                text="Global Hotkeys & Guide",
                font=("Segoe UI", 13, "bold"),
                text_color="#f8fafc"
            )
            header.pack(fill="x", pady=(16, 6))

            content = (
                "• F11: Start Recording Mouse Actions\n"
                "• F12: End Recording / Stop Action\n"
                "• F10: Replay Recorded Macro Sequence\n"
                "• Esc: Emergency Halt\n\n"
                "Profiles are saved in standard JSON format and\n"
                "can be reloaded or shared anytime.\n\n"
                "Created with precision by Ayziel."
            )

            msg_lbl = ctk.CTkLabel(
                help_win,
                text=content,
                font=("Segoe UI", 11),
                text_color="#94a3b8",
                justify="left"
            )
            msg_lbl.pack(fill="both", expand=True, padx=20, pady=10)

            close_btn = ctk.CTkButton(
                help_win,
                text="Got It",
                fg_color="#5b5bd6",
                hover_color="#4e4ec7",
                text_color="#ffffff",
                corner_radius=10,
                height=36,
                font=("Segoe UI", 11, "bold"),
                command=help_win.destroy
            )
            close_btn.pack(pady=(0, 16), padx=40, fill="x")
        else:
            messagebox.showinfo("Auto Do Guide", "F11: Record\nF12: Stop\nF10: Play\nEsc: Halt")
