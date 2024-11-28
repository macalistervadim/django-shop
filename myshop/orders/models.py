from django.conf import settings
from django.db import models

import core.models
from shop.models import Product


class Order(core.models.AbstractBaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

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

    def get_total_sum(self) -> int:
        return sum(item.get_cost() for item in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            return ""
        if "__test__" in settings.STRIPE_SECRET_KEY:
            path = "/test/"
        else:
            path = "/"
        return f"https://dashboard.stripe.com{path}payment/{self.stripe_id}"


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
