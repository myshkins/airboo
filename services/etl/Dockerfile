# syntax=docker/dockerfile:1

FROM ghcr.io/myshkins/airboo/shared-models:latest

WORKDIR /

FROM apache/airflow:2.5.1

WORKDIR /opt/airflow

COPY --chown=1000: . .

COPY --chown=1000: --from=0 /shared_models/ dags/shared_models

RUN pip install --no-cache-dir --upgrade -r requirements.txt

USER 1000
