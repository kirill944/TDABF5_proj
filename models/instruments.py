"""Класс Instrument и функции работы с коллекцией инструментов."""
from typing import List, Optional


class Instrument:
    """Музыкальный инструмент, доступный для бронирования."""

    def __init__(self, instrument_id: int, name: str, price: int) -> None:
        """Создать объект инструмента."""
        self.id = instrument_id
        self.name = name
        self.price = price

    @classmethod
    def from_data(cls, data: dict) -> "Instrument":
        """Создать объект Instrument из набора данных."""
        return cls(
            instrument_id=data['id'],
            name=data['name'],
            price=data['price'],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
        }

    def __str__(self) -> str:
        """Строковое представление инструмента."""
        return f"{self.name} — {self.price} руб."


def add_instrument(
        instruments: List[Instrument],
        instrument_id: int,
        name: str,
        price: int,
) -> Instrument:
    """Создать объект Instrument и добавить его в коллекцию."""
    instrument = Instrument(instrument_id, name, price)
    instruments.append(instrument)
    return instrument


def find_instrument(
        instruments: List[Instrument],
        name: str,
) -> List[Instrument]:
    """Найти инструменты по названию."""
    return [ins for ins in instruments if name.lower() in ins.name.lower()]


def find_instrument_by_id(
        instruments: List[Instrument],
        instrument_id: int,
) -> Optional[Instrument]:
    """Найти инструмент по идентификатору."""
    for instrument in instruments:
        if instrument.id == instrument_id:
            return instrument
    return None


def delete_instrument(
        instruments: List[Instrument],
        instrument_id: int,
) -> bool:
    """Удалить инструмент по идентификатору."""
    instrument = find_instrument_by_id(instruments, instrument_id)
    if instrument is None:
        return False
    instruments.remove(instrument)
    return True


def show_instruments(instruments: List[Instrument]) -> None:
    """Вывести список инструментов."""
    if not instruments:
        print('Список инструментов пуст')
        return
    for instrument in instruments:
        print(f"[{instrument.id}] {instrument}")
