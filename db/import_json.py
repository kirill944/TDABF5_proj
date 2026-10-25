import json
from db.database import get_connection

INSTRUMENTS_FILE = "data/instruments.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"

def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)

def import_instruments(conn):
    instruments = load_json(INSTRUMENTS_FILE)
    conn.executemany(
        "INSERT INTO instruments (id, name, price) VALUES (?, ?, ?)",
        [(i["id"], i["name"], i["price"]) for i in instruments],
    )

def import_users(conn):
    users = load_json(USERS_FILE)
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u["email"]) for u in users],
    )

def import_bookings(conn):
    bookings = load_json(BOOKINGS_FILE)
    conn.executemany(
        "INSERT INTO bookings (id, instrument_id, user_id, booking_date, is_cancelled) VALUES (?, ?, ?, ?, ?)",
        [
            (b["id"], b["instrument_id"], b["user_id"], b["booking_date"], int(b["is_cancelled"]))
            for b in bookings
        ],
    )

def main():
    conn = get_connection()
    try:
        import_instruments(conn)
        import_users(conn)
        import_bookings(conn)
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()