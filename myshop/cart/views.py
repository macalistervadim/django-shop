from django.http import HttpRequest, HttpResponse
import django.shortcuts
from django.views.decorators.http import require_POST

from cart.cart import Cart
import cart.forms
from coupons.forms import CouponApplyForm
import shop.models


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    cart_ = Cart(request)
    product = django.shortcuts.get_object_or_404(
        shop.models.Product,
        id=product_id,
    )
    form = cart.forms.CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart_.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )

    return django.shortcuts.redirect("cart:cart_detail")


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    cart_ = Cart(request)
    product = django.shortcuts.get_object_or_404(
        shop.models.Product,
        id=product_id,
    )
    cart_.remove(product=product)

    return django.shortcuts.redirect("cart:cart_detail")


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart_ = Cart(request)
    for item in cart_:
        item["update_quantity_form"] = cart.forms.CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True},
        )
    coupon_apply_form = CouponApplyForm()
    return django.shortcuts.render(
        request,
        "cart/detail.html",
        {"cart": cart_, "coupon_apply_form": coupon_apply_form},
    )
