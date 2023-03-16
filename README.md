## Dev Setup
We are rebuilding the containers without using the cache to make sure they are using the most recent code/data. You need to have docker installed on your system: https://docs.docker.com/get-docker/

### Working on API

1. Start the database containers(Redis and Postgres). 
```
docker compose -f db.yml down --volumes                               
docker compose -f db.yml build --no-cache 
docker compose -f db.yml  up --force-recreate -d
```
2. Go to api folder. If you havent already, create env and install packages. For example with linux:
```
python -m venv venv
source bin/activate
```

3. Run the project (while in api/api folder):
```
uvicorn main:app --reload 
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