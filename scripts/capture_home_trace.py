import os
import sys
import traceback
from pathlib import Path

# Ensure project root is on sys.path so imports like "school_site" and "main" resolve
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Force DEBUG for this diagnostic run so settings allow 'testserver' and show
# full tracebacks in templates rendered by RequestFactory/TestClient.
os.environ.setdefault('DJANGO_DEBUG', 'True')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_site.settings')

import django

try:
    django.setup()
except Exception:
    traceback.print_exc()
    raise


from django.test import RequestFactory

from main import views

rf = RequestFactory()
req = rf.get('/')

try:
    resp = views.home(req)
    # If the view returns a HttpResponse, render it to access template-related errors
    # TemplateResponse objects support .render(); HttpResponse does not.
    if hasattr(resp, 'render'):
        try:
            rendered = resp.render()
            content = rendered.content.decode('utf-8', errors='replace')
            print('View returned status:', getattr(resp, 'status_code', 'n/a'))
            print('Rendered content (first 2000 chars):')
            print(content[:2000])
        except Exception:
            print('Error while rendering TemplateResponse:')
            traceback.print_exc()
    else:
        # Fallback for plain HttpResponse
        try:
            content = resp.content.decode('utf-8', errors='replace')
            print('View returned status:', getattr(resp, 'status_code', 'n/a'))
            print('Response content (first 2000 chars):')
            print(content[:2000])
        except Exception:
            print('Error while decoding HttpResponse content:')
            traceback.print_exc()
except Exception:
    print('Exception when calling view:')
    traceback.print_exc()
