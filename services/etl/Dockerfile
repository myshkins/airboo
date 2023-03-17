# syntax=docker/dockerfile:1

FROM ghcr.io/myshkins/airboo/shared-models:latest

WORKDIR /

FROM apache/airflow:2.5.1

WORKDIR /opt/airflow

COPY --from=0 /shared_models/ ./shared_models

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt