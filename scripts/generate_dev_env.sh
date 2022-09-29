#!/bin/bash

echo "creating a TEST .dev.env with default development values ...\n"

echo "WARNING: do not use this in production\n"

cat > .dev.env << EOF
DEBUG=1
GHOST_ALLOWED_HOSTS="localhost,127.0.0.1"
GHOST_WEB_APP_PORT=5000
GHOST_APP_HOME="/home/app/web"
GHOST_HOME="/home/app/"
GHOST_WEB_DEV_PORT=8000
POSTGRES_DB="django-db"
POSTGRES_USER="django"
POSTGRES_PASSWORD="mysecretpassword"
POSTGRES_PORT=5432
POSTGRES_HOSTNAME="plb-app-db"
PGDATA=/var/lib/postgresql/data
EOF