from django.urls import path

import payment.views
import payment.webhooks


app_name = "payment"


urlpatterns = [
    path("process/", payment.views.payment_process, name="process"),
    path("completed/", payment.views.payment_completed, name="completed"),
    path("canceled/", payment.views.payment_canceled, name="canceled"),
    path("webhook/", payment.webhooks.stripe_webhook, name="stripe-webhook"),
]
