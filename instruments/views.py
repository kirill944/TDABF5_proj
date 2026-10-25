import sqlite3
from django.shortcuts import render

DB_PATH = "data/instrument_booking.sqlite"


def instruments(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    instruments_list = conn.execute("SELECT id, name, price FROM instruments ORDER BY name").fetchall()
    conn.close()
    return render(request, "instruments/instrument_list.html", {"instruments": instruments_list})


def instrument_detail(request, instrument_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Получаем инструмент
    instrument = conn.execute("SELECT * FROM instruments WHERE id = ?", (instrument_id,)).fetchone()

    if instrument:
        # Проверяем, есть ли активные бронирования
        active = conn.execute(
            "SELECT COUNT(*) as count FROM bookings WHERE instrument_id = ? AND is_cancelled = 0",
            (instrument_id,)
        ).fetchone()
        is_available = active['count'] == 0
    else:
        is_available = False

    conn.close()
    context = {"instrument": instrument, "is_available": is_available}
    return render(request, "instruments/instrument_detail.html", context, status=404 if instrument is None else 200)

def available_instruments(request):
    booking_date = request.GET.get("date")
    instruments_list = []

    if booking_date:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Параметризованный запрос (передаем дату через ?)
        instruments_list = conn.execute("""
                                        SELECT id, name, price
                                        FROM instruments
                                        WHERE id NOT IN (SELECT instrument_id
                                                         FROM bookings
                                                         WHERE booking_date = ?
                                                           AND is_cancelled = 0)
                                        ORDER BY name;
                                        """, (booking_date,)).fetchall()
        conn.close()

    return render(
        request,
        "instruments/available.html",
        {"instruments": instruments_list, "booking_date": booking_date}
    )