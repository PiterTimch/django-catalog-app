@echo off

cd django_catalog
docker build -t django-catalog-app .
docker tag django-catalog-app:latest pedro007salo/django-catalog-app:latest
docker push pedro007salo/django-catalog-app:latest

echo DONE
pause