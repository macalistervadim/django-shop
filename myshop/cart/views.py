import django.shortcuts
from django.views.decorators.http import require_POST

from cart.cart import Cart
import cart.forms
import shop.models


@require_POST
def cart_add(request, product_id):
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
def cart_remove(request, product_id):
    cart_ = Cart(request)
    product = django.shortcuts.get_object_or_404(
        shop.models.Product,
        id=product_id,
    )
    cart_.remove(product=product)

    return django.shortcuts.redirect("cart:cart_detail")


def cart_detail(request):
    cart_ = Cart(request)
    for item in cart_:
        item["update_quantity_form"] = cart.forms.CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True},
        )
    return django.shortcuts.render(
        request,
        "cart/detail.html",
        {"cart": cart_},
    )
