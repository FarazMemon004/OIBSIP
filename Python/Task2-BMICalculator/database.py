
import sqlite3
from datetime import datetime

DB_NAME = "bmi_records.db"


def initialize_database():
    try:
        with sqlite3.connect(DB_NAME) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
            """)
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not initialize database: {error}"
        ) from error


def save_record(username, weight, height, bmi, category):
    try:
        with sqlite3.connect(DB_NAME) as connection:
            connection.execute("""
                INSERT INTO bmi_records
                (username, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username,
                weight,
                height,
                bmi,
                category,
                datetime.now().isoformat(timespec="seconds")
            ))
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not save BMI record: {error}"
        ) from error


def get_user_records(username):
    try:
        with sqlite3.connect(DB_NAME) as connection:
            return connection.execute("""
                SELECT weight, height, bmi, category, recorded_at
                FROM bmi_records
                WHERE username = ?
                ORDER BY recorded_at ASC, id ASC
            """, (username,)).fetchall()
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not read BMI records: {error}"
        ) from error
