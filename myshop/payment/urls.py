from django.urls import path
from django.utils.translation import gettext_lazy as _

import payment.views
import payment.webhooks


app_name = "payment"


urlpatterns = [
    path(_("process/"), payment.views.payment_process, name="process"),
    path(_("completed/"), payment.views.payment_completed, name="completed"),
    path(_("canceled/"), payment.views.payment_canceled, name="canceled"),
]
