"""Загрузка и сохранение данных в JSON."""
import json
from typing import List

from models import Booking, Instrument, User
from models.instruments import find_instrument_by_id
from models.users import find_user_by_id


def load_instruments(filename: str) -> List[Instrument]:
    """Загрузить инструменты из JSON в объекты Instrument."""
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return [Instrument.from_data(item) for item in data]


def save_instruments(filename: str, instruments: List[Instrument]) -> None:
    """Сохранить объекты Instrument в JSON."""
    with open(filename, 'w', encoding='UTF-8') as file:
        json.dump(
            [instrument.to_dict() for instrument in instruments],
            file,
            ensure_ascii=False,
            indent=4,
        )


def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON в объекты User."""
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return [User.from_data(item) for item in data]


def save_users(filename: str, users: List[User]) -> None:
    """Сохранить объекты User в JSON."""
    with open(filename, 'w', encoding='UTF-8') as file:
        json.dump(
            [user.to_dict() for user in users],
            file,
            ensure_ascii=False,
            indent=4,
        )


def load_bookings(
        filename: str,
        instruments: List[Instrument],
        users: List[User],
) -> List[Booking]:
    """Загрузить бронирования, восстановив связи с объектами."""
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    bookings: List[Booking] = []
    for item in data:
        instrument = find_instrument_by_id(instruments, item['instrument_id'])
        user = find_user_by_id(users, item['user_id'])
        if instrument is None or user is None:
            continue
        bookings.append(
            Booking(
                booking_id=item['id'],
                instrument=instrument,
                user=user,
                booking_date=item['booking_date'],
                is_cancelled=item.get('is_cancelled', False),
            )
        )
    return bookings


def save_bookings(filename: str, bookings: List[Booking]) -> None:
    """Сохранить бронирования, заменив объекты на их id."""
    data = [
        {
            'id': booking.id,
            'instrument_id': booking.instrument.id,
            'user_id': booking.user.id,
            'booking_date': booking.booking_date,
            'is_cancelled': booking.is_cancelled,
        }
        for booking in bookings
    ]
    with open(filename, 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
