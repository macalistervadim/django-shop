from decimal import Decimal
from typing import Any, Generator

from django.conf import settings
from django.http import HttpRequest

from shop.models import Product

# TODO: Тесты!


class Cart:
    """
    Класс корзины покупок посредством джанго-сессий
    """

    def __init__(self, request: HttpRequest) -> None:
        """
        Инициализируем корзину покупок клиента.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(
        self,
        product: Any,
        quantity: int = 1,
        override_quantity: bool = False,
    ) -> None:
        """
        Добавление товара в корзину либо обновление его кол-ва
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self) -> None:
        """
        Сохранение изменений сеанса
        """
        self.session.modified = True

    def remove(self, product: Any) -> None:
        """
        Удаление товара из корзины
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> Generator[Any, Any, None]:
        """
        Получение товаров из базы данных
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        """
        Кол-во товарных позиций в корзине
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> int:
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self) -> None:
        """
        Удаление корзины из сеанса
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
