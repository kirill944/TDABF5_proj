from django.contrib import admin
from django.db.models import Count, Q

from .models import Booking, User


class BookingInline(admin.TabularInline):
    """Бронирования внутри карточки пользователя."""
    model = Booking
    fk_name = "user"
    extra = 0
    fields = ("instrument", "booking_date", "is_cancelled")
    autocomplete_fields = ("instrument",)
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "bookings_count")
    list_display_links = ("id", "name")
    search_fields = ("name", "email")
    ordering = ("name",)
    inlines = [BookingInline]

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


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "instrument",
        "user",
        "booking_date",
        "is_cancelled",
    )
    list_display_links = ("id",)
    list_filter = ("is_cancelled", "booking_date", "instrument")
    search_fields = ("instrument__name", "user__name", "user__email")
    list_select_related = ("instrument", "user")     # ← против N+1
    date_hierarchy = "booking_date"
    ordering = ("-booking_date",)
    autocomplete_fields = ("instrument", "user")
    list_per_page = 25