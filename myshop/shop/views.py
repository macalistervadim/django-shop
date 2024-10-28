import django.shortcuts

import shop.models


def product_list(request, category_slug=None):
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


def product_detail(request, id, slug):
    product = django.shortcuts.get_object_or_404(
        shop.models.Product,
        id=id,
        slug=slug,
        available=True,
    )

    return django.shortcuts.render(
        request,
        "shop/product/detail.html",
        {"product": product},
    )
