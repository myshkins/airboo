# syntax=docker/dockerfile:1

FROM postgis/postgis:13-3.3-alpine 

COPY create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/create-multiple-postgresql-databases.sh

EXPOSE 5432