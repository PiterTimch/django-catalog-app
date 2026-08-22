from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from catalog.models import Category, Product
from cart.cart import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product1 = Product.objects.create(
            name="Laptop", slug="laptop", category=self.category, price=Decimal("1000.00")
        )
        self.product2 = Product.objects.create(
            name="Mouse", slug="mouse", category=self.category, price=Decimal("25.50")
        )

    def _get_request(self):
        request = self.factory.get("/")
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_add_and_len(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)

        self.assertEqual(len(cart), 3)
        self.assertIn(str(self.product1.id), request.session['cart'])

    def test_invalid_quantity_raises_error(self):
        request = self._get_request()
        cart = Cart(request)
        with self.assertRaises(ValueError):
            cart.add(self.product1, quantity=0)
        with self.assertRaises(ValueError):
            cart.add(self.product1, quantity=-2)
        with self.assertRaises(ValueError):
            cart.update_quantity(self.product1, quantity=0)

    def test_update_quantity(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=1)
        cart.update_quantity(self.product1, quantity=5)

        self.assertEqual(len(cart), 5)
        self.assertEqual(request.session['cart'][str(self.product1.id)]['quantity'], 5)

    def test_remove(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=1)
        cart.remove(self.product1)

        self.assertEqual(len(cart), 0)
        self.assertNotIn(str(self.product1.id), request.session['cart'])

    def test_get_total_price(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=3)

        self.assertEqual(cart.get_total_price(), Decimal("2076.50"))

    def test_clean_deleted_products(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=1)
        cart.add(self.product2, quantity=1)

        self.product1.delete()

        cart.clean_deleted_products()

        self.assertNotIn(str(self.product1.id), request.session['cart'])
        self.assertIn(str(self.product2.id), request.session['cart'])
        self.assertEqual(len(cart), 1)

    def test_add_override_quantity(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=3)
        cart.add(self.product1, quantity=1, override_quantity=True)

        self.assertEqual(len(cart), 1)

    def test_get_total_price_empty_cart(self):
        request = self._get_request()
        cart = Cart(request)

        self.assertEqual(cart.get_total_price(), Decimal("0"))

    def test_update_quantity_on_absent_product_does_nothing(self):
        request = self._get_request()
        cart = Cart(request)
        cart.update_quantity(self.product1, quantity=5)

        self.assertEqual(len(cart), 0)

    def test_remove_absent_product_does_nothing(self):
        request = self._get_request()
        cart = Cart(request)
        cart.remove(self.product1)

        self.assertEqual(len(cart), 0)

    def test_clear(self):
        request = self._get_request()
        cart = Cart(request)
        cart.add(self.product1, quantity=1)
        cart.clear()

        self.assertEqual(len(cart), 0)
        self.assertEqual(request.session['cart'], {})
