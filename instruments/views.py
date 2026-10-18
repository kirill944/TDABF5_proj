from django.shortcuts import render
from django.http import HttpResponse

from homepage.views import page
from models.instruments import find_instrument_by_id
from models.bookings import is_instrument_available
from storage import (
    load_bookings,
    load_instruments,
    load_users,
)

INSTRUMENTS_FILE = "data/instruments.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def instruments(request):
    items = ""
    for ins in load_instruments(INSTRUMENTS_FILE):
        text = f"{ins.name} — {ins.price} руб."
        items += (
            f'<li class="list-group-item">'
            f'<a href="/instruments/{ins.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Инструменты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Instrument Booking — инструменты", content))


def instrument_detail(request, instrument_id: int):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    instrument = find_instrument_by_id(instruments_list, instrument_id)

    if instrument is None:
        content = """
        <h1 class="text-danger">Инструмент не найден</h1>
        <a href="/instruments/" class="btn btn-outline-secondary">
            ← к списку инструментов
        </a>
        """
        return HttpResponse(
            page("Инструмент не найден", content),
            status=404,
        )

    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(
        BOOKINGS_FILE, instruments_list, users_list,
    )

    # Для простоты показываем статус свободен/занят без привязки к дате:
    # проверяем, есть ли хотя бы одно активное бронирование
    active = [
        b for b in bookings_list
        if b.instrument.id == instrument.id and not b.is_cancelled
    ]
    available = not active
    status = "свободен" if available else "занят"
    badge = "bg-success" if available else "bg-danger"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{instrument.name}</h5>
            <p class="card-text"><strong>ID:</strong> {instrument.id}</p>
            <p class="card-text">
                <strong>Цена:</strong> {instrument.price} руб.
            </p>
            <p class="card-text">
                Статус:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/instruments/" class="btn btn-outline-secondary">
                ← к списку инструментов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(instrument.name, content))