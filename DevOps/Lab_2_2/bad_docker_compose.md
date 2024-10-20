version: '3'

services:
  service1:
    image: ubuntu:latest
    command: bash -c "echo 'Hello from Service 1!'"
    restart: "no"

  service2:
    image: ubuntu:latest
    command: bash -c "echo 'Hello from Service 2!'"
    restart: "no"

  service3:
    image: ubuntu:latest
    command: bash -c "echo '${GREETING} from ${TARGET}! Secret key 123456'"
    environment:
      - GREETING='Hello'
      - TARGET='Service3'
    restart: "no"
