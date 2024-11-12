from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest, HttpResponse
import django.shortcuts
import stripe

import orders.models


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request: HttpRequest) -> HttpResponse:
    order_id = request.session.get("order_id", None)
    order = django.shortcuts.get_object_or_404(
        orders.models.Order,
        id=order_id,
    )
    if request.method == "POST":
        success_url = request.build_absolute_uri(
            django.shortcuts.reverse("payment:completed"),
        )
        cancel_url = request.build_absolute_uri(
            django.shortcuts.reverse("payment:canceled"),
        )

        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }  # данные сеанса оформления платежа Stripe
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                },
            )
        session = stripe.checkout.Session.create(**session_data)

        return django.shortcuts.redirect(session.url, code=303)
    else:
        return django.shortcuts.render(
            request,
            "payment/process.html",
            locals(),
        )


# todo: test


def payment_completed(request: HttpRequest) -> HttpResponse:
    return django.shortcuts.render(request, "payment/completed.html")


def payment_canceled(request: HttpRequest) -> HttpResponse:
    return django.shortcuts.render(request, "payment/canceled.html")
