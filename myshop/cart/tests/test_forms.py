from django.test import TestCase


import cart.forms


class TestCartAddProductForm(TestCase):
    def test_cart_add_product_form_valid(self):
        form_data = {
            "quantity": 1,
        }
        form = cart.forms.CartAddProductForm(form_data)
        self.assertTrue(form.is_valid())

    def test_cart_add_product_form_invalid(self):
        form_data = {
            "quantity": 9999,
        }
        form = cart.forms.CartAddProductForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["quantity"],
            [
                f"Select a valid choice. {form_data['quantity']} "
                + "is not one of the available choices.",
            ],
        )
