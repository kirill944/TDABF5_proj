from bookings import create_booking, is_instrument_available


def test_is_instrument_available1():
    bookings = {1: 'Скрипка'}
    assert is_instrument_available(bookings, 'Скрипка') is False


def test_is_instrument_available2():
    bookings = {1: 'Гитара'}
    assert is_instrument_available(bookings, 'Скрипка') is True


def test_create_booking():
    bookings = {1: 'Гитара'}
    create_booking(bookings, 'Скрипка')
    assert len(bookings) == 2
