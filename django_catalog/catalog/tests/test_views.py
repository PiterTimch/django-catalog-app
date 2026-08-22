from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from catalog.models import Category, Product
from constants import AppConstants

_constants = AppConstants.get_instance()


class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.cat_electronics = Category.objects.create(name="Electronics", slug="electronics")
        self.cat_books = Category.objects.create(name="Books", slug="books")

        for i in range(6):
            Product.objects.create(
                name=f"Electronics Product {i}",
                slug=f"electronics-product-{i}",
                category=self.cat_electronics,
                price=Decimal("100.00"),
            )
        for i in range(3):
            Product.objects.create(
                name=f"Book {i}",
                slug=f"book-{i}",
                category=self.cat_books,
                price=Decimal("20.00"),
            )

    def test_product_list_status_code(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "catalog/product_list.html")

    def test_product_list_shows_all_products_by_default(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertIn("products", response.context)

    def test_product_list_filter_by_category(self):
        url = reverse("catalog:product_list") + "?category=electronics"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products_page = response.context["products"]
        for product in products_page.object_list:
            self.assertEqual(product.category.slug, "electronics")

    def test_product_list_filter_by_nonexistent_category_returns_empty(self):
        url = reverse("catalog:product_list") + "?category=nonexistent"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"].object_list), 0)

    def test_product_list_custom_per_page(self):
        per_page = 2
        url = reverse("catalog:product_list") + f"?per_page={per_page}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["per_page"], per_page)
        self.assertLessEqual(len(response.context["products"].object_list), per_page)

    def test_product_list_invalid_per_page_uses_default(self):
        url = reverse("catalog:product_list") + "?per_page=abc"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["per_page"], _constants.DEFAULT_PER_PAGE)

    def test_product_list_per_page_not_in_options_uses_default(self):
        url = reverse("catalog:product_list") + "?per_page=7"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["per_page"], _constants.DEFAULT_PER_PAGE)

    def test_product_list_pagination_page_2(self):
        url = reverse("catalog:product_list") + "?per_page=4&page=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["products"].object_list), 0)

    def test_product_list_context_contains_categories(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertIn("categories", response.context)
        self.assertIn("selected_category", response.context)

    def test_product_list_context_contains_per_page_options(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertIn("per_page_options", response.context)
        self.assertEqual(response.context["per_page_options"], _constants.PER_PAGE_OPTIONS)

    def test_product_list_selected_category_in_context(self):
        url = reverse("catalog:product_list") + "?category=books"
        response = self.client.get(url)
        self.assertEqual(response.context["selected_category"], "books")

    def test_product_list_page_range_in_context(self):
        url = reverse("catalog:product_list")
        response = self.client.get(url)
        self.assertIn("page_range", response.context)


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            price=Decimal("999.99"),
            description="A powerful laptop.",
        )

    def test_product_detail_status_code(self):
        url = reverse("catalog:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_uses_correct_template(self):
        url = reverse("catalog:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "catalog/product_detail.html")

    def test_product_detail_context_has_product(self):
        url = reverse("catalog:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        self.assertIn("product", response.context)
        self.assertEqual(response.context["product"], self.product)

    def test_product_detail_shows_correct_data(self):
        url = reverse("catalog:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        product = response.context["product"]
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, Decimal("999.99"))
        self.assertEqual(product.description, "A powerful laptop.")
        self.assertEqual(product.category, self.category)

    def test_product_detail_404_for_nonexistent_slug(self):
        url = reverse("catalog:product_detail", args=["does-not-exist"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_related_category_preloaded(self):
        url = reverse("catalog:product_detail", args=[self.product.slug])
        response = self.client.get(url)
        product = response.context["product"]
        self.assertEqual(product.category.name, "Electronics")
