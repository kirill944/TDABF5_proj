from django.db import models
from instruments.models import Instrument


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Инструмент",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    booking_date = models.DateField(verbose_name="Дата бронирования")
    is_cancelled = models.BooleanField(default=False, verbose_name="Отменено")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["booking_date"]

    def __str__(self):
        status = "отменено" if self.is_cancelled else "активно"
        return f"[{self.id}] {self.instrument.name} для {self.user.name} на {self.booking_date} — {status}"