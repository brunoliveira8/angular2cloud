#!/bin/bash

# echo "Collect static files"
# python manage.py collectstatic --noinput

echo "Starting server"
gunicorn config.wsgi:application -w 2 -b :8000