version: '3.3'

services:
  service1:
    image: ubuntu:20.04
    command: bash -c "echo 'Hello from Service 1!'"
    restart: "unless-stopped"

  service2:
    image: ubuntu:20.04
    command: bash -c "echo 'Hello from Service 2!'"
    restart: "unless-stopped"

  service3:
    image: ubuntu:20.04
    command: bash -c "echo '${GREETING} from ${TARGET}! Secret Key ${SECRET_KEY}'"
    environment:
      - GREETING=${GREETING}
      - TARGET=${TARGET}
      - SECRET_KEY=${SECRET_KEY}
    restart: "unless-stopped"
