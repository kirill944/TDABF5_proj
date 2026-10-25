-- ============================================
-- Instrument Booking: структура базы данных
-- ============================================

CREATE TABLE IF NOT EXISTS instruments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    instrument_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (instrument_id) REFERENCES instruments(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);