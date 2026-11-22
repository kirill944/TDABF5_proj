from django import forms
from django.utils import timezone

from instruments.models import Instrument

from .models import Booking, User


class BookingFilterForm(forms.Form):
    """Форма фильтрации списка бронирований.

    Данные приходят из GET-запроса, поэтому имена полей совпадают
    с именами существующих GET-параметров.
    """

    date = forms.DateField(
        required=False,
        label="Дата бронирования",
        widget=forms.DateInput(
            # format задаёт ISO-представление, обязательное для input type="date".
            format="%Y-%m-%d",
            attrs={"type": "date", "class": "form-control"},
        ),
    )
    instrument = forms.ModelChoiceField(
        queryset=Instrument.objects.order_by("name"),
        required=False,
        label="Инструмент",
        empty_label="Все инструменты",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("name"),
        required=False,
        label="Пользователь",
        empty_label="Все пользователи",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=[
            ("date", "По дате"),
            ("instrument", "По инструменту"),
            ("user", "По пользователю"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class BookingForm(forms.ModelForm):
    """Форма создания и редактирования бронирования на основе модели Booking."""

    class Meta:
        model = Booking
        fields = [
            "instrument",
            "booking_date",
            "user",
        ]
        labels = {
            "instrument": "Инструмент",
            "booking_date": "Дата бронирования",
            "user": "Пользователь",
        }
        help_texts = {
            "instrument": "Выберите инструмент, который нужно забронировать.",
            "booking_date": "Укажите дату бронирования — сегодня или позже.",
            "user": "Выберите пользователя, для которого создаётся бронирование.",
        }
        widgets = {
            "instrument": forms.Select(attrs={"class": "form-select"}),
            "booking_date": forms.DateInput(
                # format задаёт ISO-представление, обязательное для input type="date".
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "user": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_booking_date(self):
        """Запрещает бронирование на прошедшую дату."""
        booking_date = self.cleaned_data["booking_date"]
        if booking_date < timezone.localdate():
            raise forms.ValidationError(
                "Нельзя создать бронирование на прошедшую дату."
            )
        return booking_date
