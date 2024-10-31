from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = [OrderItem.product.field.name]


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
        Order.created.field.name,
        Order.updated.field.name,
    ]
    list_filter = [
        Order.paid.field.name,
        Order.created.field.name,
        Order.updated.field.name,
    ]
    inlines = [OrderItemInline]
