# 🔐 Password Studio — Random Password Generator

A secure and customizable password generator built with Python. Password Studio helps users create strong random passwords with adjustable length, character-type selection, password strength visualization, and clipboard support.

## ✨ Features

- **Secure Password Generation:** Uses Python's `secrets` module for cryptographically strong random passwords.
- **Custom Password Length:** Choose a password length from 8 to 64 characters.
- **Character Type Selection:** Include any combination of:
  - Uppercase letters (`A-Z`)
  - Lowercase letters (`a-z`)
  - Numbers (`0-9`)
  - Special symbols (`!@#$...`)
- **Password Strength Indicator:** Displays Weak, Medium, or Strong based on password length and selected character types.
- **Automatic Clipboard Copy:** Generated passwords are automatically copied to the clipboard.
- **Copy Password:** Copy the current password whenever needed.
- **Show/Hide Password:** Toggle password visibility.
- **Exclude Ambiguous Characters:** Optionally exclude characters such as `0`, `O`, `1`, `l`, and `I`.
- **Recent Password History:** Keeps the last five generated passwords in memory during the current session.
- **Keyboard Shortcuts:** Use `Command + G` to generate a password and `Command + C` to copy the current password.

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** — graphical user interface
- **secrets** — secure random password generation
- **string** — character sets
- **math** — speedometer visualization
- **pyperclip** — clipboard integration

## 📋 Requirements

- Python 3.10 or later recommended
- Tkinter
- pyperclip

Tkinter is included with many Python installations. Availability depends on how Python was installed.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/FarazMemon004/OIBSIP/tree/main/Python/Task3-RandomPasswordGenerator
```

### 2. Navigate to the Project Directory

```bash
cd OIBSIP-Python-Task3-Password-Generator
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 4. Activate the Virtual Environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
python -m pip install pyperclip
```

### 6. Run the Application

```bash
python main.py
```

## 📖 How to Use

1. Launch Password Studio.
2. Set the desired password length using the volume-style slider.
3. Select at least two character types.
4. Optionally enable the ambiguous-character exclusion setting.
5. Click **Generate Secure Password**.
6. View the generated password and its estimated strength.
7. The password is automatically copied to your clipboard.
8. Use **Copy Password** to copy it again or double-click a password in the recent history to copy it.

## 🔒 Security Notes

- Passwords are generated using Python's `secrets` module instead of the non-cryptographic `random` module.
- At least one character from each selected character type is included in every generated password.
- Recent password history is stored only in application memory and is not saved to a file or database.
- The displayed strength indicator is a simple estimate based on password length and the number of selected character types. It is not a formal security audit.
- Avoid sharing generated passwords or storing them in public repositories.
- Clipboard contents may remain available to other applications until overwritten.

## 📁 Project Structure

```text
OIBSIP-Python-Task3-Password-Generator/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 📦 requirements.txt

Create a `requirements.txt` file containing:

```text
pyperclip
```

Tkinter is provided separately by the Python installation on supported systems.

## 🎯 Project Objective

This project was developed as part of the **Oasis Infobyte Internship Program (OIBSIP) — Python Programming, Task 3: Random Password Generator**.

The objective is to practice Python programming, secure random generation, GUI development, user input validation, and clipboard integration.

## 👨‍💻 Author

Muhammad Faraz

GitHub: [FarazMemon004](https://github.com/FarazMemon004)

[Muhammad Faraz Memon](https://www.linkedin.com/in/muhammad-faraz-memon-92582a43a/)


---

⭐ If you find this project useful, consider giving the repository a star.
