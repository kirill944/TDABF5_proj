from django.urls import path
from . import views

app_name = "instruments"

urlpatterns = [
    path("", views.instruments, name="instruments"),
    path("available/", views.available_instruments, name="available"), # <-- Новый маршрут
    path("<int:instrument_id>/", views.instrument_detail, name="instrument_detail"),
]
