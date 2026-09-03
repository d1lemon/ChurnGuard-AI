
import sqlite3


DATABASE_NAME = "predictions.db"


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """
    Create the predictions table if it does not already exist.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            model_version TEXT NOT NULL,
            prediction INTEGER NOT NULL,
            churn_probability REAL NOT NULL,
            risk_level TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
