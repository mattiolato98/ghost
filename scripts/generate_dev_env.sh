#!/bin/bash

echo "creating a TEST .dev.env with default development values ...\n"

echo "WARNING: do not use this in production\n"

cat > .dev.env << EOF
DEBUG=1
GHOST_ALLOWED_HOSTS="localhost,127.0.0.1"
GHOST_CSRF_TRUSTED_ORIGINS="http://localhost:8000"
GHOST_WEB_APP_PORT=5000
GHOST_APP_HOME="/home/app/web"
GHOST_HOME="/home/app/"
GHOST_WEB_DEV_PORT=8000
GHOST_STATIC_FILES_FOLDER="/home/app/vol/static"
GHOST_MEDIA_FILES_FOLDER="/home/app/vol/media"
GHOST_APP_WEB_NAME="ghost-app-web-dev"
GHOST_APP_CELERY_NAME="ghost-app-celery-dev"
GHOST_APP_CELERY_BEAT_NAME="ghost-app-celery-beat-dev"
POSTGRES_DB="django-db"
POSTGRES_USER="django"
POSTGRES_PASSWORD="mysecretpassword"
POSTGRES_PORT=5432
POSTGRES_HOSTNAME="ghost-app-db"
PGDATA=/var/lib/postgresql/data
GHOST_REDIS_HOSTNAME="ghost-app-redis"
GHOST_APP_IMAGE="ghost-app"
EOF