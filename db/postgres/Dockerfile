FROM postgres:latest
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh
# copying data to container
COPY ./data/foi_requests.csv data/foi_requests.csv
COPY ./data/messages.csv data/messages.csv
COPY ./data/classifications.csv data/classifications.csv
COPY ./data/categories.csv data/categories.csv
COPY ./data/public_bodies.csv data/public_bodies.csv
COPY ./data/jurisdictions.csv data/jurisdictions.csv
# copying postgres config to container
COPY ./postgresql.conf etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]