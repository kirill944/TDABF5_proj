# Instrument Booking

Веб-приложение на Django для бронирования музыкальных инструментов.
Проект переведён с ручных SQL-запросов (ПР7, `sqlite3`) на **Django ORM** (ПР9).
В ПР10 настроена **административная панель**, добавлена расширенная фильтрация, внедрена оптимизация запросов (устранена проблема N+1) и написаны автоматизированные тесты.

---

## Стек

- Python 3.10+
- Django 5.2.19
- SQLite (через Django ORM)
- django-debug-toolbar (для анализа SQL-запросов)

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

### 4. Создать суперпользователя для админки

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
| `/instruments/` | Список инструментов + поиск (`?q=`, `?max_price=`) | `all()`, `filter(name__icontains=...)`, `filter(price__lte=...)` |
| `/instruments/<id>/` | Детали инструмента, признак доступности | `filter(id=...).first()`, `instrument.bookings.filter(is_cancelled=False)` |
| `/instruments/available/?date=YYYY-MM-DD` | Свободные инструменты на дату | `exclude(bookings__booking_date=..., bookings__is_cancelled=False)` |
| `/bookings/` | Список активных бронирований + фильтры + пагинация | `select_related()`, `filter(is_cancelled=False)`, `Q()`, `Paginator` |
| `/bookings/create/` | Создание бронирования (`BookingForm`, `ModelForm`) | `objects.active()`, `filter()`, `exists()`, `form.save()` |
| `/bookings/<id>/edit/` | Редактирование бронирования | `get_object_or_404()`, `objects.active()`, `exclude(pk=...)` |
| `/bookings/<id>/cancel/` | Отмена бронирования (только POST) | `get_object_or_404()`, `Booking.cancel()` |
| `/bookings/statistics/` | Статистика | `values().annotate(Count)`, `aggregate()` |
| `/bookings/<id>/` | Детали бронирования | `select_related()`, `filter(id=...).first()` |
| `/instruments/create/` | Создание инструмента с изображением | `ImageField`, `request.FILES` |
| `/instruments/<id>/edit/` | Редактирование инструмента и замена изображения | `ModelForm(instance=...)`, `request.FILES` |

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

## Административная панель и ORM (ПР10)

### Django Admin
В ПР10 была проведена полная настройка административной панели:
- **Локализация:** Установлен `LANGUAGE_CODE = 'ru-ru'`, заданы `verbose_name` для приложений (`apps.py`), моделей и полей. В админке всё отображается на русском языке.
- **Списки объектов:** Для `Instrument` и `User` настроены кастомные методы, выводящие количество активных броней. Для `Booking` настроен `list_display`, `date_hierarchy` и фильтры по статусу, дате и инструменту.
- **Связанные объекты (Inline):** В карточках Пользователей и Инструментов добавлены встроенные формы (`TabularInline`), позволяющие просматривать и редактировать их бронирования напрямую.
- **Поиск и автодополнение:** Для бронирований настроен `autocomplete_fields` для быстрого выбора инструмента и пользователя.

### Работа с Django ORM и фильтрация
- **Фильтрация по нескольким условиям:** В списке бронирований (`/bookings/`) реализована фильтрация по пользователю, инструменту и точной дате. Для формирования комплексных условий используется объект `Q()`.
- **Сохранение фильтров при пагинации:** В шаблоне `booking_list.html` реализован сбор GET-параметров, благодаря чему при переходе по страницам (`?page=2`) выбранные фильтры не сбрасываются.
- **Доступность инструментов:** При проверке доступности на конкретную дату учитываются только активные бронирования (`is_cancelled=False`). Отмененные брони не блокируют инструмент.

### Оптимизация запросов (Решение проблемы N+1)
В ПР10 проведен анализ SQL-запросов с помощью **Django Debug Toolbar**. 
Для устранения проблемы N+1 (когда для каждой записи списка выполняется отдельный запрос к связанной таблице) были применены:
- `select_related("instrument", "user")` в представлениях.
- `list_select_related = ("instrument", "user")` в `BookingAdmin`.
Теперь при выводе списка бронирований Django выполняет один SQL-запрос с `INNER JOIN`, а не N+1 запросов.


## Формы Django (ПР11)

В ПР11 фильтрация, создание и редактирование бронирований переведены на Django Forms.

### Формы приложения `bookings` (`bookings/forms.py`)

