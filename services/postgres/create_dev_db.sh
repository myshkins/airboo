#!/bin/bash

set -e
set -u

ls
echo "  Creating user and database air_quality"
psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE DATABASE air_quality;
    GRANT ALL PRIVILEGES ON DATABASE air_quality TO airflow;
EOSQL

echo " Populating database air_quality"
psql -v ON_ERROR_STOP=1 air_quality < /docker-entrypoint-initdb.d/air_quality_dev_dump.sql