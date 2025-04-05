#!/bin/sh
set -e

# Run migrations
# python manage.py makemigrations
python manage.py migrate --noinput

# Optionally, collect static files if needed
# python manage.py collectstatic --noinput

# Execute the passed command (e.g., gunicorn or runserver)
exec "$@"
