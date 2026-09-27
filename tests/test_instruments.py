"""Тесты для класса Instrument и функций работы с инструментами."""
from models import Instrument
from models.instruments import (
    add_instrument,
    delete_instrument,
    find_instrument,
    find_instrument_by_id,
)


def test_instrument_creation():
    instrument = Instrument(1, 'Скрипка', 30000)
    assert instrument.id == 1
    assert instrument.name == 'Скрипка'
    assert instrument.price == 30000


def test_instrument_str():
    instrument = Instrument(1, 'Скрипка', 30000)
    assert str(instrument) == 'Скрипка — 30000 руб.'


def test_instrument_from_data():
    data = {'id': 1, 'name': 'Скрипка', 'price': 30000}
    instrument = Instrument.from_data(data)
    assert instrument.id == 1
    assert instrument.name == 'Скрипка'
    assert instrument.price == 30000


def test_instrument_to_dict():
    instrument = Instrument(1, 'Скрипка', 30000)
    assert instrument.to_dict() == {'id': 1, 'name': 'Скрипка', 'price': 30000}


def test_add_instrument():
    instruments = [Instrument(1, 'Виолончель', 70000)]
    add_instrument(instruments, 2, 'Скрипка', 10000)
    assert len(instruments) == 2
    assert instruments[1].name == 'Скрипка'


def test_find_instrument():
    instruments = [Instrument(1, 'Виолончель', 70000)]
    results = find_instrument(instruments, 'Виолончель')
    assert len(results) == 1
    assert results[0].name == 'Виолончель'


def test_find_instrument_by_id():
    instruments = [Instrument(1, 'Виолончель', 70000)]
    assert find_instrument_by_id(instruments, 1).name == 'Виолончель'
    assert find_instrument_by_id(instruments, 99) is None


def test_delete_instrument():
    instruments = [Instrument(1, 'Виолончель', 70000)]
    assert delete_instrument(instruments, 1) is True
    assert len(instruments) == 0
    assert delete_instrument(instruments, 1) is False