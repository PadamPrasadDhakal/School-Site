FROM python:3.11-slim

# Install system packages needed for Pillow and common Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libffi-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt /app/

# Upgrade pip and install requirements
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput || true

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "school_site.wsgi:application", "--bind", "0.0.0.0:8000"]
