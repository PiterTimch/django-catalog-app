import os
import uuid


def product_image_path(instance, filename):
    return os.path.join("productImages/", f"{uuid.uuid4()}.webp")


def get_sized_image_url(image_field, size):
    if not image_field or not image_field.name:
        return ""
    dirname, filename = os.path.split(image_field.name)
    sized_filename = f"{size}_{filename}"
    sized_name = os.path.join(dirname, sized_filename) if dirname else sized_filename
    return image_field.storage.url(sized_name)
