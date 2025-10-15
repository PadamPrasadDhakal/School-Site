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

Render-specific deploy troubleshooting
-------------------------------------
If you're deploying to Render (or another host that builds from your repo), you may see errors during pip's build step like "Getting requirements to build wheel: finished with status 'error'". Common fixes:

1. Upgrade pip, setuptools, and wheel as a pre-build step (add this to Render's build commands):

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

2. Use a Python runtime that has wide wheel availability (e.g., Python 3.11 or 3.12) — set `runtime.txt` or the environment's Python version accordingly.

3. If a specific package fails to build, identify it in the verbose pip log and pin it to a version that provides wheels for your Python version, or install required OS-level libraries in the build image (for Pillow, install libjpeg, zlib, etc.).

If you'd like I can add a Render-specific `start`/`build` script or prepare a Dockerfile that ensures OS dependencies are installed before pip runs.
I added a sample `Dockerfile` to this repo which installs system dependencies (libjpeg, zlib, etc.), upgrades pip/setuptools/wheel and installs the Python dependencies.

To build and run locally with Docker:

```bash
docker build -t bjss:latest .
docker run -p 8000:8000 --env-file .env bjss:latest
```

Using Docker on Render
- If Render's build environment fails to build wheels, a Docker deployment (Render supports Docker) solves the issue by allowing you to install OS dependencies before pip.

