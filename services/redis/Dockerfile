# syntax=docker/dockerfile:1

FROM redis:7.0

RUN useradd -rm -d /home/redis -s /bin/bash -u 1000 iceking

WORKDIR /home/redis

COPY --chown=1000: redis.conf .

USER 1000

CMD [ "redis-server", "./redis.conf" ]