FROM python:3.9-alpine
RUN mkdir -p /home/kboiiz && addgroup kboiiz && useradd -d /home/kboiiz -g kboiiz kboiiz && chown kboiiz:kboiiz /home/kboiiz
USER kboiiz
WORKDIR /home/kboiiz
RUN echo helloo
COPY ./services/api/requirements.txt .
RUN python -m pip install -r requirements.txt