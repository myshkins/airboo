# syntax=docker/dockerfile:1

FROM kboiiz/air-quality-shared-models

WORKDIR /

FROM apache/airflow:2.5.1

WORKDIR /opt/airflow

COPY --from=0 /shared_models/ ./shared_models

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt