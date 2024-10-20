FROM ubuntu:latest

USER root

COPY . /app

CMD ["bash", "/app/start.sh"]
