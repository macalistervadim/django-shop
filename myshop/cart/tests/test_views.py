from http import HTTPStatus

from django.contrib.auth.models import User
import django.shortcuts
from django.test import TestCase

import cart.cart
from shop.models import Category, Product


class TestCartDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )

        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=5.99,
        )

    def test_cart_detail_view(self):
        url = django.shortcuts.reverse("cart:cart_detail")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cart/detail.html")

    def test_cart_detail_view_with_products(self):
        self.client.login(username="testuser", password="password")

        # Добавляем продукт в корзину
        add_product_response = self.client.post(
            django.shortcuts.reverse(
                "cart:cart_add",
                kwargs={"product_id": self.product.id},
            ),
            data={"quantity": 1},
        )
        self.assertEqual(add_product_response.status_code, HTTPStatus.FOUND)

        url = django.shortcuts.reverse("cart:cart_detail")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "cart/detail.html")
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.price)
        self.assertContains(response, "1")


class TestCartRemoveView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=5.99,
        )
        self.client.login(username="testuser", password="password")

    def test_cart_remove_view(self):
        # Добавляем продукт в корзину
        add_product_url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        self.client.post(add_product_url, data={"quantity": 1})

        remove_url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": self.product.id},
        )
        response = self.client.post(remove_url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("cart:cart_detail"),
        )

        cart_ = cart.cart.Cart(self.client)
        self.assertEqual(len(cart_), 0)

    def test_cart_remove_anonymous_user(self):
        self.client.logout()
        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": self.product.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cart_remove_non_existing_product(self):
        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": 999},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_cart_remove_not_allowed_methods(self):
        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": self.product.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class TestCartAddView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
        )
        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            price=5.99,
        )
        self.client.login(username="testuser", password="password")

    def test_cart_add_view_valid_data(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        response = self.client.post(
            url,
            data={"quantity": 2, "override": False},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("cart:cart_detail"),
        )

        cart_ = cart.cart.Cart(self.client)
        self.assertEqual(len(cart_), 2)

    def test_cart_add_view_invalid_data(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        self.client.post(
            url,
            data={"quantity": -1, "override": False},
        )

        cart_ = cart.cart.Cart(self.client)
        self.assertEqual(len(cart_), 0)

    def test_cart_add_view_override_quantity(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        self.client.post(url, data={"quantity": 1, "override": False})

        self.client.post(url, data={"quantity": 5, "override": True})

        cart_ = cart.cart.Cart(self.client)
        self.assertEqual(len(cart_), 5)

    def test_cart_add_view_not_allowed_methods(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": self.product.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_cart_add_view_non_existent_product(self):
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": 999},
        )
        response = self.client.post(
            url,
            data={"quantity": 1, "override": False},
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
