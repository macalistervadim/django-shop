from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models
from coupons.models import Coupon
from shop.models import Product


class Order(core.models.AbstractBaseModel):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("e-mail"))
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal code"), max_length=20)
    city = models.CharField(_("city"), max_length=100)
    paid = models.BooleanField(_("paid"), default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name="orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return f"Order {self.id}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.first_name!r}, "
            f"{self.last_name!r}, "
            f"{self.email!r}, "
            f"{self.address!r}, "
            f"{self.postal_code!r}, "
            f"{self.city!r}, "
            f"{self.paid!r}, "
            f"{self.stripe_id!r})"
        )

    def get_total_sum(self) -> Decimal:
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self) -> str:
        if not self.stripe_id:
            return ""
        if "__test__" in settings.STRIPE_SECRET_KEY:
            path = "/test/"
        else:
            path = "/"
        return f"https://dashboard.stripe.com{path}payment/{self.stripe_id}"

    def get_total_cost_before_discount(self) -> int:
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self) -> Decimal:
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


class OrderItem(core.models.AbstractBaseModel):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.order!r}, "
            f"{self.product!r}, "
            f"{self.price!r}, "
            f"{self.quantity!r})"
        )

    def get_cost(self) -> float:
        return self.price * self.quantity
