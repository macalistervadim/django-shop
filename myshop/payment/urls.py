from django.urls import path

import payment.views


app_name = "payment"


urlpatterns = [
    path("process/", payment.views.payment_process, name="process"),
    path("completed/", payment.views.payment_completed, name="completed"),
    path("canceled/", payment.views.payment_canceled, name="canceled"),
]  # todo: test
