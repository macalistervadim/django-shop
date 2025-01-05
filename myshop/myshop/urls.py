from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("coupons/", include("coupons.urls", namespace="coupons")),
    path("", include("shop.urls", namespace="shop")),
]

if settings.DEBUG:
    urlpatterns += (
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
        + debug_toolbar_urls()
    )
