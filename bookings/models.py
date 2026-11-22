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


class BookingQuerySet(models.QuerySet):
    """Пользовательский QuerySet бронирований.

    Инкапсулирует правило отбора активных записей, чтобы представления
    не повторяли это условие вручную.
    """

    def active(self):
        """Возвращает только активные (не отменённые) бронирования."""
        return self.filter(is_cancelled=False)


class BookingManager(models.Manager.from_queryset(BookingQuerySet)):
    """Менеджер модели Booking, доступный как Booking.objects."""


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

    objects = BookingManager()

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["booking_date"]

    def __str__(self):
        status = "отменено" if self.is_cancelled else "активно"
        return f"[{self.id}] {self.instrument.name} для {self.user.name} на {self.booking_date} — {status}"

    @property
    def status_label(self):
        """Человекочитаемое состояние бронирования."""
        return "Отменено" if self.is_cancelled else "Активно"

    def cancel(self):
        """Отменяет бронирование: запись остаётся в базе, меняется статус."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])
