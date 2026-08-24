import os
from pathlib import Path
from PIL import Image
from django.conf import settings
from constants import AppConstants

_constants = AppConstants.get_instance()


def process_product_image(image_field):
    if not image_field or not image_field.name:
        return

    dirname, filename = os.path.split(image_field.name)
    media_root = Path(settings.MEDIA_ROOT)
    upload_dir = media_root / dirname if dirname else media_root

    full_base_path = upload_dir / filename
    if not full_base_path.exists():
        return

    try:
        with Image.open(full_base_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            for size in _constants.IMAGE_SIZES:
                resized_img = img.copy()
                resized_img.thumbnail((size, size), Image.Resampling.LANCZOS)
                sized_filename = f"{size}_{filename}"
                target_path = upload_dir / sized_filename
                resized_img.save(target_path, format=_constants.IMAGE_FORMAT, quality=90)
    finally:
        if full_base_path.exists():
            full_base_path.unlink()
