from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from instruments.models import Instrument

from .forms import BookingFilterForm, BookingForm
from .models import Booking, User


def bookings(request):
    # Передаём GET-параметры в форму: Django проверяет их и сохраняет
    # введённые значения при повторном отображении страницы.
    form = BookingFilterForm(request.GET or None)
    form_valid = form.is_bound and form.is_valid()

    # Значения фильтров по умолчанию. Если форма не прошла проверку,
    # фильтрация по параметрам не выполняется.
    booking_date = None
    instrument_id = None
    user_id = None
    sort = "date"

    if form_valid:
        booking_date = form.cleaned_data.get("date")
        selected_instrument = form.cleaned_data.get("instrument")
        selected_user = form.cleaned_data.get("user")
        instrument_id = selected_instrument.pk if selected_instrument else None
        user_id = selected_user.pk if selected_user else None
        sort = form.cleaned_data.get("sort") or "date"

    error = None
    if form.is_bound and not form_valid:
        error = "Проверьте введённые значения фильтров."

    # Исходная выборка формируется пользовательским QuerySet:
    # в список попадают только активные бронирования.
    bookings_data = Booking.objects.active().select_related("instrument", "user")

    if booking_date:
        bookings_data = bookings_data.filter(booking_date=booking_date)
    if instrument_id:
        bookings_data = bookings_data.filter(instrument_id=instrument_id)
    if user_id:
        bookings_data = bookings_data.filter(user_id=user_id)

    # Словарь разрешённых полей сортировки: произвольный GET-параметр
    # в order_by() не подставляется.
    sort_fields = {
        "date": "booking_date",
        "instrument": "instrument__name",
        "user": "user__name",
    }
    sort_field = sort_fields.get(sort, "booking_date")
    bookings_data = bookings_data.order_by(sort_field, "id")

    # Пагинация.
    paginator = Paginator(bookings_data, per_page=10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "bookings": page_obj,
        "page_obj": page_obj,
        "form": form,
        "booking_date": booking_date,
        "selected_instrument": instrument_id,
        "selected_user": user_id,
        "instruments": Instrument.objects.order_by("name"),
        "users": User.objects.order_by("name"),
        "sort": sort,
        "error": error,
    }

    return render(request, "bookings/booking_list.html", context)


def booking_create(request):
    """Создание нового бронирования через ModelForm."""
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            instrument = form.cleaned_data["instrument"]
            booking_date = form.cleaned_data["booking_date"]

            # Проверяем, не занят ли инструмент на выбранную дату.
            # Отменённые бронирования не блокируют инструмент, потому что
            # не входят в Booking.objects.active().
            is_booked = (
                Booking.objects.active()
                .filter(instrument=instrument, booking_date=booking_date)
                .exists()
            )

            if is_booked:
                form.add_error(
                    None,
                    "Выбранный инструмент уже забронирован на эту дату.",
                )
            else:
                form.save()
                return redirect("bookings:bookings")
    else:
        # При GET-запросе показываем пустую форму с текущей датой.
        form = BookingForm(initial={"booking_date": timezone.localdate()})

    return render(request, "bookings/booking_form.html", {"form": form})


def booking_update(request, booking_id):
    """Редактирование существующего бронирования."""
    # Отменённые бронирования изменить нельзя — они не попадают в выборку.
    booking = get_object_or_404(Booking.objects.active(), pk=booking_id)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            instrument = form.cleaned_data["instrument"]
            booking_date = form.cleaned_data["booking_date"]

            # Текущее бронирование исключается из проверки занятости,
            # иначе оно конфликтовало бы само с собой.
            is_booked = (
                Booking.objects.active()
                .filter(instrument=instrument, booking_date=booking_date)
                .exclude(pk=booking.pk)
                .exists()
            )

            if is_booked:
                form.add_error(
                    None,
                    "Выбранный инструмент уже забронирован на эту дату.",
                )
            else:
                form.save()
                return redirect("bookings:bookings")
    else:
        form = BookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {
            "form": form,
            "booking": booking,
        },
    )


@require_POST
def booking_cancel(request, booking_id):
    """Отмена бронирования с изменением статуса записи."""
    # Ищем только активное бронирование: повторная отмена вернёт 404.
    booking = get_object_or_404(Booking.objects.active(), pk=booking_id)
    booking.cancel()
    return redirect("bookings:bookings")


def statistics(request):
    stats = (
        Booking.objects
        .values("instrument__name")
        .annotate(bookings_count=Count("id", filter=Q(is_cancelled=False)))
        .order_by("-bookings_count")
    )

    statistics_list = [
        {"instrument_name": row["instrument__name"],
         "bookings_count": row["bookings_count"]}
        for row in stats
    ]

    totals = Booking.objects.aggregate(
        total_bookings=Count("id"),
        active_bookings=Count("id", filter=Q(is_cancelled=False)),
        avg_instrument_price=Avg("instrument__price"),
        total_revenue=Sum("instrument__price", filter=Q(is_cancelled=False)),
        first_booking=Min("booking_date"),
        last_booking=Max("booking_date"),
    )

    active_future = Booking.objects.filter(
        is_cancelled=False,
        booking_date__gte="2026-01-01",
    ).count()

    return render(
        request,
        "bookings/statistics.html",
        {
            "statistics": statistics_list,
            "totals": totals,
            "active_future": active_future,
        },
    )


def booking_detail(request, booking_id):
    booking = (
        Booking.objects
        .select_related("instrument", "user")
        .filter(id=booking_id)
        .first()
    )

    if booking is None:
        return render(
            request,
            "bookings/booking_detail.html",
            {"booking": None},
            status=404,
        )

    return render(
        request,
        "bookings/booking_detail.html",
        {"booking": booking},
    )
