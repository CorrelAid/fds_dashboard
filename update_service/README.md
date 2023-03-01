Find general information about the project this repo belons to [here](https://pad.correlaid.org/s/BkDPVFUN9)

# FDS Statistics Dashboard Update Service

## Suggestions for Update Script

- Run a db query that outputs the latest foi request (by last message)
- Run a api request that download all foi requests till that latest foi request
- we need a way to keep the docker container running while the script doesnt execute


## Development Setup

This repo contains a script that updates the data in the statistics database. It requests FOI requests using the FDS API and can run in a docker container, where it will be executed regularily using a cronjob.

To develop the script on its own, follow the script only instructions. To let the script run in the docker container, follow the docker setup instructions.

### Script only

1. As the script updates the statistics DB, you need to start it first.

    Follow [this](https://github.com/CorrelAid/kn_fds_statistics_database), but set up the databases on their own.

2. Install poetry, which is used for dependency management.
    
    Follow the [official instructions](https://python-poetry.org/docs/)

3. Install requirements

    ```
    poetry install
    ```

4. Create .env file
    The database credentials are provided in evironment variables.  

    ```
    echo "POSTGRES_URL='postgresql://api:1234@localhost:5432/main' > .env " 
    ```

4. Run app
    ```
    poetry run start
    ```

### Docker Setup

1. Install Docker

    Follow the [offical instructions](https://docs.docker.com/get-docker/). For Docker Compose, take a look [here](https://docs.docker.com/compose/install/).


2. Create local container registry

    A local container registry needs to be set up and running. Follow [these instructions](https://github.com/CorrelAid/kn_fds_infra).

3. Create .env file
    The database credentials are provided in an evironment variable.  

    ```
    echo "POSTGRES_URL='postgresql://api:1234@postgres:5432/main'" > .env 
    ```

4. Build and tag image

    ```
    docker build -t localhost:5000/kn_fds_update_service:latest .
    ```

5. Push the image to the local registry
    ```
    docker push localhost:5000/kn_fds_update_service:latest
    ```

6. Use the docker compose file provided in a separate repo to set up all infrastructure of this project.

    Follow [these instructions](https://github.com/CorrelAid/kn_fds_infra)



## Sources
- https://blog.thesparktree.com/cron-in-docker
- https://himbat.ngontinh24.com/article/kickstart-your-next-python-project-with-with-poetry-pre-commit-and-github-actions
- https://python-poetry.org/docs/master/basic-usage/
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker?answertab=modifieddesc#tab-top
- https://jackmckew.dev/packaging-python-packages-with-poetry.html
- https://nschdr.medium.com/running-scheduled-python-tasks-in-a-docker-container-bf9ea2e8a66c