import sqlite3

DB_PATH = "data/instrument_booking.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row  # Для доступа к полям по именам в Django
    return conn