FROM python:3.9-slim
RUN mkdir -p /home/kboiiz && addgroup kboiiz && useradd -d /home/kboiiz -g kboiiz kboiiz && chown kboiiz:kboiiz /home/kboiiz
USER kboiiz
WORKDIR /home/kboiiz