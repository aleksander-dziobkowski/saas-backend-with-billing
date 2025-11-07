#!/bin/sh

echo "⏳ Waiting for database..."
sleep 5

echo "🚀 Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
