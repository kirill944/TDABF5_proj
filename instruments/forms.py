from django import forms

from .models import Instrument


class InstrumentForm(forms.ModelForm):
    """Форма создания и редактирования инструмента с загрузкой изображения."""

    class Meta:
        model = Instrument
        fields = ["name", "price", "image"]
        labels = {
            "name": "Название",
            "price": "Цена, руб.",
            "image": "Изображение",
        }
        help_texts = {
            "image": "Необязательно. Поддерживаются форматы изображений.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }