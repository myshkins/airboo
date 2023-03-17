FROM python:3.9-slim

RUN mkdir -p /home/github && addgroup github && useradd -d /home/github -g github github && chown github:github /home/github

USER github

WORKDIR /home/github

ENV PATH=/github/home/.local/bin:$PATH