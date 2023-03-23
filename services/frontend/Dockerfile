# syntax=docker/dockerfile:1

FROM node:19-alpine

WORKDIR /frontend

RUN npm install express --save

COPY --chown=1000: build build

COPY --chown=1000: serveApp.js .

USER 1000

ENV NODE_ENV=production
