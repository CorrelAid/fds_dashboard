
# FDS Statistics API

```
print(str(stmt.compile(dialect=postgresql.dialect(),compile_kwargs={"literal_binds": True})))
```

```
├── Dockerfile ---------- Used for container setup
├── kn_fds_statistics_api ---------- All python code aka the package
│   ├── database.py ---------- Establishs connection to the db
│   ├── helpers.py ---------- Helpercode
│   ├── main.py ---------- Entrypoint, define routes and settings here
│   ├── models.py ---------- Automatically generated db model, see generate_model()
│   ├── queries.py ---------- All db queries
│   └── schemas.py ---------- All response schemas
├── pyproject.toml ---------- Information for poetry
└── tests ---------- TBA
    ├── __init__.py
    └── test_kn_fds_statistics_api.py
```

## Developments Tips
- FastAPI has a very good [documentation](https://fastapi.tiangolo.com/). 
 

## Sources
- https://realpython.com/python-redis/
- https://docs.sqlalchemy.org/en/14/tutorial/data.html#tutorial-working-with-data
- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://fastapi.tiangolo.com/advanced/async-sql-databases/
- https://www.tutlinks.com/fastapi-with-postgresql-crud-async/
- https://python.plainenglish.io/how-to-build-a-rest-api-endpoint-on-top-of-an-existing-legacy-database-using-fastapi-489f38feab98
- https://stackoverflow.com/questions/28788186/how-to-run-sqlacodegen
- https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker?answertab=modifieddesc#tab-top
- https://fastapi.tiangolo.com/deployment/docker/
