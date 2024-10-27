import django.core.exceptions
from django.test import TestCase

import shop.models


class TestCategoryModel(TestCase):
    def test_category_model_valid(self):
        self.assertEqual(shop.models.Category.objects.count(), 0)

        new_category = shop.models.Category.objects.create(
            name="Test Category",
        )

        self.assertEqual(shop.models.Category.objects.count(), 1)
        self.assertEqual(new_category.slug, "test-category")

    def test_category_model_invalid(self):
        self.assertEqual(shop.models.Category.objects.count(), 0)

        long_name = "a" * 201
        category = shop.models.Category(name=long_name)

        with self.assertRaises(django.core.exceptions.ValidationError):
            category.full_clean()
            category.save()

        self.assertEqual(shop.models.Category.objects.count(), 0)


class TestProductModel(TestCase):
    def setUp(self):
        self.category = shop.models.Category.objects.create(
            name="Test Category",
        )

    def test_product_model_valid(self):
        self.assertEqual(shop.models.Product.objects.count(), 0)

        new_product = shop.models.Product.objects.create(
            category=self.category,
            name="Test Product",
            price=10,
        )
        self.assertEqual(shop.models.Product.objects.count(), 1)
        self.assertEqual(new_product.slug, "test-product")
        self.assertEqual(new_product.name, "Test Product")
        self.assertEqual(new_product.price, 10)

    def test_product_model_invalid_price_exceeds_max_digits(self):
        product = shop.models.Product(
            category=self.category,
            name="Test Product",
            price=1000000000,
        )

        with self.assertRaises(django.core.exceptions.ValidationError):
            product.full_clean()

        self.assertEqual(shop.models.Product.objects.count(), 0)
