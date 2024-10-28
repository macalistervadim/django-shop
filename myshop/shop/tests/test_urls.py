from http import HTTPStatus

from django.test import TestCase
import django.shortcuts

import shop.models


class TestProductListUrls(TestCase):
    def test_product_list_url(self):
        url = django.shortcuts.reverse("shop:product_list")
        request = self.client.get(url)

        self.assertEqual(request.status_code, HTTPStatus.OK)


class TestProductListWithSlugUrls(TestCase):
    def test_product_list_with_slug_url_success(self):
        category = shop.models.Category.objects.create(
            name="Tea",
        )

        url = django.shortcuts.reverse("shop:product_list_by_category", args=[category.slug])
        request = self.client.get(url)

        self.assertEqual(request.status_code, HTTPStatus.OK)

    def test_product_list_with_slug_url_invalid_slug(self):
        url = django.shortcuts.reverse("shop:product_list_by_category", args=["invalid"])
        request = self.client.get(url)

        self.assertEqual(request.status_code, HTTPStatus.NOT_FOUND)


class TestProductDetailUrls(TestCase):
    def setUp(self):
        self.category = shop.models.Category.objects.create(
            name="Tea",
        )

    def test_product_detail_url(self):
        product = shop.models.Product.objects.create(
            category=self.category,
            name="Yellow tea",
            price=10,
        )
        url = django.shortcuts.reverse("shop:product_detail", args=[product.id, product.slug])
        request = self.client.get(url)

        self.assertEqual(request.status_code, HTTPStatus.OK)

    def test_product_detail_url_invalid_data(self):
        url = django.shortcuts.reverse("shop:product_detail", args=[9999999, "invalid"])
        request = self.client.get(url)

        self.assertEqual(request.status_code, HTTPStatus.NOT_FOUND)


