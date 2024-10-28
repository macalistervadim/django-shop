from typing import Any

import django.shortcuts
from django.db import models
from django.utils.text import slugify

import core.models


class Category(core.models.AbstractBaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> models.CharField:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"slug={self.slug!r})"
        )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return django.shortcuts.reverse(
            "shop:product_list_by_category",
            args=[self.slug]
        )


class Product(core.models.AbstractBaseModel):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="media/products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> models.CharField:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"category={self.category!r}, "
            f"name={self.name!r}, "
            f"slug={self.slug!r}, "
            f"image={self.image!r}, "
            f"price={self.price!r}, "
            f"description={self.description!r}, "
            f"available={self.available!r})"
            f"created={self.created!r}, "
            f"updated={self.updated!r})"
        )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return django.shortcuts.reverse(
            "shop:product_detail",
            args=[self.id, self.slug]
        )
