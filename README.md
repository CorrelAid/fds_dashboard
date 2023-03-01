## Dev Setup
We are rebuilding the containers without using the cache to make sure they are using the most recent code/data. You need to have docker installed on your system: https://docs.docker.com/get-docker/

### Working on API
1. If you havent already, install packages. You need poetry for this to work: https://python-poetry.org/docs/
```
poetry install
```

2. Start the database containers(Redis and Postgres). 
```
docker compose -f db.yml down --volumes                               
docker compose -f db.yml build --no-cache 
docker compose -f db.yml  up --force-recreate
```

### Working on frontend
1. If you havent already, install packages. You need node for this to work: https://nodejs.org/en/download/
```
npm install
```
2. Run the api.yml docker compose file that will start the databases and the api
```
docker compose -f api.yml down --volumes                               
docker compose -f api.yml build --no-cache 
docker compose -f api.yml  up --force-recreate
```
3. Run the project
```
npm run dev
```