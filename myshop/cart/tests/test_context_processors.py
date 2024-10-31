from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from cart.cart import Cart
from cart.context_processors import cart


class CartContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def add_session_to_request(self, request):
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()

    def test_cart_context_processor(self):
        request = self.factory.get("/")

        self.add_session_to_request(request)
        context = cart(request)
        self.assertIsInstance(context, dict)
        self.assertIn("cart", context)
        self.assertIsInstance(context["cart"], Cart)
