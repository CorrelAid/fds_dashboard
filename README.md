## Dev Setup
We are rebuilding the containers without using the cache to make sure they are using the most recent code/data. You need to have docker installed on your system: https://docs.docker.com/get-docker/

### Working on API

1. Start the database containers(Redis and Postgres).
```
docker compose -f db.yml down --volumes
docker compose -f db.yml build --no-cache
docker compose -f db.yml  up --force-recreate -d
```
2. Install dependencies
```
poetry install --all-extras
```
3. Install Pre commit hook
```
poetry run pre-commit install
```
4. Go to api/api folder. Create the file .env:
```
POSTGRES_URL='postgresql://dagster:dagster@localhost:5435/main'
REDIS_ADR='localhost'
REDIS_PORT=6379
REDIS_EXPIRE=5

```
5. Run the project (while in api/api folder):
```
poetry run uvicorn main:app --reload
```

### Working on frontend
1. Run the api.yml docker compose file that will start the databases and the api
```
docker compose -f api.yml down --volumes
docker compose -f api.yml build --no-cache
docker compose -f api.yml  up --force-recreate -d
```
2. Go to frontend folder. If you havent already, install packages. You need node for this to work: https://nodejs.org/en/download/
```
npm install
```
3. Run the project (while in frontend folder):
```
npm run dev
```

### Notes
There are 46074 total foi requests.


res = 905+4160+13888+3743+4183+2331 = 29210
res =="": 16864

29210+16864 = 46074 --> total number of foi requests

status = 792+4+55+294+14265 = 15410
this equals foi_requests_not_resolved (whis is foi_requests - resolved, status==resolved is 30664) but not res==""

15410+30664=46074 --> total number of foi requests


select count(*) from foi_requests fr where resolution = '' and status = 'resolved' ==>> 1456

30664- 29210=1454

