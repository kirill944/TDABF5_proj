from django.contrib import admin
from django.db.models import Count, Q

from bookings.admin import BookingInline

from .models import Instrument


class InstrumentBookingInline(BookingInline):
    """Бронирования внутри карточки инструмента (FK — instrument)."""
    fk_name = "instrument"


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "bookings_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    list_filter = ("price",)
    ordering = ("name",)
    inlines = [InstrumentBookingInline]
    # Поле изображения доступно для загрузки и замены из админ-панели.
    fields = ("name", "price", "image")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _bookings_count=Count(
                    "bookings", filter=Q(bookings__is_cancelled=False)
                )
            )
        )

    @admin.display(description="Активных броней", ordering="_bookings_count")
    def bookings_count(self, obj):
        return obj._bookings_count