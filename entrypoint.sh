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
if python manage.py help populate_categories >/dev/null 2>&1; then
  echo "🔄 Populating categories..."
  python manage.py populate_categories || true
fi
echo "🔄 Collecting static files..."
python manage.py collectstatic --noinput
if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  echo "🔄 Creating superuser (${DJANGO_SUPERUSER_USERNAME})..."
  python manage.py createsuperuser --noinput || true
fi
echo "🚀 Starting Gunicorn server..."
exec python -m gunicorn simple_blog_ai.wsgi:application -c gunicorn_config.py
