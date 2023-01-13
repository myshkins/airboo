# syntax=docker/dockerfile:1

FROM apache/airflow:2.4.3

WORKDIR /opt/airflow

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
