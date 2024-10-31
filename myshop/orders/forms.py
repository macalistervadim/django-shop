from django import forms

import orders.models


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = orders.models.Order
        fields = [
            orders.models.Order.first_name.field.name,
            orders.models.Order.last_name.field.name,
            orders.models.Order.email.field.name,
            orders.models.Order.address.field.name,
            orders.models.Order.postal_code.field.name,
            orders.models.Order.city.field.name,
        ]
