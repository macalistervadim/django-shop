from django.db import models
import django.shortcuts
import django.urls
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200, unique=True),
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return (
            self.safe_translation_getter("name", any_language=True)
            or "Unnamed Category"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.safe_translation_getter(
                'name', any_language=True)!r}, "
            f"slug={self.slug!r})"
        )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(
                self.safe_translation_getter("name", any_language=True),
            )
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return django.urls.reverse(
            "shop:product_list_by_category",
            args=[self.slug],
        )


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(max_length=200, unique=True),
        description=models.TextField(blank=True),
    )
    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="media/products/%Y/%m/%d", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self) -> str:
        return (
            self.safe_translation_getter("name", any_language=True)
            or "Unnamed Product"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"category={self.category!r}, "
            f"name={self.safe_translation_getter(
                'name', any_language=True)!r}, "
            f"slug={self.safe_translation_getter(
                'slug', any_language=True)!r}, "
            f"image={self.image!r}, "
            f"price={self.price!r}, "
            f"description={self.safe_translation_getter(
                'description', any_language=True)!r}, "
            f"available={self.available!r})"
        )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(
                self.safe_translation_getter("name", any_language=True),
            )
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return django.urls.reverse(
            "shop:product_detail",
            args=[
                self.id,
                self.safe_translation_getter("slug", any_language=True),
            ],
        )
