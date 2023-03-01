#!/bin/bash
set -e
export PGPASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB"<<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASS';
  ALTER USER $APP_DB_USER WITH SUPERUSER;
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
  \connect $APP_DB_NAME $APP_DB_USER
  BEGIN;

  CREATE TABLE jurisdictions(
    id INT PRIMARY KEY,
    name VARCHAR(250),
    rank INT);
  
  COPY jurisdictions
  FROM '/data/jurisdictions.csv'
  DELIMITER ','
  CSV HEADER;
	
  CREATE TABLE public_bodies(
    id INT PRIMARY KEY,
    name VARCHAR(250),
    classification INT ,
    categories INT,
    address VARCHAR(500),
    jurisdiction INT);
  
  COPY public_bodies
  FROM '/data/public_bodies.csv'
  DELIMITER ','
  CSV HEADER;
  
  CREATE TABLE foi_requests(
    id INT PRIMARY KEY,
    jurisdiction VARCHAR(100),
    refusal_reason VARCHAR(750),
    costs DECIMAL,
    due_date TIMESTAMP(6) WITHOUT TIME ZONE,
    resolved_on TIMESTAMP(6) WITHOUT TIME ZONE,
    first_message TIMESTAMP(6) WITHOUT TIME ZONE,
    last_message TIMESTAMP(6) WITHOUT TIME ZONE,
    status VARCHAR(26),
    resolution VARCHAR(26),
    user_id DECIMAL,
    public_body_id DECIMAL
    );
  
  COPY foi_requests(id, jurisdiction, refusal_reason, costs, due_date, resolved_on, first_message, last_message, status, resolution, user_id, public_body_id)
  FROM '/data/foi_requests.csv'
  DELIMITER ','
  CSV HEADER;
  
  CREATE TABLE messages(
    id INT PRIMARY KEY,
    request INT,
    sent BOOLEAN,
    is_response BOOLEAN,
    is_postal BOOLEAN,
    kind VARCHAR(15),
    sender_public_body DECIMAL,
    recipient_public_body DECIMAL,
    status VARCHAR(20),
    timestamp TIMESTAMP(6) WITHOUT TIME ZONE
    );

  COPY messages
  FROM '/data/messages.csv'
  DELIMITER ','
  CSV HEADER;
  COMMIT;
EOSQL