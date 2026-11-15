"""Точка входа в приложение."""
from typing import List

from models import Booking, Instrument, User
from models.bookings import (
    cancel_booking,
    create_booking,
    get_booking_status,
    show_bookings,
)
from models.instruments import (
    add_instrument,
    find_instrument,
    find_instrument_by_id,
    show_instruments,
)
from models.users import (
    add_user,
    find_user,
    find_user_by_id,
    show_users,
)
from storage import (
    load_bookings,
    load_instruments,
    load_users,
    save_bookings,
    save_instruments,
    save_users,
)
from utils import input_date, input_int

INSTRUMENTS_FILE = 'data/instruments.json'
USERS_FILE = 'data/users.json'
BOOKINGS_FILE = 'data/bookings.json'


def create_new_booking(
        bookings: List[Booking],
        instruments: List[Instrument],
        users: List[User],
) -> None:
    """Создать новое бронирование через пользовательский сценарий."""
    instrument_id = input_int('Введите ID инструмента: ')
    instrument = find_instrument_by_id(instruments, instrument_id)
    if instrument is None:
        print('Инструмент не найден')
        return

    user_id = input_int('Введите ID пользователя: ')
    user = find_user_by_id(users, user_id)
    if user is None:
        print('Пользователь не найден')
        return

    booking_date = input_date('Введите дату (YYYY-MM-DD): ')

    booking = create_booking(bookings, instrument, user, booking_date)
    if booking is None:
        print(get_booking_status(bookings, instrument, booking_date))
        return
    print(f'Бронирование создано: {booking}')


def main() -> None:
    """Запустить приложение."""
    instruments = load_instruments(INSTRUMENTS_FILE)
    users = load_users(USERS_FILE)
    bookings = load_bookings(BOOKINGS_FILE, instruments, users)

    while True:
        print('\n1. Показать инструменты')
        print('2. Добавить инструмент')
        print('3. Найти инструмент')
        print('4. Показать пользователей')
        print('5. Добавить пользователя')
        print('6. Найти пользователя')
        print('7. Показать бронирования')
        print('8. Создать бронирование')
        print('9. Отменить бронирование')
        print('0. Выход')

        case = input('Выберите действие: ')

        if case == '0':
            break
        elif case == '1':
            show_instruments(instruments)
        elif case == '2':
            name = input('Введите название инструмента: ')
            price = input_int('Введите цену: ')
            new_id = max((i.id for i in instruments), default=0) + 1
            add_instrument(instruments, new_id, name, price)
        elif case == '3':
            query = input('Введите название для поиска: ')
            results = find_instrument(instruments, query)
            show_instruments(results)
        elif case == '4':
            show_users(users)
        elif case == '5':
            name = input('Введите имя пользователя: ')
            email = input('Введите email: ')
            new_id = max((u.id for u in users), default=0) + 1
            add_user(users, new_id, name, email)
        elif case == '6':
            query = input('Введите имя или email: ')
            results = find_user(users, query)
            show_users(results)
        elif case == '7':
            show_bookings(bookings)
        elif case == '8':
            create_new_booking(bookings, instruments, users)
        elif case == '9':
            booking_id = input_int('Введите ID бронирования: ')
            if cancel_booking(bookings, booking_id):
                print('Бронирование отменено')
            else:
                print('Бронирование не найдено')
        else:
            print('Неизвестная команда')

    save_instruments(INSTRUMENTS_FILE, instruments)
    save_users(USERS_FILE, users)
    save_bookings(BOOKINGS_FILE, bookings)
    print('Данные сохранены. До встречи!')


if __name__ == '__main__':
    main()
