# School Site (production readiness)

This repository contains a Django site for Balabhadra Janata Higher Secondary School.

What I changed to prepare for hosting:

- Added `requirements.txt` (Django, gunicorn, whitenoise, python-dotenv, sitemap helper)
- Added `Procfile` and `runtime.txt` for Heroku-like deployments
- Added `.env.example` for environment variables
- Updated `school_site/settings.py` to load environment variables, enable WhiteNoise, secure cookies, and configure static files
- Added `main/sitemaps.py` and mounted sitemap in `school_site/urls.py`
- Added `main/templates/main/robots.txt` to expose sitemap and allow crawling
- Added SEO meta tags + JSON-LD to `main/templates/main/base.html`

Quick steps to deploy/run locally (Windows PowerShell):

1. Create and activate a virtualenv (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set values. For local dev you can set `DJANGO_DEBUG=True`.

3. Collect static files:

```powershell
python manage.py collectstatic --noinput
```

4. Run the development server:

```powershell
python manage.py runserver
```

Notes & next steps:
- Consider using PostgreSQL in production and configure `DATABASES` accordingly.
- Add an Open Graph image at `static/main/assets/og-image.png` (placeholder used in templates).
- Configure a proper SECRET_KEY and ensure `DJANGO_DEBUG=False` in production.
