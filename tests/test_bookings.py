from datetime import date, timedelta

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


class BookingFilterFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.ins = Instrument.objects.create(name="Гитара", price=1000)
        self.other = Instrument.objects.create(name="Пианино", price=5000)
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=date(2026, 5, 10),
        )
        Booking.objects.create(
            instrument=self.other,
            user=self.user,
            booking_date=date(2026, 5, 11),
        )

    def test_empty_form_shows_all_active_bookings(self):
        resp = self.client.get(reverse("bookings:bookings"))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["form"].is_bound)
        self.assertEqual(len(resp.context["bookings"]), 2)

    def test_filter_by_instrument(self):
        resp = self.client.get(
            reverse("bookings:bookings"), {"instrument": self.ins.id}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["bookings"]), 1)

    def test_invalid_date_is_reported_without_crash(self):
        resp = self.client.get(reverse("bookings:bookings"), {"date": "не_дата"})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.context["error"])
        # Фильтрация по непроверенному значению не применяется.
        self.assertEqual(len(resp.context["bookings"]), 2)

    def test_unknown_instrument_is_rejected(self):
        resp = self.client.get(reverse("bookings:bookings"), {"instrument": 999999})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.context["error"])
        self.assertEqual(len(resp.context["bookings"]), 2)

    def test_unknown_sort_value_falls_back_to_date(self):
        resp = self.client.get(reverse("bookings:bookings"), {"sort": "unknown"})
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.context["error"])
        self.assertEqual(resp.context["sort"], "date")

    def test_cancelled_bookings_are_not_listed(self):
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=date(2026, 5, 12),
            is_cancelled=True,
        )
        resp = self.client.get(reverse("bookings:bookings"))
        self.assertEqual(len(resp.context["bookings"]), 2)


class BookingCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.ins = Instrument.objects.create(name="Гитара", price=1000)
        self.free_date = date.today() + timedelta(days=3)

    def test_get_returns_empty_form(self):
        resp = self.client.get(reverse("bookings:booking_create"))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["form"].is_bound)

    def test_valid_data_creates_booking(self):
        resp = self.client.post(
            reverse("bookings:booking_create"),
            {
                "instrument": self.ins.id,
                "booking_date": self.free_date.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertRedirects(resp, reverse("bookings:bookings"))
        self.assertEqual(Booking.objects.count(), 1)
        self.assertFalse(Booking.objects.first().is_cancelled)

    def test_past_date_is_rejected(self):
        past = date.today() - timedelta(days=1)
        resp = self.client.post(
            reverse("bookings:booking_create"),
            {
                "instrument": self.ins.id,
                "booking_date": past.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("booking_date", resp.context["form"].errors)
        self.assertEqual(Booking.objects.count(), 0)

    def test_busy_instrument_is_rejected(self):
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=self.free_date,
        )
        resp = self.client.post(
            reverse("bookings:booking_create"),
            {
                "instrument": self.ins.id,
                "booking_date": self.free_date.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["form"].non_field_errors())
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancelled_booking_does_not_block_instrument(self):
        Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=self.free_date,
            is_cancelled=True,
        )
        resp = self.client.post(
            reverse("bookings:booking_create"),
            {
                "instrument": self.ins.id,
                "booking_date": self.free_date.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertRedirects(resp, reverse("bookings:bookings"))
        self.assertEqual(Booking.objects.count(), 2)


class BookingUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.ins = Instrument.objects.create(name="Гитара", price=1000)
        self.other = Instrument.objects.create(name="Пианино", price=5000)
        self.free_date = date.today() + timedelta(days=3)
        self.booking = Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=self.free_date,
        )

    def test_form_is_prefilled_with_current_values(self):
        resp = self.client.get(
            reverse("bookings:booking_update", args=[self.booking.pk])
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context["form"].initial["instrument"], self.ins.pk
        )

    def test_saving_without_changes_does_not_conflict_with_itself(self):
        resp = self.client.post(
            reverse("bookings:booking_update", args=[self.booking.pk]),
            {
                "instrument": self.ins.id,
                "booking_date": self.free_date.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertRedirects(resp, reverse("bookings:bookings"))
        # Новая запись не создаётся — обновляется существующая.
        self.assertEqual(Booking.objects.count(), 1)

    def test_conflict_with_another_booking_is_rejected(self):
        Booking.objects.create(
            instrument=self.other,
            user=self.user,
            booking_date=self.free_date,
        )
        resp = self.client.post(
            reverse("bookings:booking_update", args=[self.booking.pk]),
            {
                "instrument": self.other.id,
                "booking_date": self.free_date.isoformat(),
                "user": self.user.id,
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["form"].non_field_errors())

    def test_404_for_missing_booking(self):
        resp = self.client.get(reverse("bookings:booking_update", args=[999]))
        self.assertEqual(resp.status_code, 404)


class BookingCancelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Иван", email="i@example.com")
        self.ins = Instrument.objects.create(name="Гитара", price=1000)
        self.booking = Booking.objects.create(
            instrument=self.ins,
            user=self.user,
            booking_date=date.today() + timedelta(days=2),
        )

    def test_cancel_changes_status_and_keeps_record(self):
        resp = self.client.post(
            reverse("bookings:booking_cancel", args=[self.booking.pk])
        )
        self.assertRedirects(resp, reverse("bookings:bookings"))
        self.booking.refresh_from_db()
        self.assertTrue(self.booking.is_cancelled)
        # Запись не удаляется.
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancelled_booking_is_not_listed_and_not_blocking(self):
        self.client.post(reverse("bookings:booking_cancel", args=[self.booking.pk]))
        resp = self.client.get(reverse("bookings:bookings"))
        self.assertEqual(len(resp.context["bookings"]), 0)

        self.assertFalse(
            Booking.objects.active()
            .filter(instrument=self.ins, booking_date=self.booking.booking_date)
            .exists()
        )

    def test_get_request_is_not_allowed(self):
        resp = self.client.get(
            reverse("bookings:booking_cancel", args=[self.booking.pk])
        )
        self.assertEqual(resp.status_code, 405)
        self.booking.refresh_from_db()
        self.assertFalse(self.booking.is_cancelled)

    def test_repeated_cancel_returns_404(self):
        self.client.post(reverse("bookings:booking_cancel", args=[self.booking.pk]))
        resp = self.client.post(
            reverse("bookings:booking_cancel", args=[self.booking.pk])
        )
        self.assertEqual(resp.status_code, 404)
