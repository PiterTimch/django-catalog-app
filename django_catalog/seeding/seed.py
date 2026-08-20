import os
import sys
import json
from pathlib import Path
import django
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from catalog.models import Category, Product
from seeding.models import SeedCategory, SeedProduct


def map_category(seed: SeedCategory) -> Category:
    return Category(name=seed.name, slug=seed.slug)


def map_product(seed: SeedProduct, category: Category) -> Product:
    return Product(
        name=seed.name,
        slug=seed.slug,
        category=category,
        description=seed.description,
        price=seed.price,
    )


with open(BASE_DIR / "seeding" / "json" / "categories.json", encoding="utf-8") as f:
    categories_data = json.load(f)
categories = [SeedCategory(**item) for item in categories_data]

for cat in categories:
    if not Category.objects.filter(slug=cat.slug).exists():
        map_category(cat).save()

with open(BASE_DIR / "seeding" / "json" / "products.json", encoding="utf-8") as f:
    products_data = json.load(f)
products = [SeedProduct(**item) for item in products_data]

for prod in products:
    if not Product.objects.filter(slug=prod.slug).exists():
        category = Category.objects.get(slug=prod.category_slug)
        product = map_product(prod, category)
        img_path = BASE_DIR / "seeding" / "images" / prod.image_name
        if img_path.exists():
            with open(img_path, "rb") as img_file:
                product.image.save(prod.image_name, File(img_file), save=False)
        product.save()
