from django.urls import path

import orders.views


app_name = "orders"

urlpatterns = [
    path(
        "create/",
        orders.views.order_create,
        name="order_create",
    ),
    path("admin/order/<int:order_id>/", orders.views.admin_order_detail, name="admin_order_detail"),
]
