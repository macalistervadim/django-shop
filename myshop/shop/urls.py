from django.urls import path

import shop.views


app_name = "shop"

urlpatterns = [
    path("", shop.views.product_list, name="product_list"),
    path(
        "<slug:category_slug>/",
        shop.views.product_list,
        name="product_list_by_category",
    ),
    path(
        "<int:id>/<slug:slug>/",
        shop.views.product_detail,
        name="product_detail",
    ),
]
