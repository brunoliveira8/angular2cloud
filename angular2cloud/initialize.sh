#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Starting server"
gunicorn config.wsgi:application -w 4 -b :8000