# Лабораторная №3*

## Задание
Сделать красиво работу с секретами. Например, поднять Hashicorp Vault (или другую секретохранилку) и сделать так, чтобы ci/cd пайплайн (или любой другой ваш сервис) ходил туда, брал секрет, использовал его не светя в логах. В Readme аргументировать почему ваш способ красивый, а также описать, почему хранение секретов в CI/CD переменных репозитория не является хорошей практикой.

## Выбор ПО для управления секретами

Выбор пал на `Doppler`, поскольку он прост в освоении и работает в РФ (только зарегаться надо с впн).

## Ход работы

Сначала создадим аккаунт в Doppler, создадим в нем проект (окружение `CI_CD` с конфигом `cd`), добавим в конфиг 2 секрета `DOCKER_HUB_NAME` и `DOCKER_HUB_TOKEN` (для контекста: в 3 лабе мой CI/CD пайплан заключался в том, что скрипт на питоне проходит пару тестов на раннере и при успешном прохождении с ним создается образ контейнера, который загружается в докер хаб).

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/1.png)
![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/2.png)

Теперь, чтобы получить доступ в этим секретам нам нужен `service token` допплера, который даст нам доступ к конфигу `cd`, генерируем:

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/3.png)

Создаем секрет с этим токеном в репозитории

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/4.png)

Осталось только немного изменить yaml файл пайплайна. (Здесть только 2-я джоба, т.к. 1-я без изменений)

```
name: CI/CD pipeline
run-name: Building and deploying factorial app
on:
  push:
    branches:
    - main

jobs:
  Test:
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: python3 -m unittest test_factorial.py

  Build-deploy:
    needs: Test
    runs-on: ubuntu-20.04
    steps:
      - uses: docker/setup-buildx-action@v3
      - uses: dopplerhq/cli-action@v3
      - run: |
          echo ${{ secrets.DOPPLER_TOKEN }} | doppler configure set token --scope /
          echo "DOCKER_HUB_NAME=$(doppler secrets get DOCKER_HUB_NAME --plain)" >> $GITHUB_ENV
          echo "DOCKER_HUB_TOKEN=$(doppler secrets get DOCKER_HUB_TOKEN --plain)" >> $GITHUB_ENV
      - uses: docker/login-action@v3
        with:
          username: ${{ env.DOCKER_HUB_NAME }}
          password: ${{ env.DOCKER_HUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ env.DOCKER_HUB_NAME }}/test_rep:latest
```

Что изменили: здесь мы с помощью action ставим допплер на раннер, логинимся через токен допплера и секреты из допплера переносим в переменные окружения раннера, используем их чтобы запушить образ со скриптом.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/5.png)

Как видим, пайплайн успешно отработал и образ успешно запушился

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/6.png)


### Запускаем образ на машине
Вводим следующие комманды в терминал:
* `sudo docker pull cradabi/test_rep:latest`
* `sudo docker run -it cradabi/test_rep`

После этого можно спококйно запускать `factorial.app` через `python factorial.py`.
Покажем работоспособность.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/7.png)

Работоспособность проверена.

## Аргументы
### Почему способ красивый?
Максимально понятный и простой интерфейс Doppler'a, понятная документация Doppler CLI. Создаем в допплере секреты и токен, в yaml файле дописываем несколько строчек и добавляем один секрет в репозиторий, ctrl+c -> ctrl+v несколько раз - всё.

### Почему хранения секретов в репозитории - плохая практика?
Малая гибкость, нельзя как-то разделить по ролям, окружениям, все в одной куче + если кто-то получить доступ к репозиторию, то сможет через workflow файл получить все чувствительные данные, а если мы используем секретохранилку, то это дополнительный слой безопасности. Если проект небольшой и безопасность не особо волнует, то может быть гитхаю секретов хватит, но если проект большой с кучей секретов, то какая бы то ни было секретохранилка предложит лучшее, централизованное решение.

## Результаты

Был создан проект с секретами в Doppler и использован в нашем проекте для хранения секретов безопасно.

## Работу выполнили
* Буцкий Даниил
* Корчагин Роман
