# 3 Лаба по Devops

## Введение

Пусть у для этой лабораторной работы у нас есть приложение считающее кол-во делителей натурального числа(все это в некотором репозитории на гитхабе), используя `Github Actions` напишем конфигурационный `CI/CD` файл, так что при пуше новых изменений в скрипт с нашим приложением, будут проводиться юнит-тесты, строиться новый образ приложения и загружаться на `DockerHub`. 

Создадим репозиторий на гитхабе, закинем туда `factorial.py` - скрипт, `test_facorial.py` - юнит тесты для скрипта, `Dockerfile` - докерфайл для сборки образа. На скрине ниже, созданный репозиторий с перечисленными файлами

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/1.png)

## Плохие практики 

В папке `.github/workflows` создадим файл `bad_practice.yml`.

```
name: CI/CD pipeline
run-name: Building and deploying factorial app
on: push
jobs:
  Test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          sudo apt-get update
          sudo apt-get install -y python3
      - run: |
          python3 -m unittest test_factorial.py
          
  Build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: cradabi
          password: dckr_pat_VlJCbMcxabcRjLpZ69y-6x1zqHM
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: cradabi/test_rep:latest
```

1. Использование `ubuntu-latest`, т.к. версия может меняться со временем, из=за чего может пострадать стабильность.
2. Отсутствие наименований шагов, без них сложнее сразу понять, за что отвечает тот или иной шаг. 
3. jobs `Test` и `Build-deploy` выполняются параллельно, независимо друг от друга, что нелогично, поскольку если тесты не пройдены, то нет смысла деплоить приложение, а в данной реализации, образ создасться и загрузиться на докерхаб независимо были ли тесты пройдены успешно или нет.
4. Тригерром workflow'а является `push` на любой ветке, таким образом, даже если мы будем иметь вторую ветку для фич, при пуше в нее изменений, наш проект задеплоиться еще раз с дефолтной ветки (т.е. просто лишнее действие).
5. Использование секретных данных в явном виде в `yml` файле, что, очевидно, небезопасно. Если кто-то получит доступ к нашему юзернейму и токену от докерхаба, то он сможет вносить изменения (в зависимости от того, какой токен), которые должны быть доступны только нам.
6. Установка питона через `apt-get install`, поскольку такой подход не самый стабильный, некоторые версии могут не подтянуться, если их нет в файле `/etc/apt/sources.list`, поэтому рекомендуется использовать `actions`. Также использование `actions` для установки питона позволяет не задумываться об ОС runner'a, что в целом упрощает написание yml файла.

### Демонстрация того, что workflow отработал и образ загрузился на докерхаб

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/6.png)

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/3.png)

## Исправление плохих практик

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
      - name: Check out repository code
        uses: actions/checkout@v4
      - name: Installing python on a runner server
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Unit testing
        run: python3 -m unittest test_factorial.py

  Build-deploy:
    needs: Test
    runs-on: ubuntu-20.04
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_NAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}
      - name: Build and push docker
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ secrets.DOCKER_HUB_NAME }}/test_rep:latest
```

1. Здесь мы используем `runs-on: ubuntu-20.04`, что повышает стабильность.
2. К каждому шагу добавили `name:`, код стал более читаем и понятен.
3. В job `Build-deploy` указан `needs: Test`, теперь сначала будет выполняться `Test`, а потом `Build-deploy`
4. Указан тригерром пуш на главной(main) ветке.
5. Вместо использования секретных данных напрямую, создадим секреты в настройке репозитория, и добавим их значения в yml файл через переменные.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/8.png)

6. Используем для установки питона actions, это гарантирует большую стабильность и универсальность.

### Тестируем работу

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/5.png)



![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/7.png)

С помощью `docker pull cradabi/test_rep:latest` загружаю с докерхаба образ себе на комп. и проверяем работу

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/4.png)

Как видим, все работает.

## Итоги

В процессе выполнения лабораторной работы было определено 5 плохих практик по написанию CI/CD файла для Github Actions. Все они в дальнейшем были исправлены.
