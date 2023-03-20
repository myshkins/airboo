# syntax=docker/dockerfile:1

FROM ghcr.io/myshkins/airboo/shared-models:latest

WORKDIR /

FROM python:3.10.8-slim-buster

WORKDIR /api

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

COPY --from=0 /shared_models/ ./shared_models