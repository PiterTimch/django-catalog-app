from decimal import Decimal
from django.test import TestCase
from django.db import IntegrityError
from catalog.models import Category, Product


class CategoryModelTestCase(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Electronics", slug="electronics")
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.slug, "electronics")

    def test_str_representation(self):
        category = Category.objects.create(name="Books", slug="books")
        self.assertEqual(str(category), "Books")

    def test_slug_is_unique(self):
        Category.objects.create(name="Electronics", slug="electronics")
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Electronics 2", slug="electronics")

    def test_multiple_categories(self):
        Category.objects.create(name="Electronics", slug="electronics")
        Category.objects.create(name="Books", slug="books")
        Category.objects.create(name="Clothing", slug="clothing")
        self.assertEqual(Category.objects.count(), 3)


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", slug="electronics")

    def test_create_product(self):
        product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            price=Decimal("999.99"),
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.slug, "laptop")
        self.assertEqual(product.price, Decimal("999.99"))
        self.assertEqual(product.category, self.category)

    def test_str_representation(self):
        product = Product.objects.create(
            name="Mouse",
            slug="mouse",
            category=self.category,
            price=Decimal("25.00"),
        )
        self.assertEqual(str(product), "Mouse")

    def test_slug_is_unique(self):
        Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            price=Decimal("999.99"),
        )
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Laptop 2",
                slug="laptop",
                category=self.category,
                price=Decimal("1200.00"),
            )

    def test_optional_fields(self):
        product = Product.objects.create(
            name="Keyboard",
            slug="keyboard",
            category=self.category,
            price=Decimal("50.00"),
        )
        self.assertEqual(product.description, "")
        self.assertFalse(product.image)

    def test_product_description(self):
        product = Product.objects.create(
            name="Monitor",
            slug="monitor",
            category=self.category,
            price=Decimal("300.00"),
            description="A great 4K monitor.",
        )
        self.assertEqual(product.description, "A great 4K monitor.")

    def test_cascade_delete_category_removes_products(self):
        Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            price=Decimal("999.99"),
        )
        self.assertEqual(Product.objects.count(), 1)
        self.category.delete()
        self.assertEqual(Product.objects.count(), 0)

    def test_related_name_products(self):
        Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            price=Decimal("999.99"),
        )
        Product.objects.create(
            name="Mouse",
            slug="mouse",
            category=self.category,
            price=Decimal("25.00"),
        )
        self.assertEqual(self.category.products.count(), 2)

    def test_multiple_products_in_category(self):
        for i in range(5):
            Product.objects.create(
                name=f"Product {i}",
                slug=f"product-{i}",
                category=self.category,
                price=Decimal("10.00"),
            )
        self.assertEqual(Product.objects.filter(category=self.category).count(), 5)
