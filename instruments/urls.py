from django.urls import path
from . import views

app_name = "instruments"

urlpatterns = [
    path("", views.instruments, name="instruments"),
    path("<int:instrument_id>/", views.instrument_detail,
         name="instrument_detail"),
]