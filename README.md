# Instrument Booking

Веб-приложение на Django для бронирования музыкальных инструментов.
Проект переведён с ручных SQL-запросов (ПР7, `sqlite3`) на **Django ORM** (ПР9):
модели, миграции, связи `ForeignKey`, `select_related`, `annotate`/`aggregate`,
поиск, фильтрация, сортировка и пагинация.

---

## Стек

- Python 3.10+
- Django 5.2.19
- SQLite (через Django ORM)

---

## Модели и связи

| Модель | Поля | Связи |
|---|---|---|
| `Instrument` | `name` (CharField), `price` (IntegerField) | — |
| `User` | `name` (CharField), `email` (EmailField) | — |
| `Booking` | `booking_date` (DateField), `is_cancelled` (BooleanField) | `instrument` → `Instrument` (FK, `on_delete=CASCADE`, `related_name="bookings"`), `user` → `User` (FK, `on_delete=CASCADE`, `related_name="bookings"`) |

Связи реализованы через `ForeignKey` с `on_delete` и `related_name`.
Обратные связи: `instrument.bookings`, `user.bookings`.

---

## Запуск

### 1. Клонировать репозиторий и создать виртуальное окружение

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate.bat
# Linux / macOS
source .venv/bin/activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Применить миграции

```bash
python manage.py makemigrations instruments
python manage.py makemigrations bookings
python manage.py migrate
```

После этого создаётся `db.sqlite3` с таблицами:
`instruments_instrument`, `bookings_user`, `bookings_booking` и служебными таблицами Django.

### 4. (Опционально) Создать суперпользователя для админки

```bash
python manage.py createsuperuser
```

Админка: http://127.0.0.1:8000/admin/

### 5. Запустить сервер разработки

```bash
python manage.py runserver
```

Приложение доступно по адресу: http://127.0.0.1:8000/

---

## Страницы

| URL | Описание | ORM-приёмы |
|---|---|---|
| `/` | Главная | — |
| `/instruments/` | Список инструментов + поиск (`?q=`, `?max_price=`) | `all()`, `filter(name__icontains=...)`, `filter(price__lte=...)`, `values()` |
| `/instruments/<id>/` | Детали инструмента, признак доступности | `filter(id=...).first()`, `instrument.bookings.filter(is_cancelled=False)` |
| `/instruments/available/?date=YYYY-MM-DD` | Свободные инструменты на дату | `exclude(bookings__booking_date=..., bookings__is_cancelled=False)`, `order_by("name")` |
| `/bookings/` | Список активных бронирований + пагинация | `select_related("instrument", "user")`, `filter(is_cancelled=False)`, `order_by("booking_date")`, `Paginator` |
| `/bookings/statistics/` | Статистика по инструментам и сводные показатели | `values("instrument__name").annotate(Count(...))`, `aggregate(Count, Avg, Sum, Min, Max)`, `filter(is_cancelled=False, booking_date__gte=...)` |
| `/bookings/<id>/` | Детали бронирования | `select_related("instrument", "user")`, `filter(id=...).first()` |

Несуществующий инструмент/бронирование → кастомная страница «Не найдено» со статусом **404**.
Несуществующий URL → общий `404.html`.

---

## ORM-запросы (ПР9, таблица 1)

| Направление | Минимум | Реализовано |
|---|---|---|
| Базовое получение | 2 | `Instrument.objects.all()`, `Booking.objects.filter(id=...).first()` |
| Фильтрация | 4 | `filter(is_cancelled=False)`, `instrument.bookings.filter(is_cancelled=False)`, `exclude(bookings__...=..., bookings__...=...)`, `filter(is_cancelled=False, booking_date__gte=...)` |
| Поиск | 2 | `filter(name__icontains=query)`, `filter(price__lte=int(max_price))` |
| Сортировка | 2 | `order_by("booking_date")`, `order_by("-bookings_count")`, `ordering` в `Meta` |
| Работа со связями | 2 | `select_related("instrument", "user")`, обращение `booking.instrument.name` |
| Агрегирование | 2 | `annotate(bookings_count=Count(...))`, `aggregate(Count, Avg, Sum, Min, Max)` |
| Пагинация | 1 | `Paginator` + `get_page()` |
| **Итого** | **≥15** | **16 различных выражений** |

---

## Переход с ручного SQL на ORM (ПР9)

До ПР9 представления (`instruments/views.py`, `bookings/views.py`) работали через
`sqlite3.connect("data/instrument_booking.sqlite")` и ручные SQL-запросы с `JOIN`/`GROUP BY`.

После ПР9:

1. Описаны модели `Instrument`, `User`, `Booking` в `models.py`.
2. Созданы и применены миграции.
3. Данные из `data/instrument_booking.sqlite` перенесены в `db.sqlite3` (скрипт `legacy/import_to_orm.py`).
4. Представления переписаны на ORM: `all`, `filter`, `exclude`, `get/first`, `select_related`, `values`, `annotate`, `aggregate`, `Paginator`.
5. Шаблоны используют объекты моделей (`booking.instrument.name`, `booking.user.name`) вместо словарей из `sqlite3`.

Консольные артефакты ПР1–ПР7 сохранены в `legacy/` (не удалены — согласно требованию «не удалять ранее реализованные функции»).

---

## Переменные окружения и настройки

`instrument_booking/settings.py`:

- `DEBUG = True` — для разработки (статика отдаётся `runserver`).
- `DATABASES` → `BASE_DIR / "db.sqlite3"` — рабочая БД ORM.
- `INSTALLED_APPS` содержит `django.contrib.staticfiles`, `homepage`, `instruments`, `bookings`.
- `TEMPLATES["DIRS"]` содержит `BASE_DIR / "templates"`.
- `STATIC_URL = "static/"`.
