# Лабораторная №3*

## Задание
Сделать красиво работу с секретами. Например, поднять Hashicorp Vault (или другую секретохранилку) и сделать так, чтобы ci/cd пайплайн (или любой другой ваш сервис) ходил туда, брал секрет, использовал его не светя в логах. В Readme аргументировать почему ваш способ красивый, а также описать, почему хранение секретов в CI/CD переменных репозитория не является хорошей практикой.

## Ход работы
Я выбрал Doppler для хранения секретов, потому что он очень прост в использовании. VPN нужно включать только для регистрации. 
Сначала создадим аккаунт в `Doppler`, создадим в нем проект, добавим в конфиг 2 секрета `DOCKER_HUB_NAME` и `DOCKER_HUB_TOKEN`.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/1.png)
![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/2.png)

Теперь, чтобы получить доступ в этим секретам нам нужен `access token` допплера, который даст нам доступ к секретам, генерируем:

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/3.png)

Создаем секрет с этим токеном в репозитории

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3_2/4.png)

Видоизмененный файл пайплайна указан ниже:

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

## Почему хранения секретов в репозитории - плохая практика?
Малая гибкость, нельзя как-то разделить по ролям, окружениям, все в одной куче + если кто-то получить доступ к репозиторию, то сможет через workflow файл получить все чувствительные данные, а если мы используем секретохранилку, то это дополнительный слой безопасности. Если проект небольшой и безопасность не особо волнует, то может быть гитхаю секретов хватит, но если проект большой с кучей секретов, то какая бы то ни было секретохранилка предложит лучшее, централизованное решение.



### Почему способ красивый?
* понятный и простой интерфейс Doppler
* легко изменить пайплайн для работы с Doppler
* автоматическое шифрование и доступ через токен, что исключает риски утечек
* возможность хранить все секреты в одном месте, где их легко изменять/обновлять


### Почему хранение секретов в CI/CD переменных репозитория - плохая практика?

* риск утечек из-за открытости доступа всем, кто имеет доступ к репозиторию
* сложность работы с секретами в переменных при возрастании масштаба проекта

## Результаты

Был создан проект с секретами в Doppler и использован в нашем проекте для хранения секретов безопасно.

## Работу выполнили
* Буцкий Даниил
* Корчагин Роман
