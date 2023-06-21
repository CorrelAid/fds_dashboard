#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
gunzip -c /data/db.gz | psql dbname --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" main
