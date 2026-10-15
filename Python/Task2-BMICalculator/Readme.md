# BMI Calculator — OIBSIP Task 2

A Python-based Body Mass Index (BMI) Calculator that calculates BMI from a user's weight and height, classifies the result into standard BMI categories, and stores historical records for multiple users using SQLite.

## Features

- **BMI Calculation:** Calculates BMI using weight in kilograms and height in meters.
- **BMI Classification:** Categorizes results as Underweight, Normal, Overweight, or Obese.
- **Input Validation:** Handles non-numeric inputs, empty fields, zero values, and negative measurements.
- **Two-Decimal Precision:** Displays BMI results rounded to two decimal places.
- **Multi-User Support:** Stores BMI records for different users.
- **Data Persistence:** Saves historical records in an SQLite database.
- **BMI History:** Retrieves and displays previously saved records for a selected user.
- **Trend Visualization:** Generates a line chart to track BMI changes over time.
- **Error Handling:** Handles database read and write errors with informative messages.

## Technologies Used

- **Python** — Core programming language
- **Tkinter** — Python's standard GUI library
- **SQLite** — Local database for storing BMI records
- **Matplotlib** — BMI trend visualization

## BMI Formula

BMI is calculated using the following formula:

```text
BMI = Weight (kg) / Height (m)²
```

**Example:**

For a person weighing 70 kg with a height of 1.75 m:

```text
BMI = 70 / (1.75 × 1.75)
BMI = 22.86
```

## BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25.0 – 29.9 | Overweight |
| 30.0 or above | Obese |

These categories are intended for adults and should not be used as a standalone medical diagnosis.

## Project Structure

```text
BMI-Calculator/
├── main.py             # Application logic and BMI calculations
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── bmi_records.db      # Generated automatically
```

The database file is created automatically when the application starts successfully.

## Requirements

- Python 3.10 or later recommended
- Tkinter
- SQLite3
- Matplotlib

Tkinter and SQLite3 are included with many Python installations. Their availability depends on your Python distribution.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/FarazMemon004/OIBSIP/tree/main/Python/Task2-BMICalculator
cd BMI-Calculator
```

Replace `https://github.com/FarazMemon004/OIBSIP/tree/main/Python/Task2-BMICalculator` with your GitHub username.

### 2. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
matplotlib
```

### 4. Run the Application

```bash
python main.py
```

## How to Use

1. Start the application.
2. Enter the user's name.
3. Enter weight in kilograms.
4. Enter height in meters.
5. Calculate BMI to see the result and its category.
6. View the user's saved records through the history feature.
7. Open the trend chart to visualize historical BMI measurements.

Each calculation is saved to the local SQLite database, allowing records to be retrieved in future sessions.

## Database

The application uses SQLite to store the following information:

- Record ID
- Username
- Weight
- Height
- BMI value
- BMI category
- Date and time of calculation

Records are associated with usernames so that different users can view their own histories.

**Privacy note:** Records are stored locally in the project's database file. Avoid sharing the database publicly if it contains personal information.

## Error Handling

The application validates user input and handles common errors, including:

- Missing usernames
- Non-numeric weight or height
- Zero or negative measurements
- Missing historical records
- SQLite database read and write failures

## Future Improvements

- Add BMI goal tracking.
- Support exporting records to CSV.
- Add date-range filters for historical data.
- Introduce user authentication.
- Add automated unit tests.
- Improve accessibility and localization.

## Project Objective

This project was developed as part of **Oasis Infobyte Internship (OIBSIP) — Python Programming Task 2** to practice Python programming, input validation, database management, and data visualization.

## Author

**Muhammad Faraz**

GitHub: https://github.com/FarazMemon004

## Disclaimer

BMI is a general screening measure and does not directly measure body fat or overall health. Consult a qualified healthcare professional for personalized medical advice.

## License

This project is available for educational and learning purposes. Add a license file if you intend to distribute it under specific terms.
