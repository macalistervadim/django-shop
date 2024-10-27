from django.contrib import admin

import shop.models as models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        models.Category.name.field.name,
        models.Category.slug.field.name,
    ]
    prepopulated_fields = {
        models.Category.slug.field.name: (models.Category.name.field.name,),
    }


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
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
    prepopulated_fields = {
        models.Product.slug.field.name: (models.Product.name.field.name,),
    }
