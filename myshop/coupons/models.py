from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import core.models


class Coupon(core.models.AbstractBaseModel):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount for this coupon (0-100)",
    )
    active = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.code}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r}, "
            f"valid_from={self.valid_from!r}, "
            f"valid_to={self.valid_to!r}, "
            f"discount={self.discount!r}, "
            f"active={self.active!r})"
        )
