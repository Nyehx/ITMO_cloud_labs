# Лабораторная №2_*

## Задание
- Написать “плохой” Docker Compose файл, в котором есть не менее трех “bad practices” по их написанию.
- Написать “хороший” Docker Compose файл, в котором эти плохие практики исправлены.
- В Readme описать каждую из плохих практик в плохом файле, почему она плохая и как в хорошем она была исправлена, как исправление повлияло на результат.
- После предыдущих пунктов в хорошем файле настроить сервисы так, чтобы контейнеры в рамках этого compose-проекта так же поднимались вместе, но не "видели" друг друга по сети. В отчете описать, как этого добились и кратко объяснить принцип такой изоляции.

## Установка Docker Compose
Первым делом устанавливаем Docker на операционную систему. В нашем случае это Linux, а именно AstraLinux:2.12.46, запущенная через VirtualBox. Для того чтобы установить Docker, нужно открыть терминал ввести команды:
* sudo apt update
* sudo apt install docker-compose

## Написание Docker-Compose file

Для того, чтобы запустить докеры, нужно ввести следующие команды в нужных директориях:

* sudo docker-compose up .

Покажем, что наши контейнеры на самом деле работают, и выыполняют то, что написано в bash.md.

```
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
```

![net](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_2_2/1.png)

```
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
```

![net](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_2_2/2.png)

Успешно собран и запущен плохой и хороший контейнеры.

### Плохой Dockerfile

Сначала опишем, какие "плохие практики" были использованы при первоначальном написании докерфайла.

1. Первая "плохая практика" заключается в использовании "latest" для образов

* Использование образа ubuntu:latest может привести к непредсказуемым изменениям в работе приложения при обновлениях образа.

В данном примере в качестве базового образа для докера используется ubuntu последней версии. Последняя версия может измениться, и написанный докерфайл может перестать работать в более новых версиях.

2. Вторая "плохая практика" заключается в том, что мы жустко указываем секретный код в docker-compose файле.
* В service3 происходит жесткое кодирование строки Secret Key: 123456, что делает приложение уязвимым.
Каждый может посмотреть пароль.

3. Третья "плохая практика" - Прямая инициализация переменных

 * Переменные инициализируются напрямую а не в окружении.
  
4. Четвертая "плохая практика" - Отсутствие директив для перезапуска

 * Указание restart: no не позволяет контейнерам автоматически перезапуститься в случае сбоя


### Хороший Dockerfile

По порядку опишем, какие решения были приняты для исправления ошибок. Так же опишем, как исправление ошибок повлияло на реузльтат.

1. Укажем конкретную версию.

* image: ubuntu:20.04

Независимо от внешних источников, Docker всегда будет запускаться одинаково и будет стабилен через некторое время - это "хорошая практика".

2. Использование переменных окружения для секретных ключей:
* В service3 переменная SECRET_KEY теперь передается через переменные окружения, а не жестко закодирована. Это повышает безопасность.

3. Корректная передача переменных окружения:
* Переменные GREETING и TARGET передаются в service3 через переменные окружения, что гарантирует, что они будут инициализированы при выполнении.

4. Политики перезапуска:
* Добавлены директивы restart: unless-stopped для всех сервисов, что обеспечивает автоматический перезапуск контейнеров в случае сбоев.

  
 ## Сетевая настройка Docker Compose проекта
В Docker Compose файле добавим блок с объявлением сетей `networks:`. Кроме этого, подключим сервисы к разным сетям (`network1`,  `network2` и `network3`), теперь они изолированы друг от друга.
```
version: '3.3'

services:
  service1:
    image: ubuntu:20.04
    command: bash -c "echo 'Hello from Service 1!'"
    restart: "unless-stopped"
    networks:
      - network1

  service2:
    image: ubuntu:20.04
    command: bash -c "echo 'Hello from Service 2!'"
    restart: "unless-stopped"
    networks:
      - network2

  service3:
    image: ubuntu:20.04
    command: bash -c "echo '${GREETING} from ${TARGET}! Secret Key ${SECRET_KEY}'"
    environment:
      - GREETING=${GREETING}
      - TARGET=${TARGET}
      - SECRET_KEY=${SECRET_KEY}
    restart: "unless-stopped"
    networks:
      - network3



networks:
  network1:
    driver: bridge
  network2:
    driver: bridge
  network3:
    driver: bridge
```


## Результаты

Теперь подведём небольшие итоги. 

1. Был написан "плохой" докерфайл. В нем были использованы 3 "плохих" практики. Все 3 "плохие" практики описаны.
2. Был написан "хороший" докерфайл. В нем были исправлены возникшие ранее "плохие" практики. Так же мы описали каждое решение, и как оно повлияет на сам Docker.
3. Мы описали 4 "плохие" практики при работе с контейнерами.

## Работу выполнили
* Буцкий Даниил
* Корчагин Роман
