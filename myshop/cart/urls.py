from django.urls import path

import cart.views


app_name = "cart"

urlpatterns = [
    path("", cart.views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", cart.views.cart_add, name="cart_add"),
    path(
        "remove/<int:product_id>/",
        cart.views.cart_remove,
        name="cart_remove",
    ),
]
