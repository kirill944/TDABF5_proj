from random import randint


def create_booking(bookings: dict[int, str],
                   instrument_name: str) -> None:
    booking_id = randint(1, 10000)
    while booking_id in bookings:
        booking_id = randint(1, 10000)
    bookings[booking_id] = instrument_name
    print('Бронирование добавлено. Id:', booking_id)


def cancel_booking(bookings: dict[int, str],
                   booking_id: int) -> None:
    if booking_id in bookings:
        del bookings[booking_id]
        print('Бронирование успешно удалено')
    else:
        print('Бронирования не существует')


def is_instrument_available(bookings: dict[int, str],
                            instrument_name: str) -> bool:
    for booking in bookings:
        if bookings[booking] == instrument_name:
            return False
    return True
