from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Product


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Keyboard", slug="keyboard", category=self.category, price=Decimal("50.00")
        )

    def test_cart_add_view_catalog(self):
        url = reverse("cart:cart_add", args=[self.product.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("cart:cart_detail"))
        self.assertEqual(self.client.session["cart"][str(self.product.id)]["quantity"], 1)

    def test_cart_add_view_detail_page_custom_quantity(self):
        url = reverse("cart:cart_add", args=[self.product.id])
        response = self.client.post(url, {"quantity": 3})
        self.assertRedirects(response, reverse("cart:cart_detail"))
        self.assertEqual(self.client.session["cart"][str(self.product.id)]["quantity"], 3)

    def test_cart_update_view(self):
        add_url = reverse("cart:cart_add", args=[self.product.id])
        self.client.post(add_url, {"quantity": 1})

        update_url = reverse("cart:cart_update", args=[self.product.id])
        response = self.client.post(update_url, {"quantity": 5})
        self.assertRedirects(response, reverse("cart:cart_detail"))
        self.assertEqual(self.client.session["cart"][str(self.product.id)]["quantity"], 5)

    def test_cart_remove_view(self):
        add_url = reverse("cart:cart_add", args=[self.product.id])
        self.client.post(add_url, {"quantity": 1})

        remove_url = reverse("cart:cart_remove", args=[self.product.id])
        response = self.client.post(remove_url)
        self.assertRedirects(response, reverse("cart:cart_detail"))
        self.assertNotIn(str(self.product.id), self.client.session["cart"])

    def test_cart_detail_view(self):
        url = reverse("cart:cart_detail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_404_for_non_existent_product(self):
        non_existent_id = 99999
        add_url = reverse("cart:cart_add", args=[non_existent_id])
        update_url = reverse("cart:cart_update", args=[non_existent_id])
        remove_url = reverse("cart:cart_remove", args=[non_existent_id])

        self.assertEqual(self.client.post(add_url).status_code, 404)
        self.assertEqual(self.client.post(update_url).status_code, 404)
        self.assertEqual(self.client.post(remove_url).status_code, 404)
