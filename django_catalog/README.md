# Django Catalog App

## Startup

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
