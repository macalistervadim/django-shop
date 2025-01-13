from django.urls import path
from django.utils.translation import gettext_lazy as _

import orders.views


app_name = "orders"

urlpatterns = [
    path(
        _("create/"),
        orders.views.order_create,
        name="order_create",
    ),
    path(
        "admin/order/<int:order_id>/",
        orders.views.admin_order_detail,
        name="admin_order_detail",
    ),
]
