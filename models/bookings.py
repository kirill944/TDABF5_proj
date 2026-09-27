from typing import List, Optional

from .instruments import Instrument
from .users import User


class Booking:
    """Бронирование инструмента пользователем."""

    def __init__(
            self,
            booking_id: int,
            instrument: Instrument,
            user: User,
            booking_date: str,
            is_cancelled: bool = False,
    ) -> None:
        """Создать объект бронирования."""
        self.id = booking_id
        self.instrument = instrument
        self.user = user
        self.booking_date = booking_date
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        """Отменить бронирование."""
        self.is_cancelled = True

    def __str__(self) -> str:
        """Строковое представление бронирования."""
        status = 'отменено' if self.is_cancelled else 'активно'
        return (
            f"[{self.id}] {self.instrument.name} для {self.user.name} "
            f"на {self.booking_date} — {status}"
        )


def is_instrument_available(
        bookings: List[Booking],
        instrument: Instrument,
        booking_date: str,
) -> bool:
    """Проверить доступность инструмента на дату."""
    for booking in bookings:
        if (
                booking.instrument.id == instrument.id
                and booking.booking_date == booking_date
                and not booking.is_cancelled
        ):
            return False
    return True


def create_booking(
        bookings: List[Booking],
        instrument: Instrument,
        user: User,
        booking_date: str,
) -> Optional[Booking]:
    """Создать бронирование, если инструмент свободен."""
    if not is_instrument_available(bookings, instrument, booking_date):
        return None

    booking_id = _generate_booking_id(bookings)
    booking = Booking(booking_id, instrument, user, booking_date)
    bookings.append(booking)
    return booking


def cancel_booking(
        bookings: List[Booking],
        booking_id: int,
) -> bool:
    """Отменить бронирование по идентификатору."""
    for booking in bookings:
        if booking.id == booking_id:
            booking.cancel()
            return True
    return False


def get_booking_status(
        bookings: List[Booking],
        instrument: Instrument,
        booking_date: str,
) -> str:
    """Вернуть текстовый статус доступности инструмента."""
    if is_instrument_available(bookings, instrument, booking_date):
        return f"Инструмент {instrument.name} свободен на {booking_date}"
    return f"Инструмент {instrument.name} занят на {booking_date}"


def show_bookings(bookings: List[Booking]) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print('Список бронирований пуст')
        return
    for booking in bookings:
        print(booking)


def _generate_booking_id(bookings: List[Booking]) -> int:
    """Сгенерировать уникальный идентификатор бронирования."""
    if not bookings:
        return 1
    return max(b.id for b in bookings) + 1
