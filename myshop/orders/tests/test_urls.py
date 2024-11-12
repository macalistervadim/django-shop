import http

import django.shortcuts
from django.test import TestCase


class TestOrderCreateUrls(TestCase):
    def test_order_create_urls_get_method(self):
        url = django.shortcuts.reverse("orders:order_create")
        request = self.client.get(url)

        self.assertEqual(request.status_code, http.HTTPStatus.OK)

    def test_order_create_urls_post_method(self):
        url = django.shortcuts.reverse("orders:order_create")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "mail@mail.ru",
            "address": "123 Main St",
            "city": "San Francisco",
            "postal_code": "12345",
        }
        request = self.client.post(url, data=data)

        self.assertEqual(request.status_code, http.HTTPStatus.FOUND)
