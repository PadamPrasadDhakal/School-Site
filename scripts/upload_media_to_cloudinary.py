import os
import cloudinary.uploader
from django.conf import settings
from main.models import Teacher

def run():
  fname = 'teachers/518979667_1198525445624264_2111814113738436257_n.jpg'
  qs = Teacher.objects.filter(photo=fname)
  print(f'Found {qs.count()} teachers with photo {fname}')
  for t in qs:
    local_path = os.path.join(settings.BASE_DIR, fname)
    if not os.path.exists(local_path):
      print(f'File not found: {local_path}')
      continue
    res = cloudinary.uploader.upload(local_path, folder='main/teachers')
    public_id = res.get('public_id')
    fmt = res.get('format')
    if public_id and fmt:
      t.photo = f"{public_id}.{fmt}"
      t.save()
      print(f'Updated teacher id {t.pk}')
    else:
      print('Upload failed:', res)
