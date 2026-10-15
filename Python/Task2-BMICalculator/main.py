
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from database import initialize_database, save_record, get_user_records


# -------------------- Theme --------------------

BG = "#F4F3FA"
WHITE = "#FFFFFF"
TEXT = "#24213D"
MUTED = "#85839B"
PURPLE = "#7055DF"
PURPLE_DARK = "#5B42C8"
BORDER = "#E9E7F2"
GREEN = "#15966A"
ORANGE = "#E99A28"
RED = "#E64B55"

FONT = "Helvetica Neue"


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", ORANGE
    if bmi < 25:
        return "Normal", GREEN
    if bmi < 30:
        return "Overweight", "#E87532"
    return "Obese", RED


# -------------------- Main Window --------------------

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("1100x780")
root.minsize(900, 700)
root.configure(bg=BG)

style = ttk.Style(root)
if "aqua" in style.theme_names():
    style.theme_use("aqua")

style.configure(
    "Modern.TEntry",
    padding=10,
    font=(FONT, 12)
)

style.configure(
    "Modern.Treeview",
    rowheight=35,
    font=(FONT, 10),
    background=WHITE,
    fieldbackground=WHITE
)

style.configure(
    "Modern.Treeview.Heading",
    font=(FONT, 10, "bold")
)


def card(parent, padding=20):
    return tk.Frame(
        parent,
        bg=WHITE,
        padx=padding,
        pady=padding,
        highlightbackground=BORDER,
        highlightthickness=1
    )


def label(parent, text, size=11, color=TEXT, bold=False, **kwargs):
    return tk.Label(
        parent,
        text=text,
        font=(FONT, size, "bold" if bold else "normal"),
        bg=kwargs.pop("bg", WHITE),
        fg=color,
        **kwargs
    )


def button(parent, text, command, primary=False):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=PURPLE if primary else WHITE,
        fg=WHITE if primary else TEXT,
        activebackground=PURPLE_DARK if primary else BG,
        activeforeground=WHITE if primary else TEXT,
        font=(FONT, 11, "bold"),
        relief="flat",
        bd=0,
        padx=15,
        pady=11,
        cursor="hand2"
    )


# -------------------- Database --------------------

try:
    initialize_database()
except RuntimeError as error:
    messagebox.showerror("Database Error", str(error), parent=root)
    root.destroy()
    raise SystemExit(1)


# -------------------- Application Layout --------------------

sidebar = tk.Frame(root, bg="#EFEDFA", width=190)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg=BG)
content.pack(side="left", fill="both", expand=True)

# Sidebar branding
brand = tk.Frame(sidebar, bg="#EFEDFA")
brand.pack(fill="x", padx=18, pady=(28, 32))

logo = tk.Canvas(
    brand, width=44, height=44,
    bg="#EFEDFA", highlightthickness=0
)
logo.pack(side="left")

logo.create_rounded_rectangle = None
logo.create_rectangle(
    2, 2, 42, 42, fill=PURPLE, outline=PURPLE
)
logo.create_text(
    22, 22, text="♥", fill=WHITE,
    font=(FONT, 22, "bold")
)

brand_text = tk.Frame(brand, bg="#EFEDFA")
brand_text.pack(side="left", padx=8)

label(
    brand_text, "BMI Calculator", 11, TEXT, True,
    bg="#EFEDFA"
).pack(anchor="w")

label(
    brand_text, "Your health, your way", 8, MUTED,
    bg="#EFEDFA"
).pack(anchor="w", pady=(3, 0))


