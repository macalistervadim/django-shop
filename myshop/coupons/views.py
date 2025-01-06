from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

import coupons.forms
import coupons.models


@require_POST
def coupon_apply(request: HttpRequest) -> HttpResponse:
    now = timezone.now()
    form = coupons.forms.CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = coupons.models.Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session["coupon_id"] = coupon.id
            messages.success(request, "Coupon successfully activated.")
        except coupons.models.Coupon.DoesNotExist:
            request.session["coupon_id"] = (
                None  # TODO: здесь надо добавить мол если промо уже был - то запоминть его и не заменять на NONE
            )
            messages.error(request, "Coupon not found.")
    return redirect("cart:cart_detail")
