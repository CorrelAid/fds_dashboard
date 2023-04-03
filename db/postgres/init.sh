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
    name VARCHAR(250)
    );
  
  COPY jurisdictions
  FROM '/data/jurisdictions.csv'
  DELIMITER ','
  CSV HEADER;

  CREATE TABLE public_bodies(
    id INT PRIMARY KEY,
    name VARCHAR(250),
    jurisdiction_id INT,
    CONSTRAINT fk_jurisdiction
      FOREIGN KEY(jurisdiction_id) 
	      REFERENCES jurisdictions(id)
        );
  
  COPY public_bodies
  FROM '/data/public_bodies.csv'
  DELIMITER ','
  CSV HEADER;


CREATE TABLE campaigns(
    id INT PRIMARY KEY,
    name VARCHAR(250),
    slug VARCHAR(30),
    start_date TIMESTAMP(6) WITHOUT TIME ZONE,
    active BOOLEAN);
  
  COPY campaigns
  FROM '/data/campaigns.csv'
  DELIMITER ','
  CSV HEADER;


  CREATE TABLE foi_requests(
    id INT PRIMARY KEY,
    jurisdiction_id INT,
    refusal_reason VARCHAR(750),
    costs DECIMAL,
    due_date TIMESTAMP(6) WITHOUT TIME ZONE,
    created_at TIMESTAMP(6) WITHOUT TIME ZONE,
    last_message TIMESTAMP(6) WITHOUT TIME ZONE,
    status VARCHAR(26),
    resolution VARCHAR(26),
    user_id INT,
    public_body_id INT,
    campaign_id INT,
    CONSTRAINT fk_public_body
      FOREIGN KEY(public_body_id) 
	      REFERENCES public_bodies(id),
    CONSTRAINT fk_jurisdiction
      FOREIGN KEY(jurisdiction_id) 
	      REFERENCES jurisdictions(id),
    CONSTRAINT fk_campaign
      FOREIGN KEY(campaign_id) 
	      REFERENCES campaigns(id)
    );
  
  COPY foi_requests
  FROM '/data/foi_requests.csv'
  DELIMITER ','
  CSV HEADER;


  CREATE TABLE messages(
    id INT PRIMARY KEY,
    foi_request_id INT,
    sent BOOLEAN,
    is_response BOOLEAN,
    is_postal BOOLEAN,
    kind VARCHAR(15),
    sender_public_body DECIMAL,
    recipient_public_body DECIMAL,
    status VARCHAR(20),
    timestamp TIMESTAMP(6) WITHOUT TIME ZONE,
    CONSTRAINT fk_foi_request
      FOREIGN KEY(foi_request_id) 
	      REFERENCES foi_requests(id)
    );

  COPY messages
  FROM '/data/messages.csv'
  DELIMITER ','
  CSV HEADER;
  COMMIT;
EOSQL