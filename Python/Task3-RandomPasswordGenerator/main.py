
import tkinter as tk
from tkinter import messagebox
import secrets
import string
import math
import pyperclip


# ==========================================================
# THEME: macOS LIGHT + GLASSY SKY BLUE
# ==========================================================

BG = "#F4F5F8"
CARD = "#FFFFFF"
TEXT = "#20232B"
MUTED = "#737B8C"
BORDER = "#DDE3EC"

ACCENT = "#38BDF8"
ACCENT_HOVER = "#0EA5E9"
ACCENT_LIGHT = "#E0F5FF"
ACCENT_DARK = "#087EAE"

SUCCESS = "#26966B"
WARNING = "#D69A24"
DANGER = "#E45B69"

AMBIGUOUS = "0O1lI"

CHARACTER_SETS = {
    "Uppercase (A-Z)": string.ascii_uppercase,
    "Lowercase (a-z)": string.ascii_lowercase,
    "Numbers (0-9)": string.digits,
    "Symbols (!@#$...)": "!@#$%^&*()-_=+[]{};:,.?/"
}


# ==========================================================
# SECURE PASSWORD GENERATION
# ==========================================================

def generate_password(length, selected_types, exclude_ambiguous):
    if length < 8:
        raise ValueError("Password length must be at least 8.")

    if len(selected_types) < 2:
        raise ValueError("Select at least two character types.")

    pools = []

    for name in selected_types:
        chars = CHARACTER_SETS[name]

        if exclude_ambiguous:
            chars = "".join(
                char for char in chars
                if char not in AMBIGUOUS
            )

        if not chars:
            raise ValueError(
                f"No available characters for {name}."
            )

        pools.append(chars)

    if length < len(pools):
        raise ValueError("Password length is too short.")

    # Guarantee at least one character from every selected type.
    result = [secrets.choice(pool) for pool in pools]

    all_chars = "".join(pools)

    # Fill the remaining password length securely.
    for _ in range(length - len(result)):
        result.append(secrets.choice(all_chars))

    # Securely shuffle the password characters.
    secrets.SystemRandom().shuffle(result)

    return "".join(result)


def calculate_strength(length, type_count):
    if length >= 16 and type_count >= 3:
        return "Strong", SUCCESS

    if length >= 12 and type_count >= 2:
        return "Medium", WARNING

    return "Weak", DANGER


# ==========================================================
# APPLICATION
# ==========================================================

class PasswordGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Password Studio")
        self.root.geometry("620x900")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.current_password = ""
        self.history = []

        self.length_var = tk.IntVar(value=16)
        self.exclude_var = tk.BooleanVar(value=False)
        self.password_visible = tk.BooleanVar(value=True)

        self.type_vars = {
            name: tk.BooleanVar(value=True)
            for name in CHARACTER_SETS
        }

        self.build_ui()

        self.root.bind(
            "<Command-g>",
            lambda event: self.generate()
        )
        self.root.bind(
            "<Command-c>",
            lambda event: self.copy_password()
        )

    # ------------------------------------------------------
    # REUSABLE UI HELPERS
    # ------------------------------------------------------

    def label(
        self, parent, text, bg=CARD, fg=TEXT,
        size=11, bold=False, **kwargs
    ):
        return tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=(
                "Helvetica Neue",
                size,
                "bold" if bold else "normal"
            ),
            **kwargs
        )

    def card(self, parent, padding=16):
        return tk.Frame(
            parent,
            bg=CARD,
            padx=padding,
            pady=padding,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def glass_button(
        self, parent, text, command, compact=False
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=ACCENT_LIGHT,
            fg=ACCENT_DARK,
            activebackground=ACCENT_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground="#B6E8FC",
            cursor="hand2",
            font=(
                "Helvetica Neue",
                10 if compact else 12,
                "bold"
            ),
            padx=12 if compact else 18,
            pady=7 if compact else 10
        )

    # ------------------------------------------------------
    # BUILD UI
    # ------------------------------------------------------

    def build_ui(self):

        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 12))

        self.label(
            header,
            "Password Studio",
            BG, TEXT, 25, True
        ).pack(anchor="w")

        self.label(
            header,
            "Your passwords. Your control.",
            BG, MUTED, 11
        ).pack(anchor="w", pady=(3, 0))

        # Two top cards
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=20, pady=3)

        top.grid_columnconfigure(
            0, weight=1, uniform="top"
        )
        top.grid_columnconfigure(
            1, weight=1, uniform="top"
        )

        # CARD 1: SPEEDOMETER
        gauge_card = self.card(top, padding=10)
        gauge_card.grid(
            row=0, column=0,
            sticky="nsew", padx=4
        )

        self.label(
            gauge_card,
            "STRENGTH",
            CARD, MUTED, 10, True
        ).pack(anchor="w", padx=3)

        self.gauge = tk.Canvas(
            gauge_card,
            width=265,
            height=175,
            bg=CARD,
            highlightthickness=0
        )
        self.gauge.pack(fill="x", pady=(2, 0))

        self.strength_label = self.label(
            gauge_card,
            "NOT TESTED",
            CARD, MUTED, 12, True
        )
        self.strength_label.pack(pady=(0, 3))

        self.strength_detail = self.label(
            gauge_card,
            "Generate a password",
            CARD, MUTED, 9
        )
        self.strength_detail.pack()

        # CARD 2: PASSWORD DISPLAY
        password_card = self.card(top, padding=12)
        password_card.grid(
            row=0, column=1,
            sticky="nsew", padx=4
        )

        self.label(
            password_card,
            "YOUR PASSWORD",
            CARD, MUTED, 10, True
        ).pack(anchor="w")

        self.password_display = tk.Frame(
            password_card,
            bg="#F1F8FC",
            highlightbackground="#D4ECF8",
            highlightthickness=1,
            height=105
        )
        self.password_display.pack(
            fill="x", pady=(12, 8)
        )
        self.password_display.pack_propagate(False)

        self.password_text = tk.Text(
            self.password_display,
            height=3,
            wrap="char",
            bg="#F1F8FC",
            fg=TEXT,
            insertbackground=ACCENT_DARK,
            font=("Menlo", 11),
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
            highlightthickness=0
        )
        self.password_text.pack(
            fill="both", expand=True
        )
        self.password_text.insert(
            "1.0",
            "Your password\nwill appear here"
        )
        self.password_text.configure(state="disabled")

        self.glass_button(
            password_card,
            "Copy Password",
            self.copy_password,
            compact=True
        ).pack(pady=(3, 8))

        self.show_checkbox = tk.Checkbutton(
            password_card,
            text="Show password",
            variable=self.password_visible,
            command=self.toggle_password,
            bg=CARD,
            fg=MUTED,
            activebackground=CARD,
            activeforeground=ACCENT_DARK,
            selectcolor=ACCENT_LIGHT,
            font=("Helvetica Neue", 9),
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.show_checkbox.pack(anchor="w")

        # COMPACT GENERATE BUTTON
        self.glass_button(
            self.root,
            "✦  Generate Secure Password",
            self.generate
        ).pack(pady=(12, 14))

        # SETTINGS CARD
        settings = self.card(self.root, padding=15)
        settings.pack(
            fill="x", padx=24, pady=4
        )

        self.label(
            settings,
            "CUSTOMIZE YOUR PASSWORD",
            CARD, TEXT, 12, True
        ).pack(anchor="w")

        # Password length label
        length_row = tk.Frame(settings, bg=CARD)
        length_row.pack(fill="x", pady=(12, 0))

        self.label(
            length_row,
            "Password length",
            CARD, TEXT, 11, True
        ).pack(side="left")

        self.length_value = self.label(
            length_row,
            "16 characters",
            CARD, ACCENT_DARK, 11, True
        )
        self.length_value.pack(side="right")

        # MACOS VOLUME-STYLE SLIDER
        self.volume_canvas = tk.Canvas(
            settings,
            height=42,
            bg=CARD,
            highlightthickness=0,
            cursor="hand2"
        )
        self.volume_canvas.pack(
            fill="x", pady=(2, 10)
        )

        self.volume_canvas.bind(
            "<Configure>",
            self.draw_volume_slider
        )
        self.volume_canvas.bind(
            "<Button-1>",
            self.volume_slider_click
        )
        self.volume_canvas.bind(
            "<B1-Motion>",
            self.volume_slider_drag
        )

        # Character type heading
        self.label(
            settings,
            "CHARACTER TYPES",
            CARD, MUTED, 10, True
        ).pack(anchor="w", pady=(0, 5))

        # Character type checkboxes
        types_grid = tk.Frame(settings, bg=CARD)
        types_grid.pack(fill="x")

        for index, (name, variable) in enumerate(
            self.type_vars.items()
        ):
            checkbox = tk.Checkbutton(
                types_grid,
                text=name,
                variable=variable,
                bg=CARD,
                fg=TEXT,
                activebackground=CARD,
                activeforeground=ACCENT_DARK,
                selectcolor=ACCENT_LIGHT,
                font=("Helvetica Neue", 10),
                bd=0,
                highlightthickness=0,
                cursor="hand2"
            )
            checkbox.grid(
                row=index // 2,
                column=index % 2,
                sticky="w",
                padx=(0, 8),
                pady=3
            )

        # Exclude ambiguous characters
        self.exclude_checkbox = tk.Checkbutton(
            settings,
            text="Exclude ambiguous characters (0, O, 1, l, I)",
            variable=self.exclude_var,
            bg=CARD,
            fg=TEXT,
            activebackground=CARD,
            activeforeground=ACCENT_DARK,
            selectcolor=ACCENT_LIGHT,
            font=("Helvetica Neue", 10),
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.exclude_checkbox.pack(
            anchor="w", pady=(8, 0)
        )

        # HISTORY CARD
        history_card = self.card(self.root, padding=12)
        history_card.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(8, 14)
        )

        history_header = tk.Frame(
            history_card, bg=CARD
        )
        history_header.pack(fill="x")

        self.label(
            history_header,
            "RECENT PASSWORDS",
            CARD, TEXT, 11, True
        ).pack(side="left")

        self.label(
            history_header,
            "Last 5",
            CARD, MUTED, 9
        ).pack(side="right")

        self.history_list = tk.Listbox(
            history_card,
            height=4,
            bg="#F8FAFC",
            fg=TEXT,
            selectbackground=ACCENT_LIGHT,
            selectforeground=TEXT,
            font=("Menlo", 10),
            relief="flat",
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.history_list.pack(
            fill="both",
            expand=True,
            pady=(8, 5)
        )
        self.history_list.bind(
            "<Double-Button-1>",
            self.copy_history_password
        )

        self.label(
            history_card,
            "Double-click a history item to copy it. History clears on exit.",
            CARD, MUTED, 9
        ).pack(anchor="w")

        # Initial slider and gauge
        self.root.after(100, self.draw_volume_slider)
        self.draw_speedometer("None")

    # ------------------------------------------------------
    # MACOS VOLUME-STYLE PASSWORD LENGTH SLIDER
    # ------------------------------------------------------

    def draw_volume_slider(self, event=None):
        canvas = self.volume_canvas
        canvas.delete("all")

        width = canvas.winfo_width()

        if width < 50:
            return

        left = 14
        right = width - 14
        center_y = 21

        minimum = 8
        maximum = 64
        value = self.length_var.get()

        ratio = (value - minimum) / (maximum - minimum)
        knob_x = left + ratio * (right - left)

        # Background track
        canvas.create_line(
            left, center_y,
            right, center_y,
            fill="#DCE4EC",
            width=8,
            capstyle=tk.ROUND
        )

        # Sky-blue progress track
        if knob_x > left:
            canvas.create_line(
                left, center_y,
                knob_x, center_y,
                fill=ACCENT,
                width=8,
                capstyle=tk.ROUND
            )

        # White circular slider knob
        canvas.create_oval(
            knob_x - 10, center_y - 10,
            knob_x + 10, center_y + 10,
            fill="#FFFFFF",
            outline=ACCENT,
            width=3
        )

    def volume_slider_click(self, event):
        self.set_volume_value(event.x)

    def volume_slider_drag(self, event):
        self.set_volume_value(event.x)

    def set_volume_value(self, x):
        canvas = self.volume_canvas

        left = 14
        right = canvas.winfo_width() - 14

        if right <= left:
            return

        x = max(left, min(x, right))
        ratio = (x - left) / (right - left)

        value = round(8 + ratio * (64 - 8))

        self.length_var.set(value)
        self.length_value.config(
            text=f"{value} characters"
        )

        self.draw_volume_slider()

    # ------------------------------------------------------
    # PASSWORD SHOW / HIDE
    # ------------------------------------------------------

    def update_password_display(self):
        self.password_text.configure(state="normal")
        self.password_text.delete("1.0", tk.END)

        if not self.current_password:
            display = "Your password\nwill appear here"
        elif self.password_visible.get():
            display = self.current_password
        else:
            display = "•" * len(self.current_password)

        self.password_text.insert("1.0", display)
        self.password_text.configure(state="disabled")

    def toggle_password(self):
        self.update_password_display()

    # ------------------------------------------------------
    # SPEEDOMETER
    # ------------------------------------------------------

    def draw_speedometer(self, strength):
        canvas = self.gauge
        canvas.delete("all")
        canvas.update_idletasks()

        width = max(canvas.winfo_width(), 265)
        cx = width / 2
        cy = 137
        radius = min(100, width * 0.37)

        # Outer dial
        canvas.create_oval(
            cx - radius - 8, cy - radius - 8,
            cx + radius + 8, cy + radius + 8,
            fill="#F1F8FC",
            outline="#D8EAF4",
            width=2
        )

        # Gauge color zones
        zones = [
            (120, 60, "#F87171"),
            (60, 60, "#FBBF24"),
            (0, 60, "#34D399")
        ]

        for start, extent, color in zones:
            canvas.create_arc(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                start=start,
                extent=extent,
                style="arc",
                outline=color,
                width=13
            )

        # Inner glossy rim
        canvas.create_arc(
            cx - radius + 12, cy - radius + 12,
            cx + radius - 12, cy + radius - 12,
            start=0,
            extent=180,
            style="arc",
            outline="#FFFFFF",
            width=3
        )

        # Tick marks
        for angle_deg in range(0, 181, 15):
            angle = math.radians(180 - angle_deg)

            outer = radius - 17
            inner = outer - (
                9 if angle_deg % 30 == 0 else 5
            )

            x1 = cx + outer * math.cos(angle)
            y1 = cy - outer * math.sin(angle)
            x2 = cx + inner * math.cos(angle)
            y2 = cy - inner * math.sin(angle)

            canvas.create_line(
                x1, y1, x2, y2,
                fill="#7C91A3",
                width=(
                    2 if angle_deg % 30 == 0 else 1
                )
            )

        # Gauge labels
        for text, angle_deg, color in [
            ("WEAK", 180, DANGER),
            ("MEDIUM", 90, WARNING),
            ("STRONG", 0, SUCCESS)
        ]:
            angle = math.radians(180 - angle_deg)
            label_radius = radius - 37

            x = cx + label_radius * math.cos(angle)
            y = cy - label_radius * math.sin(angle)

            canvas.create_text(
                x, y,
                text=text,
                fill=color,
                font=("Helvetica Neue", 7, "bold")
            )

        # Needle
        needle_angles = {
            "None": 180,
            "Weak": 180,
            "Medium": 90,
            "Strong": 0
        }

        angle = math.radians(
            needle_angles.get(strength, 180)
        )
        needle_length = radius - 43

        nx = cx + needle_length * math.cos(angle)
        ny = cy - needle_length * math.sin(angle)

        # Needle shadow
        canvas.create_line(
            cx + 2, cy + 2,
            nx + 2, ny + 2,
            fill="#D5E2EA",
            width=7,
            capstyle=tk.ROUND
        )

        # Blue needle
        canvas.create_line(
            cx, cy, nx, ny,
            fill=ACCENT,
            width=4,
            capstyle=tk.ROUND
        )

        # Pivot
        canvas.create_oval(
            cx - 10, cy - 10,
            cx + 10, cy + 10,
            fill="#FFFFFF",
            outline="#B8D9E9",
            width=2
        )

        canvas.create_oval(
            cx - 4, cy - 4,
            cx + 4, cy + 4,
            fill=ACCENT,
            outline=""
        )

    # ------------------------------------------------------
    # GENERATE PASSWORD
    # ------------------------------------------------------

    def generate(self):
        selected = [
            name
            for name, variable in self.type_vars.items()
            if variable.get()
        ]

        try:
            password = generate_password(
                self.length_var.get(),
                selected,
                self.exclude_var.get()
            )
        except ValueError as error:
            messagebox.showerror(
                "Invalid Settings",
                str(error),
                parent=self.root
            )
            return

        self.current_password = password
        self.update_password_display()

        strength, color = calculate_strength(
            len(password), len(selected)
        )

        self.strength_label.config(
            text=strength.upper(),
            fg=color
        )

        self.strength_detail.config(
            text=(
                f"{len(password)} characters  •  "
                f"{len(selected)} character types"
            )
        )

        self.draw_speedometer(strength)

        # Keep only the last five generated passwords in memory.
        self.history.insert(0, password)
        self.history = self.history[:5]

        self.history_list.delete(0, tk.END)

        for item in self.history:
            self.history_list.insert(tk.END, item)

        # Automatically copy the new password.
        try:
            pyperclip.copy(password)
        except Exception:
            messagebox.showwarning(
                "Clipboard Unavailable",
                "Password generated, but automatic copying failed. "
                "Use Copy Password to try again.",
                parent=self.root
            )

    # ------------------------------------------------------
    # COPY CURRENT PASSWORD
    # ------------------------------------------------------

    def copy_password(self):
        if not self.current_password:
            messagebox.showinfo(
                "No Password",
                "Generate a password first.",
                parent=self.root
            )
            return

        try:
            pyperclip.copy(self.current_password)
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard.",
                parent=self.root
            )
        except Exception:
            messagebox.showerror(
                "Clipboard Error",
                "Could not access the clipboard.",
                parent=self.root
            )

    # ------------------------------------------------------
    # COPY FROM HISTORY
    # ------------------------------------------------------

    def copy_history_password(self, event=None):
        selection = self.history_list.curselection()

        if not selection:
            return

        password = self.history_list.get(selection[0])

        try:
            pyperclip.copy(password)
            messagebox.showinfo(
                "Copied",
                "Selected password copied to clipboard.",
                parent=self.root
            )
        except Exception:
            messagebox.showerror(
                "Clipboard Error",
                "Could not access the clipboard.",
                parent=self.root
            )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