| Класс | Базовый класс | Назначение |
|---|---|---|
| `BookingFilterForm` | `forms.Form` | Фильтрация списка бронирований по дате, инструменту и пользователю + сортировка |
| `BookingForm` | `forms.ModelForm` | Создание и редактирование бронирования на основе модели `Booking` |

**`BookingFilterForm`** объявляет поля `date` (`DateField` с виджетом `DateInput(type="date")`),
`instrument` и `user` (`ModelChoiceField` с `queryset` и `empty_label`), `sort` (`ChoiceField`
с тремя допустимыми значениями). Имена полей совпадают с именами GET-параметров, поэтому
`page` остаётся вне формы — номер страницы относится к пагинации.

**`BookingForm`** включает только поля `instrument`, `booking_date` и `user`. Служебное поле
`is_cancelled` в форму не попадает: статус новой записи определяется моделью
(`default=False`), а меняется только операцией отмены. Для полей настроены `labels`,
`help_texts` и `widgets` (Bootstrap-классы, `type="date"` для даты).

### Валидация

| Способ | Где реализован | Что проверяет |
|---|---|---|
| Встроенная валидация полей | `BookingFilterForm`, `BookingForm` | Тип даты, существование выбранного объекта в `QuerySet`, допустимость значения сортировки, обязательность полей |
| `clean_booking_date()` | `BookingForm` | Запрет бронирования на прошедшую дату (`timezone.localdate()`) |
| Проверка занятости | `booking_create()`, `booking_update()` | Отсутствие активного бронирования того же инструмента на ту же дату |

Некорректные GET-параметры не приводят к исключению: при неуспешной валидации формы
фильтрация по непроверенным значениям не выполняется, а пользователь видит общее сообщение
и ошибки конкретных полей.

### Обработка GET- и POST-запросов

| Представление | GET | POST |
|---|---|---|
| `bookings()` | Связанная с `request.GET` форма, фильтрация через `cleaned_data` | — |
| `booking_create()` | Пустая форма с текущей датой в `initial` | `BookingForm(request.POST)` → проверка занятости → `form.save()` → `redirect` |
| `booking_update()` | `BookingForm(instance=booking)` с текущими значениями | `BookingForm(request.POST, instance=booking)` → `exclude(pk=booking.pk)` → `form.save()` |
| `booking_cancel()` | 405 (`@require_POST`) | `booking.cancel()` → `redirect` |

При ошибке форма отображается повторно с введёнными значениями, ошибками полей
(`field.errors`) и общими ошибками формы (`form.non_field_errors`).

### Правила предметной области

- Активные бронирования выбираются через пользовательский `Booking.objects.active()`
  (`BookingQuerySet.active()`), а не через `Booking.objects.all()`.
- Отменённое бронирование не блокирует инструмент, поскольку не входит в `active()`.
- При редактировании текущая запись исключается из проверки занятости
  (`.exclude(pk=booking.pk)`), иначе она конфликтовала бы сама с собой.
- Отмена не удаляет запись: `Booking.cancel()` выставляет `is_cancelled=True`.
- `booking_update()` и `booking_cancel()` ищут объект через `Booking.objects.active()`,
  поэтому отменённое бронирование нельзя изменить или отменить повторно (404).

### Защита POST-запросов

Все изменяющие операции выполняются методом POST и защищены `{% csrf_token %}`:
создание и редактирование бронирования (`booking_form.html`), отмена бронирования
(кнопка в `booking_list.html`), создание и редактирование инструмента
(`instrument_form.html`). Адрес отмены, открытый GET-запросом, возвращает 405.

### Загрузка изображений

- В модель `Instrument` добавлено поле `image = ImageField(upload_to="instruments/")`
  (`blank=True`, `null=True`), миграция `instruments/0002_instrument_image.py`.
- В `settings.py` заданы `MEDIA_URL = "/media/"` и `MEDIA_ROOT = BASE_DIR / "media"`;
  в корневом `urls.py` при `DEBUG` подключена раздача медиафайлов через `static()`.
- Форма `InstrumentForm` (`instruments/forms.py`) включает поле `image`;
  представления передают `request.FILES`, шаблон использует
  `enctype="multipart/form-data"`.
- Изображение выводится на странице инструмента и в карточке списка; при отсутствии
  файла показывается сообщение «Изображение не загружено».
- Загружать и заменять изображение можно также из административной панели Django.

### Тестирование

В корне проекта создана папка `tests/` (тесты отделены от приложений). Написаны тесты для проверки бизнес-логики (доступность, поиск, 404) и пагинации.

Запуск тестов:
```bash
python manage.py test tests
```
