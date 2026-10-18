from django.shortcuts import render
from django.http import HttpResponse

from homepage.views import page
from models.bookings import find_booking_by_id
from storage import (
    load_bookings,
    load_instruments,
    load_users,
)

INSTRUMENTS_FILE = "data/instruments.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def bookings(request):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE, instruments_list, users_list,
    )

    items = ""
    for booking in bookings_list:
        status = "отменено" if booking.is_cancelled else "активно"
        badge = "bg-secondary" if booking.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/bookings/{booking.id}/">
                {booking.instrument.name} — {booking.booking_date}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Бронирования</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Instrument Booking — бронирования", content))


def booking_detail(request, booking_id: int):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE, instruments_list, users_list,
    )
    booking = find_booking_by_id(bookings_list, booking_id)

    if booking is None:
        content = """
        <h1 class="text-danger">Бронирование не найдено</h1>
        <a href="/bookings/" class="btn btn-outline-secondary">
            ← к списку бронирований
        </a>
        """
        return HttpResponse(
            page("Бронирование не найдено", content),
            status=404,
        )

    status = "отменено" if booking.is_cancelled else "активно"
    badge = "bg-secondary" if booking.is_cancelled else "bg-success"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Бронирование №{booking.id}</h5>
            <p class="card-text">
                Инструмент: {booking.instrument.name}
            </p>
            <p class="card-text">Дата: {booking.booking_date}</p>
            <p class="card-text">Пользователь: {booking.user.name}</p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/bookings/" class="btn btn-outline-secondary">
                ← к списку бронирований
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Бронирование №{booking.id}", content),
    )