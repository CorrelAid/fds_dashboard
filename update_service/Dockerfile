## No cronjob so far

FROM python:3.10.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install curl libpq-dev python3-dev gcc -y \
    && curl -sSL https://install.python-poetry.org | python - --version 1.1.13 \
	&& apt-get install cron -y

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY ./ ./

COPY crontab /etc/cron.d/my-cron-file

RUN chmod +x ./kn_fds_update_service/main.py

RUN chmod 0644 /etc/cron.d/my-cron-file

RUN crontab /etc/cron.d/my-cron-file

RUN touch /var/log/cronjob.log

RUN ln -sf /proc/$$/fd/1 /var/log/cronjob.log

ENTRYPOINT ["cron", "-f"]