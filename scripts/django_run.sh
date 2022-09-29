#!/bin/sh

set -e

if [[ -z $DEBUG ]]; then
    python manage.py wait_for_db
    python manage.py collectstatic --noinput
    python manage.py migrate

    gunicorn load_balancer_ws.wsgi:application --bind 0.0.0.0:$GHOST_WEB_APP_PORT
else
    python manage.py wait_for_db
    python manage.py migrate

    python manage.py runserver 0.0.0.0:$GHOST_WEB_DEV_PORT
fi