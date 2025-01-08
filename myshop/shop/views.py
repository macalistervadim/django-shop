from typing import Any

from django.http import HttpRequest, HttpResponse
import django.shortcuts

import cart.forms
import shop.models
from shop.recommender import Recommender


def product_list(
    request: HttpRequest,
    category_slug: Any = None,
) -> HttpResponse:
    category = None
    categories = shop.models.Category.objects.all()
    products = shop.models.Product.objects.filter(available=True)

    if category_slug:
        category = django.shortcuts.get_object_or_404(
            shop.models.Category,
            slug=category_slug,
        )
        products = products.filter(category=category)

    return django.shortcuts.render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request: HttpRequest, id: int, slug: Any) -> HttpResponse:
    product = django.shortcuts.get_object_or_404(
        shop.models.Product,
        id=id,
        slug=slug,
        available=True,
    )
    cart_product_form = cart.forms.CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product])

    return django.shortcuts.render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )
