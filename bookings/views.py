import sqlite3
from django.shortcuts import render

DB_PATH = "data/instrument_booking.sqlite"


def bookings(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # JOIN запрос для получения полной информации
    bookings_data = conn.execute("""
                                 SELECT b.id, b.booking_date, i.name AS instrument_name, u.name AS user_name
                                 FROM bookings b
                                          JOIN instruments i ON b.instrument_id = i.id
                                          JOIN users u ON b.user_id = u.id
                                 WHERE b.is_cancelled = 0
                                 ORDER BY b.booking_date;
                                 """).fetchall()
    conn.close()
    return render(request, "bookings/booking_list.html", {"bookings": bookings_data})


def statistics(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # GROUP BY запрос
    stats = conn.execute("""
                         SELECT i.name AS instrument_name, COUNT(b.id) AS bookings_count
                         FROM instruments i
                                  LEFT JOIN bookings b ON i.id = b.instrument_id AND b.is_cancelled = 0
                         GROUP BY i.id, i.name
                         ORDER BY bookings_count DESC;
                         """).fetchall()
    conn.close()
    return render(request, "bookings/statistics.html", {"statistics": stats})


def booking_detail(request, booking_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Используем JOIN, чтобы получить имена инструмента и пользователя
    booking = conn.execute("""
                           SELECT b.id,
                                  b.booking_date,
                                  b.is_cancelled,
                                  i.name AS instrument_name,
                                  u.name AS user_name
                           FROM bookings b
                                    JOIN instruments i ON b.instrument_id = i.id
                                    JOIN users u ON b.user_id = u.id
                           WHERE b.id = ?
                           """, (booking_id,)).fetchone()
    conn.close()

    context = {
        "booking": booking
    }

    # Если бронирование не найдено, возвращаем статус 404
    return render(
        request,
        "bookings/booking_detail.html",
        context,
        status=404 if booking is None else 200
    )