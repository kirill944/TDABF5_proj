from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Avg, Sum, Min, Max
from django.core.paginator import Paginator
from .models import Booking


def bookings(request):
    # select_related — оптимизация запросов (JOIN)
    bookings_qs = (
        Booking.objects
        .select_related("instrument", "user")
        .filter(is_cancelled=False)                      # фильтрация по одному условию
        .order_by("booking_date")                        # сортировка по одному полю
    )

    # Пагинация
    paginator = Paginator(bookings_qs, per_page=10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "bookings/booking_list.html",
        {"bookings": page_obj, "page_obj": page_obj},
    )


def statistics(request):
    # annotate + Count — группировка (уже было)
    stats = (
        Booking.objects
        .values("instrument__name")
        .annotate(bookings_count=Count("id", filter=Q(is_cancelled=False)))
        .order_by("-bookings_count")                     # сортировка по вычисляемому полю
    )

    statistics_list = [
        {"instrument_name": row["instrument__name"],
         "bookings_count": row["bookings_count"]}
        for row in stats
    ]

    # aggregate — сводные показатели (расширено Min/Max)
    totals = Booking.objects.aggregate(
        total_bookings=Count("id"),
        active_bookings=Count("id", filter=Q(is_cancelled=False)),
        avg_instrument_price=Avg("instrument__price"),
        total_revenue=Sum("instrument__price", filter=Q(is_cancelled=False)),
        first_booking=Min("booking_date"),               # НОВОЕ: Min
        last_booking=Max("booking_date"),                # НОВОЕ: Max
    )

    # НОВОЕ: фильтрация по нескольким условиям в одном filter()
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