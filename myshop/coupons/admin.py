from django.contrib import admin

from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        Coupon.code.field.name,
        Coupon.valid_from.field.name,
        Coupon.valid_to.field.name,
        Coupon.discount.field.name,
        Coupon.active.field.name,
    ]
    list_filter = [
        Coupon.active.field.name,
        Coupon.valid_from.field.name,
        Coupon.valid_to.field.name,
    ]
    search_fields = [Coupon.code.field.name]
