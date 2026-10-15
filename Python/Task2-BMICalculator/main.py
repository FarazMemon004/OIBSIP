
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt

from database import (
    initialize_database,
    save_record,
    get_user_records,
)


# ---------- macOS-inspired palette ----------

BG = "#F5F5F7"
CARD = "#FFFFFF"
TEXT = "#1D1D1F"
MUTED = "#86868B"
PURPLE = "#7357D9"
BORDER = "#E5E5EA"


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#D97706"
    elif bmi < 25:
        return "Normal", "#248A55"
    elif bmi < 30:
        return "Overweight", "#D97706"
    return "Obese", "#D93025"


def show_error(title, message):
    messagebox.showerror(title, message, parent=root)


def calculate_bmi():
    username = name_entry.get().strip()

    if not username:
        show_error("Missing Name", "Please enter your name.")
        name_entry.focus_set()
        return

    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError

    except ValueError:
        show_error(
            "Invalid Measurements",
            "Enter valid positive numbers for weight and height."
        )
        return

    bmi = weight / (height ** 2)
    category, color = classify_bmi(bmi)

    result_value.config(text=f"{bmi:.2f}", fg=color)
    result_category.config(
        text=category.upper(),
        fg=color
    )
    result_hint.config(
        text="Your BMI has been calculated.",
        fg=MUTED
    )

    try:
        save_record(username, weight, height, bmi, category)
        status_label.config(
            text=f"Record saved for {username}",
            fg=MUTED
        )
    except RuntimeError as error:
        status_label.config(text="Record could not be saved", fg="#D93025")
        show_error("Database Error", str(error))


