# Django Catalog App

## Prerequisites
Rename .env.example to .env.development and update the environment variables inside to match your local database settings.

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
