
## Development Setup
The Repo contains python scripts to download and process initial data. If you want to work on the scripts it can make sense to set up a virtual environment. In Linux you can do this the following way.

1. Create a virtual environment and and install requirements.

    There are multiple ways to do this. One is the following:

    ```
    cd python_scripts
    python -m venv env  
    source env/bin/activate
    python -m pip install -r requirements.txt
    ```

## Project explanation
```
.
├── data 
│   └── foi_request_list.pbz2 ----------------- all foi requests requested through api
├── docker-compose.yml ----------------- Run this to only set ub dbs
├── Postgres ----------------- All files needed for building the postgres docker container
│   ├── Dockerfile
│   ├── initial_data.csv ----------------- processed intial data to be inputted in db
│   ├── init.sh ----------------- shell script executed at start up of the container
│   └── postgresql.conf ----------------- postgres config copied to container in dockerfile
├── python_scripts ----------------- all python code. used to generate and process data
│   ├── helpercode ----------------- local python package containing some helper code
│   │   ├── helpers.py
│   │   └── __init__.py
│   ├── initial_data_gen.py ----------------- downloads the whole foi request list
│   ├── initial_data_processing.py ----------------- processes downloaded data
│   └── requirements.txt
└── Redis ----------------- All files needed for building the redis docker container
    ├── Dockerfile
    └── redis.conf ----------------- redis config copied to container in dockerfile
```
## Development Tips

### Connecting to postgres

You need to have [psql](https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/) installed on your host machine. To connect to postgres inside the container, first determine the user, passsword and server. This is specified in the docker-compose.yml. If you followed the instructions to set up the server on its own, run:

Note: we started the database on port 5431!
    
```
psql postgresql://postgres:postgres@localhost:5431/main
```

Check database content:

```
SELECT * FROM foi_requests;
```

### Connecting to Redis
You can test your redis install using python and your terminal. Just be sure to have the redis package installed and then type `python`. Aferwards:
```
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')
```
### Checking logs

The logs of a container are a valuable source for troubleshooting. To access them, run:
    ```
    docker logs postgres
    ```


## Sources
- https://dev.to/andre347/how-to-easily-create-a-postgres-database-in-docker-4moj
- https://stackoverflow.com/questions/38713597/create-table-in-postgresql-docker-image
- https://graspingtech.com/docker-compose-postgresql/
- https://www.youtube.com/watch?v=krSgKN-5DHs
