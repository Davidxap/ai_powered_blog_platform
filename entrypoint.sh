#!/usr/bin/env bash
set -e

echo "🔄 Waiting for PostgreSQL to be ready..."
until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Check if populate_categories command exists
if python manage.py help populate_categories >/dev/null 2>&1; then
  echo "🔄 Populating categories..."
  python manage.py populate_categories || true
fi

echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if credentials provided
if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  echo "🔄 Creating superuser (${DJANGO_SUPERUSER_USERNAME})..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
" || true
fi

echo "🚀 Starting Gunicorn server..."
exec python -m gunicorn simple_blog_ai.wsgi:application --bind 0.0.0.0:8000 -c gunicorn_config.py
