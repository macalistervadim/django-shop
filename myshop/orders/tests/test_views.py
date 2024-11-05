from http import HTTPStatus

import django.shortcuts
from django.test import TestCase

from cart.cart import Cart
from orders.models import Order, OrderItem
from shop.models import Category, Product


class TestOrderCreateView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=100,
        )

    def add_to_cart(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        self.client.post(
            url,
            {"product_id": self.product.id, "quantity": 2, "override": False},
        )

    def test_order_create_view_get_method(self):
        url = django.shortcuts.reverse("orders:order_create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "orders/order/create.html")

    def test_order_create_view_post_method(self):
        self.add_to_cart()

        url = django.shortcuts.reverse("orders:order_create")
        post_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "address": "123 Test St",
            "postal_code": "12345",
            "city": "Test City",
        }
        response = self.client.post(url, data=post_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "orders/order/created.html")

        order = Order.objects.get(email="johndoe@example.com")
        self.assertEqual(order.first_name, "John")
        self.assertEqual(order.last_name, "Doe")

        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, self.product.price)
        self.assertEqual(order_item.quantity, 2)

        cart = Cart(self.client)
        self.assertEqual(len(cart), 0)
