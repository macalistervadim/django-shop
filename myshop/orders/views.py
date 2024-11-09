from django.http import HttpRequest, HttpResponse
import django.shortcuts

from cart.cart import Cart
import orders.forms
import orders.models
from orders.tasks import order_created


def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == "POST":
        form = orders.forms.OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                orders.models.OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            order_created.delay(order.id)  # запустить асинхронное задание

            return django.shortcuts.render(
                request,
                "orders/order/created.html",
                {"order": order},
            )
    else:
        form = orders.forms.OrderCreateForm()

    return django.shortcuts.render(
        request,
        "orders/order/create.html",
        {"form": form, "cart": cart},
    )
