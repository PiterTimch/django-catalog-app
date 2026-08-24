# Django Catalog App

## Environment Files

- **Local**: `django_catalog/.env.example` (inside app directory) -> copy/rename to `django_catalog/.env.development`
- **Docker / Production**: `.env.example` (in root directory) -> copy/rename to `.env`

## Prerequisites
Rename `django_catalog/.env.example` to `django_catalog/.env.development` and update the environment variables inside to match your local database settings.

## Startup

0. Move to directory
```
cd .\django_catalog\
```

1. Create DB:
```
python -m uv run python create_db.py
```

2. Migrations:
```
python -m uv run python manage.py migrate
```

3. Seed data:
```
python -m uv run python seeding/seed.py
```

4. Create superuser:
```
python -m uv run python manage.py createsuperuser
```

5. Run server:
```
python -m uv run python manage.py runserver
```

## Tests

### All in one

```
python -m uv run python manage.py test catalog cart
```

### Separately

```
python -m uv run python manage.py test catalog
python -m uv run python manage.py test cart
python -m uv run python manage.py test catalog.tests.test_models
python -m uv run python manage.py test catalog.tests.test_views
python -m uv run python manage.py test cart.tests.test_cart
python -m uv run python manage.py test cart.tests.test_views
```

## Server Deployment (working for Ubontu 22.04)

1. Install Docker (if not installed):
```
sudo apt update
sudo apt install -y docker.io
```

2. Install Nginx (if not installed):
```
sudo apt update
sudo apt install -y nginx
```

3. Prepare Environment Variables:
Copy `.env.example` in root directory to `.env` and set environment variables:
```
cp .env.example .env
```

4. Configure Nginx:
Copy `default` Nginx configuration file from the project root to `/etc/nginx/sites-available/default`:
```
sudo cp default /etc/nginx/sites-available/default
sudo nginx -t
sudo systemctl restart nginx
```

5. Run Docker containers:
```
docker compose pull
docker compose up -d
```
