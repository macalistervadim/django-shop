from django.contrib import admin
from parler.admin import TranslatableAdmin

import shop.models as models


@admin.register(models.Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = [
        models.Category.name.field.name,
        models.Category.slug.field.name,
    ]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(models.Product)
class ProductAdmin(TranslatableAdmin):
    list_display = [
        models.Product.name.field.name,
        models.Product.slug.field.name,
        models.Product.price.field.name,
        models.Product.available.field.name,
        models.Product.created.field.name,
        models.Product.updated.field.name,
    ]
    list_filter = [
        models.Product.available.field.name,
        models.Product.created.field.name,
        models.Product.updated.field.name,
    ]
    list_editable = [
        models.Product.price.field.name,
        models.Product.available.field.name,
    ]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
