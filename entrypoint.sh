#!/bin/sh
set -e

# Применяем миграции (создаёт БД и заливает начальный контент)
python manage.py migrate --noinput

# Создаём суперпользователя, если задан и ещё не существует
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@fnk.bigbee.su}" 2>/dev/null \
        && echo "Суперпользователь $DJANGO_SUPERUSER_USERNAME создан" \
        || echo "Суперпользователь уже существует — пропускаем"
fi

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
