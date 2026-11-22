from django.shortcuts import get_object_or_404, redirect, render

from .forms import InstrumentForm
from .models import Instrument


def instruments(request):
    instruments_list = Instrument.objects.all()
    query = request.GET.get("q")
    if query:
        instruments_list = instruments_list.filter(name__icontains=query)

    max_price = request.GET.get("max_price")
    if max_price and max_price.isdigit():
        instruments_list = instruments_list.filter(price__lte=int(max_price))

    return render(
        request,
        "instruments/instrument_list.html",
        {
            "instruments": instruments_list,
            "query": query or "",
            "max_price": max_price or "",
        },
    )


def instrument_detail(request, instrument_id: int):
    # Ручная проверка вместо get_object_or_404
    instrument = Instrument.objects.filter(id=instrument_id).first()

    if instrument is None:
        # Кастомная страница «Инструмент не найден» со статусом 404
        return render(
            request,
            "instruments/instrument_detail.html",
            {"instrument": None, "is_available": False},
            status=404,
        )

    active_bookings = instrument.bookings.filter(is_cancelled=False)
    is_available = not active_bookings.exists()

    return render(
        request,
        "instruments/instrument_detail.html",
        {"instrument": instrument, "is_available": is_available},
    )


def available_instruments(request):
    booking_date = request.GET.get("date")
    instruments_list = Instrument.objects.none()

    if booking_date:
        instruments_list = (
            Instrument.objects
            .exclude(
                bookings__booking_date=booking_date,
                bookings__is_cancelled=False,
            )
            .order_by("name")
        )

    names_only = Instrument.objects.values("id", "name").order_by("name")

    return render(
        request,
        "instruments/available.html",
        {
            "instruments": instruments_list,
            "booking_date": booking_date,
            "names_only": names_only,
        },
    )


def instrument_create(request):
    """Создание инструмента с загрузкой изображения."""
    if request.method == "POST":
        # Передаём форме обычные данные и загруженные файлы.
        form = InstrumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("instruments:instruments")
    else:
        form = InstrumentForm()

    return render(request, "instruments/instrument_form.html", {"form": form})


def instrument_update(request, instrument_id):
    """Редактирование инструмента, в том числе замена изображения."""
    instrument = get_object_or_404(Instrument, pk=instrument_id)

    if request.method == "POST":
        form = InstrumentForm(request.POST, request.FILES, instance=instrument)
        if form.is_valid():
            form.save()
            return redirect("instruments:instruments")
    else:
        form = InstrumentForm(instance=instrument)

    return render(
        request,
        "instruments/instrument_form.html",
        {
            "form": form,
            "instrument": instrument,
        },
    )