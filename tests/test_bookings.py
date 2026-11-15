from datetime import date

from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking, User
from instruments.models import Instrument


class AvailabilityTests(TestCase):
    def setUp(self):
        self.ins = Instrument.objects.create(name="Гитара", price=1000)
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.today = date.today()

    def test_instrument_with_active_booking_is_not_available(self):
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=self.today,
            is_cancelled=False,
        )
        resp = self.client.get(
            reverse("instruments:available"),
            {"date": self.today.isoformat()},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.ins, resp.context["instruments"])

    def test_instrument_with_cancelled_booking_is_available(self):
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=self.today,
            is_cancelled=True,
        )
        resp = self.client.get(
            reverse("instruments:available"),
            {"date": self.today.isoformat()},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.ins, resp.context["instruments"])


class BookingDetailTests(TestCase):
    def test_404_for_missing_booking(self):
        resp = self.client.get(reverse("bookings:booking_detail", args=[999]))
        self.assertEqual(resp.status_code, 404)


class PaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.ins = Instrument.objects.create(name="Гитара", price=1000)

    def test_pagination_preserves_filters(self):
        # 15 активных броней → 2 страницы по 10
        for i in range(15):
            Booking.objects.create(
                instrument=self.ins,
                user=self.user,
                booking_date=date(2026, 1, 1 + i % 28),
                is_cancelled=False,
            )
        resp = self.client.get(
            reverse("bookings:bookings"),
            {"instrument": self.ins.id, "page": 1},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["page_obj"].has_next())

    def test_pagination_keeps_get_params_in_links(self):
        for i in range(15):
            Booking.objects.create(
                instrument=self.ins,
                user=self.user,
                booking_date=date(2026, 1, 1 + i % 28),
                is_cancelled=False,
            )
        resp = self.client.get(
            reverse("bookings:bookings"),
            {"instrument": self.ins.id, "page": 1},
        )
        html = resp.content.decode()
        # ссылка «Вперёд» должна содержать instrument=...
        self.assertIn(f"instrument={self.ins.id}", html)
        self.assertIn("page=2", html)