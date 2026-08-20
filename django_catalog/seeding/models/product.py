from dataclasses import dataclass


@dataclass
class SeedProduct:
    name: str
    slug: str
    category_slug: str
    description: str
    price: float
    image_name: str
