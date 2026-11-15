"""Тесты для класса Booking и функций работы с бронированиями."""
from models import Booking, Instrument, User
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    is_instrument_available,
)


def _make_room():
    return Instrument(1, 'Скрипка', 30000)


def _make_user():
    return User(1, 'Иван Петров', 'ivan@example.com')


def test_booking_creation():
    instrument = _make_room()
    user = _make_user()
    booking = Booking(1, instrument, user, '2026-09-15')

    assert booking.id == 1
    assert booking.instrument is instrument
    assert booking.user is user
    assert booking.booking_date == '2026-09-15'
    assert booking.is_cancelled is False


def test_booking_cancel():
    booking = Booking(1, _make_room(), _make_user(), '2026-09-15')
    booking.cancel()
    assert booking.is_cancelled is True


def test_booking_str_active():
    booking = Booking(1, _make_room(), _make_user(), '2026-09-15')
    assert 'активно' in str(booking)
    assert 'Скрипка' in str(booking)


def test_booking_str_cancelled():
    booking = Booking(1, _make_room(), _make_user(), '2026-09-15')
    booking.cancel()
    assert 'отменено' in str(booking)


def test_is_instrument_available_true():
    bookings = []
    assert is_instrument_available(bookings, _make_room(),
                                   '2026-09-15') is True


def test_is_instrument_available_false():
    instrument = _make_room()
    user = _make_user()
    bookings = [Booking(1, instrument, user, '2026-09-15')]
    assert is_instrument_available(bookings, instrument, '2026-09-15') is False


def test_is_instrument_available_other_date():
    instrument = _make_room()
    user = _make_user()
    bookings = [Booking(1, instrument, user, '2026-09-15')]
    assert is_instrument_available(bookings, instrument, '2026-09-16') is True


def test_cancelled_does_not_block():
    instrument = _make_room()
    user = _make_user()
    booking = Booking(1, instrument, user, '2026-09-15')
    booking.cancel()
    bookings = [booking]
    assert is_instrument_available(bookings, instrument, '2026-09-15') is True


def test_create_booking_success():
    bookings = []
    instrument = _make_room()
    user = _make_user()
    booking = create_booking(bookings, instrument, user, '2026-09-15')
    assert booking is not None
    assert len(bookings) == 1
    assert booking.instrument is instrument


def test_create_booking_conflict():
    instrument = _make_room()
    user = _make_user()
    bookings = [Booking(1, instrument, user, '2026-09-15')]
    result = create_booking(bookings, instrument, user, '2026-09-15')
    assert result is None
    assert len(bookings) == 1


def test_cancel_booking():
    instrument = _make_room()
    user = _make_user()
    bookings = [Booking(1, instrument, user, '2026-09-15')]
    assert cancel_booking(bookings, 1) is True
    assert bookings[0].is_cancelled is True


def test_cancel_booking_not_found():
    bookings = []
    assert cancel_booking(bookings, 99) is False


def test_get_booking_status_available():
    status = get_booking_status([], _make_room(), '2026-09-15')
    assert 'свободен' in status


def test_get_booking_status_busy():
    instrument = _make_room()
    user = _make_user()
    bookings = [Booking(1, instrument, user, '2026-09-15')]
    status = get_booking_status(bookings, instrument, '2026-09-15')
    assert 'занят' in status
