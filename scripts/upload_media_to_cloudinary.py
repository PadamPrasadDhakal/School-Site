"""Upload existing local media files to Cloudinary and update ImageField values.

Run this script after setting CLOUDINARY_URL in the environment (and installing
cloudinary). It will iterate common models with ImageFields and upload files
that look like local paths to Cloudinary, then replace the ImageField value
with the Cloudinary public_id + format so the configured storage backend
(`cloudinary_storage`) can generate the correct URL.

Usage:
    set CLOUDINARY_URL=...   # Windows PowerShell or env
    python scripts/upload_media_to_cloudinary.py

CAUTION: Back up your database before running. This script updates model
instances in-place.
"""

import os
from pathlib import Path
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_site.settings')
import django
django.setup()

from django.conf import settings
from django.db import transaction

try:
    import cloudinary.uploader
except Exception as e:
    raise RuntimeError('cloudinary is required. pip install cloudinary') from e

from main.models import Teacher, Post, PhotoAlbum, PhotoGallery, SagarmathaTeensClubMember

BASE_DIR = Path(settings.BASE_DIR)

MODEL_FIELD_MAP = {
    Teacher: ['photo'],
    Post: ['image'],
    PhotoAlbum: ['cover'],
    PhotoGallery: ['image'],
    SagarmathaTeensClubMember: ['photo'],
}

def is_already_cloudinary(value):
    """Return True if value appears to be a Cloudinary URL or already uploaded."""
    if not value:
        return True
    try:
        url = value.url
    except Exception:
        # If value is a simple string name, consider non-http values as local
        url = getattr(value, 'url', '')
    return 'res.cloudinary.com' in (url or '') or (str(value).startswith('http'))


def upload_file(local_path, folder=None):
    opts = {}
    if folder:
        opts['folder'] = folder
    print(f"Uploading {local_path} to Cloudinary...")
    res = cloudinary.uploader.upload(str(local_path), **opts)
    return res


def process_model(model, fields):
    qs = model.objects.all()
    total = qs.count()
    print(f'Processing {model.__name__}: {total} instances')
    for i, obj in enumerate(qs, 1):
        updated = False
        for field in fields:
            field_file = getattr(obj, field)
            # Skip empty
            if not field_file:
                continue
            # If already a cloudinary URL, skip
            try:
                url = field_file.url
            except Exception:
                url = None

            if url and 'res.cloudinary.com' in url:
                continue

            # Build local file path
            name = getattr(field_file, 'name', None)
            if not name:
                continue
            local_path = BASE_DIR / name
            if not local_path.exists():
                print(f'  [{i}/{total}] Local file not found: {local_path} (skipping)')
                continue

            try:
                folder = f"{model._meta.app_label}/{field}"
                res = upload_file(local_path, folder=folder)
                public_id = res.get('public_id')
                fmt = res.get('format')
                if public_id and fmt:
                    new_name = f"{public_id}.{fmt}"
                    setattr(obj, field, new_name)
                    updated = True
                    print(f'  [{i}/{total}] Uploaded and updated field {field} -> {new_name}')
                else:
                    print(f'  [{i}/{total}] Upload did not return public_id/format, result: {res}')
            except Exception:
                print(f'  [{i}/{total}] Error uploading {local_path}:')
                traceback.print_exc()

        if updated:
            try:
                obj.save()
            except Exception:
                print(f'  [{i}/{total}] Error saving object {obj}')
                traceback.print_exc()


def main():
    if not os.getenv('CLOUDINARY_URL'):
        print('CLOUDINARY_URL not set. Set the environment variable and try again.')
        return

    for model, fields in MODEL_FIELD_MAP.items():
        process_model(model, fields)

    print('Done uploading media to Cloudinary.')


if __name__ == '__main__':
    main()
