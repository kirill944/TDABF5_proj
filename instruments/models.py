from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    class Meta:
        verbose_name = "Инструмент"
        verbose_name_plural = "Инструменты"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} — {self.price} руб."