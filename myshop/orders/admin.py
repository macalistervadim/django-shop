import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
import django.shortcuts
from django.utils.safestring import mark_safe

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = [OrderItem.product.field.name]


def order_detail(obj):
    url = django.shortcuts.reverse(
        "orders:admin_order_detail", args=[obj.id],
    )

    return mark_safe(f"<a href='{url}'>View</a>")

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
              field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response
export_to_csv.short_description = "Export to CSV"

def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f"<a href='{url}' target='_blank'>{obj.stripe_id}</a>"
        return mark_safe(html)
    return ''
order_stripe_payment.short_description = 'Stripe Payment'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        Order.id.field.name,
        Order.first_name.field.name,
        Order.last_name.field.name,
        Order.email.field.name,
        Order.address.field.name,
        Order.postal_code.field.name,
        Order.city.field.name,
        Order.paid.field.name,
        order_stripe_payment,
        Order.created.field.name,
        Order.updated.field.name,
        order_detail,
    ]
    list_filter = [
        Order.paid.field.name,
        Order.created.field.name,
        Order.updated.field.name,
    ]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
