#!/bin/sh

.venv/bin/python manage.py migrate --noinput

.venv/bin/python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
import os
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

.venv/bin/python seeding/seed.py || echo "Seeding skipped or failed, continuing..."

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
