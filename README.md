# Project «Foodgram» in Docker

### Продуктовый помощник. Хранит рецепты, которыми можно делиться с пользователями. Рецепты можно добавить в избранное, добавить в список покупок и сохранить в формате 'shop_list.txt'.

## Для проверки
### http://158.160.0.11/ главная страница
### http://158.160.0.11/admin админка
####   mail   - admin@mail.ru
#### password - qwerty1234


[![API for Foodgram](https://github.com/Oskalovlev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](https://github.com/Oskalovlev/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Технологии
* Python - 3.10
* Django - 4.2
* PostgreSQL - 15
* Djoser - 2.1.0
* Gunicorn - 20.1.0
* Docker - 20.10.2

  PS подробнее в requrements.txt

## Установка

### Инструкции для развертывания и запуска приложения
для Linux-систем все команды необходимо выполнять от имени администратора
  - Склонировать репозиторий
    ```sh
    git clone https://github.com/Oskalovlev/foodgram-project-react.git
    ```
  - Выполнить вход на удаленный сервер
  - Установить docker на сервер:
    ```sh
    apt install docker.io 
    ```
  - Установить docker-compose на сервер:
    ```sh
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ```
  - Локально отредактировать файл infra/nginx.conf, обязательно в строке server_name вписать IP-адрес сервера
  - Скопировать файлы docker-compose.yml и nginx.conf из директории infra на сервер:
    ```sh
    scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
    scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
    ```
  - Создать .env файл по предлагаемому ниже шаблону. Обязательно изменить значения POSTGRES_USER и POSTGRES_PASSWORD
  - Шаблон описания файла .env
    ```sh
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    ```
  - Для работы с Workflow добавить в Secrets GitHub переменные окружения для работы:
  - ```sh
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя БД postgres>
    DB_USER=<пользователь БД>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
Workflow состоит из четырёх шагов:
  - Проверка кода на соответствие PEP8
  - Сборка и публикация образа бекенда на DockerHub.
  - Автоматический деплой на удаленный сервер.
  - Отправка уведомления в телеграм-чат.
  - собрать и запустить контейнеры на сервере:
    ```bash
    docker-compose up -d --build
    ```
  - После успешной сборки выполнить следующие действия (только при первом деплое):
    * провести миграции внутри контейнеров:
    ```bash
    docker-compose exec web python manage.py migrate
    ```
    * собрать статику проекта:
    ```bash
    docker-compose exec web python manage.py collectstatic --no-input
    ```  
    * Создать суперпользователя Django, после запроса от терминала ввести логин и пароль для суперпользователя:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

### Команды для заполнения базы данными
  - Заполнить базу данными
  - Создать резервную копию данных:
    ```bash
    docker-compose exec web python manage.py dumpdata > fixtures.json
    ```
  - Остановить и удалить неиспользуемые элементы инфраструктуры Docker:
    ```bash
    docker-compose down -v --remove-orphans
    ```
## Примеры API-запросов
  *Подробные примеры запросов приведены в документации ReDoc *

### Автор 
#### Оскалов Лев