def sidebar_action(title, command, selected=False):
    bg = "#DFDAFB" if selected else "#EFEDFA"
    fg = PURPLE_DARK if selected else TEXT

    btn = tk.Button(
        sidebar,
        text=title,
        command=command,
        bg=bg,
        fg=fg,
        activebackground="#DFDAFB",
        activeforeground=PURPLE_DARK,
        font=(FONT, 11, "bold" if selected else "normal"),
        anchor="w",
        padx=15,
        pady=12,
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    btn.pack(fill="x", padx=12, pady=4)
    return btn


# Forward references are resolved when buttons are clicked.
sidebar_action("⌂   Calculate BMI", lambda: name_entry.focus_set(), True)
sidebar_action("◷   History", lambda: show_history())
sidebar_action("▥   Trend Chart", lambda: show_chart())

tk.Frame(sidebar, bg="#EFEDFA").pack(fill="both", expand=True)

label(
    sidebar, "OIBSIP Task 2\nPython Project",
    9, MUTED, bg="#EFEDFA", justify="left"
).pack(anchor="w", padx=22, pady=25)


# -------------------- Header --------------------

header = tk.Frame(content, bg=BG)
header.pack(fill="x", padx=28, pady=(25, 20))

label(
    header, "YOUR WELLNESS", 9, PURPLE, True, bg=BG
).pack(anchor="w")

label(
    header, "Calculate your BMI", 25, TEXT, True, bg=BG
).pack(anchor="w", pady=(5, 3))

label(
    header,
    "Enter your measurements to understand your BMI.",
    11, MUTED, bg=BG
).pack(anchor="w")


# -------------------- Main Cards --------------------

top = tk.Frame(content, bg=BG)
top.pack(fill="x", padx=24)

top.columnconfigure(0, weight=11, uniform="cards")
top.columnconfigure(1, weight=9, uniform="cards")

# Input card
form_card = card(top, 18)
form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

label(
    form_card, "♙  Personal information", 14, TEXT, True
).pack(anchor="w", pady=(0, 18))


def create_field(parent, title, placeholder):
    label(parent, title, 10, TEXT, True).pack(anchor="w", pady=(0, 5))

    entry = ttk.Entry(parent, style="Modern.TEntry")
    entry.pack(fill="x", pady=(0, 13))
    entry.insert(0, placeholder)

    def clear_placeholder(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")

    def restore_placeholder(event):
        if not entry.get().strip():
            entry.insert(0, placeholder)

    entry.bind("<FocusIn>", clear_placeholder)
    entry.bind("<FocusOut>", restore_placeholder)

    return entry


name_entry = create_field(form_card, "Full name", "Enter your name")

measurements = tk.Frame(form_card, bg=WHITE)
measurements.pack(fill="x")

measurements.columnconfigure(0, weight=1)
measurements.columnconfigure(1, weight=1)

weight_frame = tk.Frame(measurements, bg=WHITE)
weight_frame.grid(row=0, column=0, sticky="ew", padx=(0, 7))

height_frame = tk.Frame(measurements, bg=WHITE)
height_frame.grid(row=0, column=1, sticky="ew", padx=(7, 0))

weight_entry = create_field(
    weight_frame, "Weight (kg)", "e.g. 70"
)
height_entry = create_field(
    height_frame, "Height (m)", "e.g. 1.75"
)

calculate_button = button(
    form_card, "Calculate BMI   →", lambda: calculate_bmi(), True
)
calculate_button.pack(fill="x", pady=(3, 0))


# Result card
result_card = card(top, 18)
result_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

label(result_card, "✚  Your result", 14, TEXT, True).pack(anchor="w")

label(
    result_card, "BODY MASS INDEX", 9, MUTED, True
).pack(anchor="w", pady=(22, 3))

result_value = label(
    result_card, "--", 37, TEXT, True
)
result_value.pack(anchor="w")

result_category = label(
    result_card, "AWAITING RESULT", 11, MUTED, True
)
result_category.pack(anchor="w", pady=(0, 8))

result_hint = label(
    result_card,
    "Your result will appear here after calculation.",
    10, MUTED, wraplength=250, justify="left"
)
result_hint.pack(anchor="w", pady=(0, 16))

# BMI scale
scale = tk.Canvas(
    result_card, height=14, bg=WHITE, highlightthickness=0
)
scale.pack(fill="x", pady=(0, 10))

segments = [
    (0.0, 0.25, ORANGE),
    (0.25, 0.50, GREEN),
    (0.50, 0.75, "#E87532"),
    (0.75, 1.0, RED),
]

def draw_scale(bmi=None):
    scale.delete("all")
    width = max(scale.winfo_width(), 220)

    for start, end, color in segments:
        scale.create_rectangle(
            width * start, 2, width * end - 3, 11,
            fill=color, outline=color
        )

    if bmi is not None:
        # Map BMI 10–40 onto the scale.
        position = max(0, min(1, (bmi - 10) / 30))
        x = width * position
        scale.create_line(
            x, 0, x, 14, fill=TEXT, width=3
        )

scale.bind("<Configure>", lambda event: draw_scale())
scale.after(100, draw_scale)

category_range = label(
    result_card, "BMI categories: Underweight · Normal · Overweight · Obese",
    8, MUTED, wraplength=260, justify="left"
)
category_range.pack(anchor="w", pady=(5, 0))


# -------------------- BMI Categories --------------------

categories_card = card(content, 16)
categories_card.pack(fill="x", padx=24, pady=(16, 0))

label(
    categories_card, "BMI categories", 13, TEXT, True
).pack(anchor="w", pady=(0, 12))

category_row = tk.Frame(categories_card, bg=WHITE)
category_row.pack(fill="x")

category_data = [
    ("Underweight", "< 18.5", ORANGE, "#FFF7E8"),
    ("Normal", "18.5 – 24.9", GREEN, "#EAF8F2"),
    ("Overweight", "25 – 29.9", "#E87532", "#FFF1E9"),
    ("Obese", "≥ 30", RED, "#FFF0F0"),
]

for title, value, color, bg_color in category_data:
    item = tk.Frame(
        category_row, bg=bg_color, padx=8, pady=11
    )
    item.pack(side="left", fill="both", expand=True, padx=3)

    label(
        item, title, 9, color, True, bg=bg_color
    ).pack(anchor="w")

    label(
        item, value, 10, TEXT, bg=bg_color
    ).pack(anchor="w", pady=(5, 0))


# -------------------- History and Trend --------------------

actions = tk.Frame(content, bg=BG)
actions.pack(fill="x", padx=24, pady=16)

actions.columnconfigure(0, weight=1)
actions.columnconfigure(1, weight=1)

history_card = tk.Frame(
    actions, bg="#F0ECFF", padx=16, pady=15
)
history_card.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

label(
    history_card, "◷  View your history", 11, PURPLE_DARK, True,
    bg="#F0ECFF"
).pack(anchor="w")

label(
    history_card, "Review your previous BMI records.",
    9, MUTED, bg="#F0ECFF", wraplength=210, justify="left"
).pack(anchor="w", pady=(7, 12))

button(
    history_card,
    "Open history  →",
    lambda: show_history(),
    True
).pack(fill="x")

trend_card = tk.Frame(
    actions, bg="#EAF1FF", padx=16, pady=15
)
trend_card.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

label(
    trend_card, "▥  BMI trend chart", 11, "#3D65C7", True,
    bg="#EAF1FF"
).pack(anchor="w")

label(
    trend_card, "See how your measurements change over time.",
    9, MUTED, bg="#EAF1FF", wraplength=210, justify="left"
).pack(anchor="w", pady=(7, 12))

button(
    trend_card,
    "Open trend  →",
    lambda: show_chart(),
    True
).pack(fill="x")

status_label = label(
    content, "Your records are stored locally on this Mac.",
    9, MUTED, bg=BG
)
status_label.pack(anchor="w", padx=28, pady=(0, 15))


# -------------------- Functional Features --------------------

def calculate_bmi():
    username = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if username in ("", "Enter your name"):
        messagebox.showerror(
            "Missing name", "Please enter your name.", parent=root
        )
        name_entry.focus_set()
        return

    try:
        weight = float(weight_text)
        height = float(height_text)

        if weight <= 0 or height <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid measurements",
            "Enter a positive numeric weight and height.\n\n"
            "Example: 70 kg and 1.75 m.",
            parent=root
        )
        return

    bmi = weight / (height * height)
    category, color = classify_bmi(bmi)

    result_value.config(text=f"{bmi:.2f}", fg=color)
    result_category.config(text=category.upper(), fg=color)

    if category == "Normal":
        hint = "Your BMI is within the standard adult healthy range."
    else:
        hint = f"Your BMI falls in the {category.lower()} category."

    result_hint.config(text=hint)
    category_range.config(
        text=f"Your category: {category}  ·  BMI {bmi:.2f}"
    )
    draw_scale(bmi)

    try:
        save_record(username, weight, height, bmi, category)
        status_label.config(
            text=f"✓  Record saved locally for {username}",
            fg=GREEN
        )
    except RuntimeError as error:
        status_label.config(text="Unable to save record.", fg=RED)
        messagebox.showerror("Database Error", str(error), parent=root)


def show_history():
    username = name_entry.get().strip()

    if not username or username == "Enter your name":
        messagebox.showerror(
            "Name required",
            "Enter a user's name to view their history.",
            parent=root
        )
        return

    try:
        records = get_user_records(username)
    except RuntimeError as error:
        messagebox.showerror("Database Error", str(error), parent=root)
        return

    if not records:
        messagebox.showinfo(
            "BMI History",
            f"No records found for {username}.",
            parent=root
        )
        return

    window = tk.Toplevel(root)
    window.title(f"BMI History — {username}")
    window.geometry("760x420")
    window.configure(bg=BG)

    label(
        window, f"{username}'s history", 20, TEXT, True, bg=BG
    ).pack(anchor="w", padx=22, pady=(22, 15))

    columns = ("date", "weight", "height", "bmi", "category")
    table = ttk.Treeview(
        window, columns=columns, show="headings",
        style="Modern.Treeview"
    )

    headers = {
        "date": "Date and time",
        "weight": "Weight (kg)",
        "height": "Height (m)",
        "bmi": "BMI",
        "category": "Category",
    }

    for column, title in headers.items():
        table.heading(column, text=title)
        table.column(column, width=135, anchor="center")

    for weight, height, bmi, category, recorded_at in records:
        table.insert(
            "", "end",
            values=(
                recorded_at, f"{weight:.1f}",
                f"{height:.2f}", f"{bmi:.2f}", category
            )
        )

    table.pack(fill="both", expand=True, padx=22, pady=(0, 22))


def show_chart():
    username = name_entry.get().strip()

    if not username or username == "Enter your name":
        messagebox.showerror(
            "Name required",
            "Enter a user's name to view their BMI trend.",
            parent=root
        )
        return

    try:
        records = get_user_records(username)
    except RuntimeError as error:
        messagebox.showerror("Database Error", str(error), parent=root)
        return

    if not records:
        messagebox.showinfo(
            "BMI Trend", "No saved records to plot.", parent=root
        )
        return

    dates = [record[4] for record in records]
    values = [record[2] for record in records]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#F4F3FA")
    ax.set_facecolor("white")

    ax.plot(
        dates, values,
        marker="o", linewidth=2.5,
        color=PURPLE, markersize=7
    )

    ax.axhline(18.5, color=ORANGE, linestyle="--", label="18.5")
    ax.axhline(25, color=GREEN, linestyle="--", label="25")
    ax.axhline(30, color=RED, linestyle="--", label="30")

    ax.set_title(f"BMI history for {username}", pad=15)
    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.grid(alpha=0.2)
    ax.legend(title="Reference values")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


root.mainloop()
