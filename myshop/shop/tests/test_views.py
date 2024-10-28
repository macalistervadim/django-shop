from http import HTTPStatus

import django.shortcuts
from django.test import TestCase

import shop.models


class TestProductListView(TestCase):
    def setUp(self):
        self.category = shop.models.Category.objects.create(
            name="Tea",
        )
        self.product = shop.models.Product.objects.create(
            category=self.category,
            name="Yellow tea",
            price=10,
        )

    def test_product_list_view(self):
        url = django.shortcuts.reverse("shop:product_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "shop/product/list.html")
        self.assertIn("categories", response.context)
        self.assertIn("products", response.context)
        self.assertEqual(
            response.context["products"][0].name,
            self.product.name,
        )

    def test_product_list_view_with_category(self):
        url = django.shortcuts.reverse(
            "shop:product_list_by_category",
            kwargs={"category_slug": "tea"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "shop/product/list.html")
        self.assertEqual(response.context["category"], self.category)
        self.assertEqual(len(response.context["products"]), 1)
        self.assertEqual(
            response.context["products"][0].name,
            self.product.name,
        )


class TestProductDetailView(TestCase):
    def setUp(self):
        self.category = shop.models.Category.objects.create(
            name="Tea",
        )
        self.product = shop.models.Product.objects.create(
            category=self.category,
            name="Yellow tea",
            price=10,
        )

    def test_product_detail_view_valid(self):
        url = django.shortcuts.reverse(
            "shop:product_detail",
            kwargs={"id": self.product.id, "slug": self.product.slug},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "shop/product/detail.html")
        self.assertEqual(response.context["product"].name, self.product.name)

    def test_product_detail_view_invalid_data(self):
        url = django.shortcuts.reverse(
            "shop:product_detail",
            kwargs={"id": 99999999, "slug": "invalid"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
