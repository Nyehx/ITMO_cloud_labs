# Лабораторная №3

## Задание
* Написать “плохой” CI/CD файл, который работает, но в нем есть не менее пяти “bad practices” по написанию CI/CD.
* Написать “хороший” CI/CD, в котором эти плохие практики исправлены.
* В Readme описать каждую из плохих практик в плохом файле, почему она плохая и как в хорошем она была исправлена, как исправление повлияло на результат.

## Создание репозитория

Пусть у для этой лабораторной работы у нас есть приложение считающее кол-во делителей натурального числа(все это в некотором репозитории на гитхабе), используя `Github Actions` напишем конфигурационный `CI/CD` файл, так что при пуше новых изменений в скрипт с нашим приложением, будут проводиться юнит-тесты, строиться новый образ приложения и загружаться на `DockerHub`. 

Создадим репозиторий на гитхабе, закинем туда `factorial.py` - скрипт, `test_facorial.py` - юнит тесты для скрипта, `Dockerfile` - докерфайл для сборки образа. На скрине ниже, созданный репозиторий с перечисленными файлами

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/1.png)

Код `Dockerfile`:
```
FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 

ADD factorial.py .
```

Код `factorial.py`, который выводит факториал введенного из консоли числа:
```
import sys


def factorial(n):
    if n < 0:
        raise ValueError("Факториал не определен.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def main():
    if len(sys.argv) != 2:
        return

    try:
        n = int(sys.argv[1])
        result = factorial(n)
        print("Факториал равен " + str(result))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
```

Код `test_factorial.py`, который тестирует основную программу:

```
import unittest
from factorial import factorial


class TestFactorial(unittest.TestCase):

    def test_factorial_of_positive_numbers(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)

    def test_factorial_of_negative_numbers(self):
        with self.assertRaises(ValueError):
            factorial(-1)


if __name__ == "__main__":
    unittest.main()
```


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

1. Использование `ubuntu-latest`, т.к. версия может меняться со временем, из-за чего проект может быть нестабильным.
2. jobs `Test` и `Build-deploy` выполняются параллельно, независимо друг от друга, что непродуктивно, т.к. если не прошел шаг тестов, то не нужно записывать образ на докерхаб.
3. Тригерром workflow'а является `push` на любой ветке, таким образом, даже если мы будем иметь вторую ветку для фич, при пуше в нее изменений, наш проект задеплоиться еще раз с дефолтной ветки, что является неэффективной расстратой ресурсов.
4. Использование секретных данных в явном виде в `yml` файле, что, очевидно, небезопасно. Если кто-то получит доступ к нашему юзернейму и токену от докерхаба, то он сможет вносить изменения в ваши проекты.
5. Установка питона через `apt-get install`, поскольку такой подход не самый стабильный, некоторые версии могут не скачаться, если их нет в файле `/etc/apt/sources.list`, поэтому рекомендуется использовать `actions`. Также использование `actions` для установки питона позволяет не задумываться об ОС runner'a, что в целом упрощает написание yml файла.

### Демонстрация того, что workflow отработал и образ загрузился на докерхаб

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/6.png)

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/3.png)

## Хорошие практики

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
      - name: Check out
        uses: actions/checkout@v4
      - name: Installing python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Unit tests
        run: python3 -m unittest test_factorial.py

  Build-deploy:
    needs: Test
    runs-on: ubuntu-20.04
    steps:
      - name: Set up Docker Build
        uses: docker/setup-buildx-action@v3
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_NAME }}
          password: ${{ secrets.DOCKER_HUB_TOKEN }}
      - name: Push to docker hub
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ secrets.DOCKER_HUB_NAME }}/test_rep:latest
```

1. Здесь мы используем `runs-on: ubuntu-20.04`, а не ubuntu-latest, что повышает стабильность.
2. В job `Build-deploy` указан `needs: Test`, теперь сначала будет выполняться `Test`, а потом `Build-deploy`, что повышает продуктивность проекта.
3. Пушатся только при изменении в ветку main/
4. Вместо использования секретных данных напрямую, создадим секреты в настройке репозитория, и добавим их значения в yml файл через переменные.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/8.png)

5. Используем для установки питона actions, это гарантирует большую стабильность и универсальность.

### Проверяем загрузку на Docker Hub

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/5.png)



![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/7.png)

### Запускаем образ на машине
Вводим следующие комманды в терминал:
* `sudo docker pull cradabi/test_rep:latest`
* `sudo docker run -it cradabi/test_rep`

После этого можно спококйно запускать `factorial.app` через `python factorial.py`.
Покажем работоспособность.

![image](https://github.com/Nyehx/ITMO_cloud_labs/blob/main/DevOps/Lab_3/4.png)

Работоспособность проверена.

## Результаты

Теперь подведём итоги. 

1. Был написан "плохой" CI/CD файл. В нем были использованы 5 "плохих" практик. Все "плохие" практики описаны.
2. Был написан "хороший" CI/CD файл. В нем были исправлены возникшие ранее "плохие" практики. Так же мы описали каждое решение, и как оно повлияет на само решение.

## Работу выполнили
* Буцкий Даниил
* Корчагин Роман
