# syntax=docker/dockerfile:1

FROM ghcr.io/myshkins/airboo/shared-models:latest


WORKDIR /

FROM python:3.10.8-slim-buster

RUN useradd -rm -d /home/api -s /bin/bash -u 1000 iceking

WORKDIR /home/api

COPY --chown=1000: requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=1000: . .

COPY --chown=1000: --from=0 /shared_models/ ./shared_models

USER 1000
