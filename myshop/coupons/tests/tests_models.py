import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

import coupons.models


class TestCouponModel(TestCase):
    def setUp(self):
        self.data = {
            "code": "Test",
            "valid_from": datetime.datetime(2024, 1, 1, 0, 0),
            "valid_to": datetime.datetime(2025, 1, 1, 0, 0),
            "discount": 20,
            "active": True,
        }

    def test_coupon_model_valid(self):
        coupon = coupons.models.Coupon.objects.create(**self.data)

        self.assertEqual(coupon.code, self.data["code"])
        self.assertEqual(coupon.valid_from, self.data["valid_from"])
        self.assertEqual(coupon.valid_to, self.data["valid_to"])
        self.assertEqual(coupon.discount, self.data["discount"])
        self.assertTrue(coupon.active)

    def test_coupon_str_representation(self):
        coupon = coupons.models.Coupon.objects.create(**self.data)
        self.assertEqual(str(coupon), "Test")

    def test_coupon_repr_representation(self):
        coupon = coupons.models.Coupon.objects.create(**self.data)
        self.assertEqual(
            repr(coupon),
            "Coupon(code='Test', "
            "valid_from=datetime.datetime(2024, 1, 1, 0, 0), "
            "valid_to=datetime.datetime(2025, 1, 1, 0, 0),"
            " discount=20, active=True)",
        )

    def test_invalid_discount_too_high(self):
        self.data["discount"] = 150
        with self.assertRaises(ValidationError):
            coupon = coupons.models.Coupon(**self.data)
            coupon.full_clean()

    def test_invalid_discount_negative(self):
        self.data["discount"] = -10
        with self.assertRaises(ValidationError):
            coupon = coupons.models.Coupon(**self.data)
            coupon.full_clean()

    def test_unique_code(self):
        coupons.models.Coupon.objects.create(**self.data)
        with self.assertRaises(ValidationError):
            coupon = coupons.models.Coupon(**self.data)
            coupon.full_clean()
