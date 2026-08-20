import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.files import File
from catalog.models import Category, Product

SEEDING_DIR = Path(__file__).resolve().parent


def seed_categories():
    with open(SEEDING_DIR / "json" / "categories.json", encoding="utf-8") as f:
        for data in json.load(f):
            Category.objects.get_or_create(
                slug=data["slug"],
                defaults={"name": data["name"]},
            )


def seed_products():
    with open(SEEDING_DIR / "json" / "products.json", encoding="utf-8") as f:
        for data in json.load(f):
            category = Category.objects.get(slug=data["category_slug"])
            product, created = Product.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "category": category,
                    "description": data["description"],
                    "price": data["price"],
                },
            )
            if created:
                img_path = SEEDING_DIR / "images" / data["image_name"]
                if img_path.exists():
                    with open(img_path, "rb") as img_file:
                        product.image.save(data["image_name"], File(img_file), save=True)


if __name__ == "__main__":
    seed_categories()
    seed_products()