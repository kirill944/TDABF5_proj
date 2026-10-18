from django.urls import path
from . import views

urlpatterns = [
    path("", views.instruments, name="instruments"),
    path("<int:instrument_id>/", views.instrument_detail,
         name="instrument_detail"),
]