FROM python:3.10.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install curl libpq-dev python3-dev gcc -y \
    && curl -sSL https://install.python-poetry.org | python - --version 1.1.13

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY ./ ./

CMD [ "poetry", "run", "start" ]