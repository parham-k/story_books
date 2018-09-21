#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py makemigrations web_service
python manage.py migrate
python manage.py createsuperuser