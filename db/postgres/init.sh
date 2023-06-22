#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
gunzip -c /data/db.gz | sed 's/\r$//' | psql dbname --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"



