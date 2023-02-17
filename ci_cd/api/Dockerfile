FROM python:3.9-slim
RUN mkdir -p /home/github && addgroup github && useradd -d /home/github -g github github && chown github:github /home/github
USER github
WORKDIR /home/github
ENV PATH=/home/github/.local/bin:$PATH
COPY ./services/api/requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt