from django.core.management.base import BaseCommand
import os
from pathlib import Path
import traceback

class Command(BaseCommand):
    help = 'Upload local media files to Cloudinary and update ImageField values.'

    def handle(self, *args, **options):
        try:
            from django.conf import settings
            import django
            django.setup()
            from main.models import Teacher, Post, PhotoAlbum, PhotoGallery, SagarmathaTeensClubMember
            try:
                import cloudinary.uploader
            except Exception:
                self.stderr.write('cloudinary package is required. Run pip install cloudinary')
                return

            BASE_DIR = Path(settings.BASE_DIR)

            MODEL_FIELD_MAP = {
                Teacher: ['photo'],
                Post: ['image'],
                PhotoAlbum: ['cover'],
                PhotoGallery: ['image'],
                SagarmathaTeensClubMember: ['photo'],
            }

            def upload_file(local_path, folder=None):
                opts = {}
                if folder:
                    opts['folder'] = folder
                self.stdout.write(f"Uploading {local_path} to Cloudinary...")
                res = cloudinary.uploader.upload(str(local_path), **opts)
                return res

            for model, fields in MODEL_FIELD_MAP.items():
                qs = model.objects.all()
                total = qs.count()
                self.stdout.write(f'Processing {model.__name__}: {total} instances')
                for i, obj in enumerate(qs, 1):
                    updated = False
                    for field in fields:
                        field_file = getattr(obj, field)
                        if not field_file:
                            continue
                        try:
                            url = field_file.url
                        except Exception:
                            url = None
                        if url and 'res.cloudinary.com' in url:
                            continue
                        name = getattr(field_file, 'name', None)
                        if not name:
                            continue
                        local_path = BASE_DIR / name
                        if not local_path.exists():
                            self.stdout.write(f'  [{i}/{total}] Local file not found: {local_path} (skipping)')
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
                                self.stdout.write(f'  [{i}/{total}] Uploaded and updated field {field} -> {new_name}')
                            else:
                                self.stdout.write(f'  [{i}/{total}] Upload did not return public_id/format, result: {res}')
                        except Exception:
                            self.stdout.write(f'  [{i}/{total}] Error uploading {local_path}:')
                            traceback.print_exc()
                    if updated:
                        try:
                            obj.save()
                        except Exception:
                            self.stdout.write(f'  [{i}/{total}] Error saving object {obj}')
                            traceback.print_exc()

            self.stdout.write('Done uploading media to Cloudinary.')

        except Exception as e:
            self.stderr.write(str(e))
*** End Patch