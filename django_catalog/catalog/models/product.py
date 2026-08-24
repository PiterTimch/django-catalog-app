from django.db import models
from .category import Category
from catalog.utils import product_image_path, process_product_image, get_sized_image_url
from constants import AppConstants

_constants = AppConstants.get_instance()


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            process_product_image(self.image)

    @property
    def image_small_url(self):
        return get_sized_image_url(self.image, _constants.IMAGE_SIZE_SMALL)

    @property
    def image_large_url(self):
        return get_sized_image_url(self.image, _constants.IMAGE_SIZE_LARGE)
