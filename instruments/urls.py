from django.urls import path
from . import views

app_name = "instruments"

urlpatterns = [
    path("", views.instruments, name="instruments"),
    path("available/", views.available_instruments, name="available"),  # Новый маршрут
    path("create/", views.instrument_create, name="instrument_create"),
    path("<int:instrument_id>/edit/", views.instrument_update, name="instrument_update"),
    path("<int:instrument_id>/", views.instrument_detail, name="instrument_detail"),
]
