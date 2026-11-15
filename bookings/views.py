from django.shortcuts import render
from django.db.models import Count, Q, Avg, Sum, Min, Max
from django.core.paginator import Paginator

from .models import Booking, User
from instruments.models import Instrument


def bookings(request):
    bookings_qs = Booking.objects.select_related("instrument", "user").filter(is_cancelled=False)

    # Собираем условия в объект Q
    query = Q()

    instrument_id = request.GET.get("instrument")
    if instrument_id and instrument_id.isdigit():
        query &= Q(instrument_id=int(instrument_id))

    user_id = request.GET.get("user")
    if user_id and user_id.isdigit():
        query &= Q(user_id=int(user_id))

    booking_date = request.GET.get("date")
    if booking_date:
        query &= Q(booking_date=booking_date)

    # Применяем все собранные условия за один раз
    if query:
        bookings_qs = bookings_qs.filter(query)

    # Сортировка
    bookings_qs = bookings_qs.order_by("booking_date")

    # Пагинация
    paginator = Paginator(bookings_qs, per_page=10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "bookings/booking_list.html",
        {
            "bookings": page_obj,
            "page_obj": page_obj,
            "instruments": Instrument.objects.order_by("name"),
            "users": User.objects.order_by("name"),
            "selected_instrument": instrument_id or "",
            "selected_user": user_id or "",
            "selected_date": booking_date or "",  # <-- изменили название переменной
        },
    )


def statistics(request):
    # ... без изменений, как у вас было ...
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