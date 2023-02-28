FROM python:3.9-slim
COPY ci_cd/test/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /home/github && addgroup github && useradd -d /home/github -g github github && chown github:github /home/github
USER github
WORKDIR /home/github
ENV PATH=/home/github/.local/bin:$PATH
