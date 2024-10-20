FROM ubuntu:20.04

RUN useradd -m myuser
USER myuser

COPY start.sh /app/start.sh

CMD ["bash", "/app/start.sh"]
