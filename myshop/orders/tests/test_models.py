from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

import orders.models
import shop.models


class TestOrderModel(TestCase):
    def test_order_model_valid(self):
        count = orders.models.Order.objects.count()
        self.assertEqual(count, 0)

        order = orders.models.Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="mail@mail.ru",
            address="Mark 2 two",
            postal_code="12345",
            city="America",
        )
        self.assertEqual(order.first_name, "John")
        self.assertEqual(order.last_name, "Doe")
        self.assertEqual(order.email, "mail@mail.ru")
        self.assertEqual(order.address, "Mark 2 two")
        self.assertEqual(order.postal_code, "12345")
        self.assertEqual(order.city, "America")
        count = orders.models.Order.objects.count()
        self.assertEqual(count, 1)

    def test_order_model_invalid(self):
        count = orders.models.Order.objects.count()
        self.assertEqual(count, 0)

        order = orders.models.Order(
            first_name="John",
            last_name="Doe",
            email="mailmailamila",
            address="Mark 2 two",
            postal_code="12345",
            city="America",
        )

        with self.assertRaises(ValidationError):
            order.full_clean()

        count = orders.models.Order.objects.count()
        self.assertEqual(count, 0)


class TestOrderItem(TestCase):
    def setUp(self):
        self.category = shop.models.Category.objects.create(
            name="category",
        )
        self.product = shop.models.Product.objects.create(
            category=self.category,
            name="Test Product",
            price=1000,
        )
        self.order = orders.models.Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="mail@mail.ru",
            address="Mark 2 two",
            postal_code="12345",
            city="America",
        )

    def test_order_item_model_valid(self):
        count = orders.models.OrderItem.objects.count()
        self.assertEqual(count, 0)

        order_item = orders.models.OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=Decimal(10),
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, 10)

        count = orders.models.OrderItem.objects.count()
        self.assertEqual(count, 1)

    def test_order_item_model_invalid_price(self):
        with self.assertRaises(ValidationError):
            order_item = orders.models.OrderItem(
                order=self.order,
                product=self.product,
                quantity=1,
                price=Decimal("1000000000"),
            )
            order_item.full_clean()

    def test_order_item_model_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            order_item = orders.models.OrderItem(
                order=self.order,
                product=self.product,
                quantity=-1,
                price=Decimal("10.00"),
            )
            order_item.full_clean()
