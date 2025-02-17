from django.contrib.admin.views.decorators import staff_member_required
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
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                orders.models.OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            order_created.delay(order.id)  # запустить асинхронное задание

            request.session["order_id"] = order.id  # задать заказ в сеансе
            return django.shortcuts.redirect(
                django.shortcuts.reverse("payment:process"),
            )
    else:
        form = orders.forms.OrderCreateForm()

    return django.shortcuts.render(
        request,
        "orders/order/create.html",
        {"form": form, "cart": cart},
    )


@staff_member_required
def admin_order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order = django.shortcuts.get_object_or_404(
        orders.models.Order,
        id=order_id,
    )

    return django.shortcuts.render(
        request,
        "admin/orders/order/detail.html",
        {"order": order},
    )