def show_history():
    username = name_entry.get().strip()

    if not username:
        show_error("Missing Name", "Enter a name to view history.")
        return

    try:
        records = get_user_records(username)
    except RuntimeError as error:
        show_error("Database Error", str(error))
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
    window.geometry("760x400")
    window.configure(bg=BG)

    container = tk.Frame(window, bg=BG, padx=24, pady=24)
    container.pack(fill="both", expand=True)

    tk.Label(
        container,
        text=f"{username}'s History",
        font=("Helvetica Neue", 22, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 16))

    columns = ("date", "weight", "height", "bmi", "category")
    tree = ttk.Treeview(
        container, columns=columns, show="headings"
    )

    labels = {
        "date": "Recorded At",
        "weight": "Weight (kg)",
        "height": "Height (m)",
        "bmi": "BMI",
        "category": "Category",
    }

    for column, label in labels.items():
        tree.heading(column, text=label)
        tree.column(column, width=130, anchor="center")

    scrollbar = ttk.Scrollbar(
        container, orient="vertical", command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    for weight, height, bmi, category, recorded_at in records:
        tree.insert(
            "",
            "end",
            values=(
                recorded_at,
                f"{weight:.1f}",
                f"{height:.2f}",
                f"{bmi:.2f}",
                category,
            )
        )

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def show_chart():
    username = name_entry.get().strip()

    if not username:
        show_error("Missing Name", "Enter a name to view the trend.")
        return

    try:
        records = get_user_records(username)
    except RuntimeError as error:
        show_error("Database Error", str(error))
        return

    if not records:
        messagebox.showinfo(
            "BMI Trend",
            "No saved records are available for this user.",
            parent=root
        )
        return

    dates = [record[4] for record in records]
    values = [record[2] for record in records]

    plt.figure(figsize=(9, 5))
    plt.plot(dates, values, marker="o", linewidth=2)
    plt.axhline(18.5, linestyle="--", label="18.5")
    plt.axhline(25, linestyle="--", label="25")
    plt.axhline(30, linestyle="--", label="30")

    plt.title(f"BMI Trend — {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=30, ha="right")
    plt.grid(alpha=0.2)
    plt.legend(title="Reference levels")
    plt.tight_layout()
    plt.show()


# ---------- Application ----------

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("540x720")
root.minsize(480, 680)
root.configure(bg=BG)

# Use the native macOS Aqua theme when available.
style = ttk.Style(root)

if "aqua" in style.theme_names():
    style.theme_use("aqua")

style.configure(
    "Mac.TEntry",
    padding=9,
    font=("Helvetica Neue", 13)
)

style.configure(
    "Mac.TButton",
    padding=(12, 9),
    font=("Helvetica Neue", 12)
)

try:
    initialize_database()
except RuntimeError as error:
    messagebox.showerror("Database Error", str(error), parent=root)
    root.destroy()
    raise SystemExit(1)


# Main scroll-free content area
main = tk.Frame(root, bg=BG, padx=28, pady=24)
main.pack(fill="both", expand=True)

# Header
tk.Label(
    main,
    text="HEALTH",
    font=("Helvetica Neue", 10, "bold"),
    bg=BG,
    fg=PURPLE
).pack(anchor="w")

tk.Label(
    main,
    text="BMI Calculator",
    font=("Helvetica Neue", 29, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(3, 2))

tk.Label(
    main,
    text="A simple overview of your body mass index.",
    font=("Helvetica Neue", 12),
    bg=BG,
    fg=MUTED
).pack(anchor="w", pady=(0, 22))


# Measurement card
form_card = tk.Frame(
    main, bg=CARD, padx=20, pady=18,
    highlightbackground=BORDER, highlightthickness=1
)
form_card.pack(fill="x")

tk.Label(
    form_card,
    text="Your measurements",
    font=("Helvetica Neue", 16, "bold"),
    bg=CARD,
    fg=TEXT
).pack(anchor="w", pady=(0, 14))


def add_field(parent, label, placeholder=None):
    tk.Label(
        parent,
        text=label,
        font=("Helvetica Neue", 11, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 5))

    entry = ttk.Entry(
        parent, style="Mac.TEntry", font=("Helvetica Neue", 13)
    )
    entry.pack(fill="x", pady=(0, 13))
    return entry


name_entry = add_field(form_card, "Name")
weight_entry = add_field(form_card, "Weight  ·  kg")
height_entry = add_field(form_card, "Height  ·  meters")

calculate_button = tk.Button(
    form_card,
    text="Calculate BMI",
    command=calculate_bmi,
    bg=PURPLE,
    fg="white",
    activebackground="#5F43C4",
    activeforeground="white",
    font=("Helvetica Neue", 13, "bold"),
    relief="flat",
    bd=0,
    padx=12,
    pady=11,
    cursor="pointinghand"
)
calculate_button.pack(fill="x", pady=(0, 2))


# Result card
result_card = tk.Frame(
    main,
    bg=CARD,
    padx=20,
    pady=16,
    highlightbackground=BORDER,
    highlightthickness=1
)
result_card.pack(fill="x", pady=(16, 0))

tk.Label(
    result_card,
    text="YOUR RESULT",
    font=("Helvetica Neue", 10, "bold"),
    bg=CARD,
    fg=MUTED
).pack(anchor="w")

result_value = tk.Label(
    result_card,
    text="--",
    font=("Helvetica Neue", 35, "bold"),
    bg=CARD,
    fg=TEXT
)
result_value.pack(anchor="w", pady=(3, 0))

result_category = tk.Label(
    result_card,
    text="AWAITING MEASUREMENTS",
    font=("Helvetica Neue", 11, "bold"),
    bg=CARD,
    fg=MUTED
)
result_category.pack(anchor="w", pady=(0, 4))

result_hint = tk.Label(
    result_card,
    text="Enter your measurements to get started.",
    font=("Helvetica Neue", 11),
    bg=CARD,
    fg=MUTED
)
result_hint.pack(anchor="w")


# History and chart actions
actions = tk.Frame(main, bg=BG)
actions.pack(fill="x", pady=(16, 0))

history_button = ttk.Button(
    actions,
    text="View History",
    command=show_history,
    style="Mac.TButton"
)
history_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

chart_button = ttk.Button(
    actions,
    text="View Trend",
    command=show_chart,
    style="Mac.TButton"
)
chart_button.pack(side="left", fill="x", expand=True, padx=(5, 0))


status_label = tk.Label(
    main,
    text="Your records are stored locally on this Mac.",
    font=("Helvetica Neue", 10),
    bg=BG,
    fg=MUTED
)
status_label.pack(anchor="w", pady=(14, 0))

root.mainloop()
