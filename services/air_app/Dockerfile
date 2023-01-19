# syntax=docker/dockerfile:1

FROM python:3.10.8-slim-buster

WORKDIR /air_app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .