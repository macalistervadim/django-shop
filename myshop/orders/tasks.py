from celery import shared_task
from django.core.mail import send_mail

import orders.models


# todo: test
@shared_task
def order_created(order_id):
    """
    Задание по отправке уведомления по эл. почте
    при успешном создании заказа
    """
    order = orders.models.Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = (
        f"Dear {order.first_name}, \n\n"
        "Your order has been created."
        f"Your order ID is {order.id}."
    )
    mail_sent = send_mail(subject, message, "admin@myshop.com", [order.email])

    return mail_sent
