from django.shortcuts import render
from models.instruments import find_instrument_by_id
from storage import load_bookings, load_instruments, load_users

INSTRUMENTS_FILE = "data/instruments.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def instruments(request):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    context = {"instruments": instruments_list}
    return render(request, "instruments/instrument_list.html", context)


def instrument_detail(request, instrument_id: int):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    instrument = find_instrument_by_id(instruments_list, instrument_id)

    if instrument:
        users_list = load_users(USERS_FILE)
        bookings_list = load_bookings(BOOKINGS_FILE, instruments_list, users_list)
        active = [b for b in bookings_list if b.instrument.id == instrument.id and not b.is_cancelled]
        is_available = not active
    else:
        is_available = False

    context = {
        "instrument": instrument,
        "is_available": is_available,
    }
    return render(
        request,
        "instruments/instrument_detail.html",
        context,
        status=404 if instrument is None else 200
    )