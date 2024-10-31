from http import HTTPStatus

from django.contrib.auth.models import User
import django.shortcuts
from django.test import TestCase

from shop.models import Category, Product


class TestCartDetailUrls(TestCase):

    def test_cart_detail_url_login_user(self):
        url = django.shortcuts.reverse("cart:cart_detail")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestCartAddUrls(TestCase):
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

    def test_cart_add_url_login_user(self):
        self.client.login(username="testuser", password="password")
        product_id = self.product.id

        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": product_id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("cart:cart_detail"),
        )

    def test_cart_add_url_anonymous_user(self):
        product_id = self.product.id

        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": product_id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cart_add_url_get_method(self):
        self.client.login(username="testuser", password="password")

        product_id = self.product.id
        url = django.shortcuts.reverse(
            "cart:cart_add",
            kwargs={"product_id": product_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class TestCartRemoveUrls(TestCase):
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

    def test_cart_remove_url_login_user(self):
        self.client.login(username="testuser", password="password")
        product_id = self.product.id

        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": product_id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("cart:cart_detail"),
        )

    def test_cart_remove_url_anonymous_user(self):
        product_id = self.product.id

        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": product_id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cart_remove_url_get_method(self):
        self.client.login(username="testuser", password="password")

        product_id = self.product.id
        url = django.shortcuts.reverse(
            "cart:cart_remove",
            kwargs={"product_id": product_id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
