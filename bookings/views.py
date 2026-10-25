from django.shortcuts import render
from models.bookings import find_booking_by_id
from storage import load_bookings, load_instruments, load_users

INSTRUMENTS_FILE = "data/instruments.json"
USERS_FILE = "data/users.json"
BOOKINGS_FILE = "data/bookings.json"


def bookings(request):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(BOOKINGS_FILE, instruments_list, users_list)

    context = {"bookings": bookings_list}
    return render(request, "bookings/booking_list.html", context)


def booking_detail(request, booking_id: int):
    instruments_list = load_instruments(INSTRUMENTS_FILE)
    users_list = load_users(USERS_FILE)
    bookings_list = load_bookings(BOOKINGS_FILE, instruments_list, users_list)

    booking = find_booking_by_id(bookings_list, booking_id)
    context = {"booking": booking}

    return render(
        request,
        "bookings/booking_detail.html",
        context,
        status=404 if booking is None else 200
    )