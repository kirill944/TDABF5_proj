from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    # Список бронирований.
    path("", views.bookings, name="bookings"),
    # Статические маршруты располагаются до маршрутов с <int:booking_id>.
    path("create/", views.booking_create, name="booking_create"),
    path("statistics/", views.statistics, name="statistics"),
    # Редактирование и отмена бронирования.
    path("<int:booking_id>/edit/", views.booking_update, name="booking_update"),
    path("<int:booking_id>/cancel/", views.booking_cancel, name="booking_cancel"),
    # Просмотр отдельного бронирования.
    path("<int:booking_id>/", views.booking_detail, name="booking_detail"),
]
