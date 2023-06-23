FROM postgres:latest
# Install dos2unix utility
RUN apt-get update && apt-get install -y dos2unix
# copy init.sh to container
COPY ./init.sh docker-entrypoint-initdb.d/init.sh
RUN dos2unix /docker-entrypoint-initdb.d/init.sh
RUN sed -i -e 's/\r$//' docker-entrypoint-initdb.d/init.sh
# copying data to container
COPY ./data/db.gz data/db.gz
RUN dos2unix data/db.gz

# copying postgres config to container
COPY ./postgresql.conf etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]