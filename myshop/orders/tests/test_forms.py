from django.test import TestCase

import orders.forms


class TestOrderCreateForm(TestCase):
    def test_order_create_form_valid(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "mail@mail.ru",
            "address": "123 Main St",
            "city": "San Francisco",
            "postal_code": "12345",
        }
        form = orders.forms.OrderCreateForm(data)

        self.assertTrue(form.is_valid())

    def test_order_create_form_invalid(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "mailmailmailmail",
            "address": "123 Main St",
            "city": "San Francisco",
            "postal_code": "12345",
        }
        form = orders.forms.OrderCreateForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(
            form.errors["email"],
            ["Enter a valid email address."],
        )
