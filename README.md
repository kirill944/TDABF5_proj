# Instrument Booking — система бронирования музыкальных инструментов

## Назначение
Консольное приложение для управления музыкальными инструментами,
пользователями и их бронированием.

## Основные сущности

### Instrument
Атрибуты: `id`, `name`, `price`.
Методы: `__str__()`, `from_data()`, `to_dict()`.

### User
Атрибуты: `id`, `name`, `email`.
Методы: `__str__()`, `from_data()`, `to_dict()`.

### Booking
Атрибуты: `id`, `instrument` (объект Instrument), `user` (объект User),
`booking_date`, `is_cancelled`.
Методы: `cancel()`, `__str__()`.

## Взаимодействие объектов
`Booking` хранит ссылки на объекты `Instrument` и `User` — это позволяет
обращаться к данным через `booking.instrument.name` и `booking.user.email`.

## Хранение данных
JSON-файлы в `data/`. При загрузке JSON → объекты, при сохранении
объекты → JSON. В `bookings.json` связи хранятся как `instrument_id` и `user_id`.

## Запуск
```bash
python main.py
```

## Тесты
```bash
pytest -v
```

## Проверка качества кода
```bash
flake8 --exclude .venv
```
