from django.test import TestCase
from django.urls import reverse

from instruments.models import Instrument


class SearchTests(TestCase):
    def setUp(self):
        Instrument.objects.create(name="Гитара", price=1000)
        Instrument.objects.create(name="Пианино", price=5000)

    def test_search_by_name(self):
        resp = self.client.get(reverse("instruments:instruments"), {"q": "Гитар"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["instruments"]), 1)
        self.assertEqual(resp.context["instruments"][0].name, "Гитара")

    def test_max_price(self):
        resp = self.client.get(
            reverse("instruments:instruments"), {"max_price": "2000"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["instruments"]), 1)
        self.assertEqual(resp.context["instruments"][0].name, "Гитара")

    def test_max_price_non_digit_ignored(self):
        resp = self.client.get(
            reverse("instruments:instruments"), {"max_price": "abc"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["instruments"]), 2)

    def test_instrument_detail_404(self):
        resp = self.client.get(
            reverse("instruments:instrument_detail", args=[999])
        )
        self.assertEqual(resp.status_code, 404)