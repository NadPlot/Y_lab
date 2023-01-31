# Y_lab
REST API по работе с меню ресторана

## Цель:
Написать проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции.

### Задачи:

● Обернуть проект в контейнер (Docker Compose);
● Написать CRUD тесты для API с помощью библиотеки pytest;
● Подготовить отдельный контейнер для запуска тестов;
● Вывести бизнес-логику и запросы в БД в отдельные слои приложения;
● Добавить кэш хранилище Redis
● Добавить pre-commit хуки в проект
● Описать ручки API в соответствии с OpenAPI


### Условия:
Даны 3 сущности:

Меню, Подменю, Блюдо.


Зависимости:
● У меню есть подменю, которые к ней привязаны.
● У подменю есть блюда.
Условия:
● Блюдо не может быть привязано напрямую к меню, минуя подменю.
● Блюдо не может находиться в 2-х подменю одновременно.
● Подменю не может находиться в 2-х меню одновременно.
● Если удалить меню, должны удалиться все подменю и блюда этого меню.
● Если удалить подменю, должны удалиться все блюда этого подменю.
● Цены блюд выводить с округлением до 2 знаков после запятой.
● Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
● Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
● Во время запуска тестового сценария БД должна быть пуста.

## Requirements

anyio==3.6.2
async-timeout==4.0.2
attrs==22.2.0
certifi==2022.12.7
cffi==1.15.1
click==8.1.3
cryptography==39.0.0
exceptiongroup==1.1.0
fastapi==0.89.1
greenlet==2.0.2
h11==0.14.0
httpcore==0.16.3
httpx==0.23.3
idna==3.4
iniconfig==2.0.0
packaging==23.0
pluggy==1.0.0
psycopg2-binary==2.9.5
pycparser==2.21
pydantic==1.10.4
pytest==7.2.1
redis==4.4.2
rfc3986==1.5.0
sniffio==1.3.0
SQLAlchemy==1.4.46
starlette==0.22.0
tomli==2.0.1
types-pyOpenSSL==23.0.0.2
types-redis==4.4.0.4
typing_extensions==4.4.0
uvicorn==0.20.0


ВАЖНО: переписала models.py (id: int -> id: UUID)

## Сборка и Запуск контейнера приложение FastAPI, PostgreSQL, Redis

    $ docker-compose up -d --build

API будет доступно по ссылке: http://0.0.0.0:8000/
Документация API (Swagger UI): http://0.0.0.0:8000/api/openapi
Документация в формате OpenAPI: http://0.0.0.0:8000/api/v1/openapi.json

## Сборка и запуск контейнера для тестирования приложения FastAPI
после запуска основного контейнера

    $ docker-compose -f docker-compose.tests.yml up -d --build

Посмотреть логи

    $ docker container logs test

## Подключение к БД

В процессе запуска контейнера будет созданы две БД - postgres (для работы приложения)
и test (для тестов).
Таблицы в БД созданы простым способом, при первом запуске приложения FastAPI.

app/main.py

    models.Base.metadata.create_all(bind=engine)  # Создание таблиц БД

Alembic не использовала.

### Пример файла .env:
Для запуска контейнеров и тестов не нужен.
При необходимости переменные окружения из docker-compose.yml можно вынесни в файл .env:

    DATABASE_URL=postgresql://username:password@db:5432/db_name
    POSTGRES_USER=username
    POSTGRES_PASSWORD=password
    POSTGRES_DB=db_name

Добавить в requirements.txt:

python-dotenv==0.21.0

Изменить config.py:

    import os
    from pydantic import BaseSettings, Field
    from dotenv import load_dotenv  # добавить
    load_dotenv()  # добавить

    class Settings(BaseSettings):
        db_url: str = Field(os.getenv('DATABASE_URL'))  # изменить

    settings = Settings()

Изменить в docker-compose.yml и docker-compose.tests.yml environment: на:

    env_file:
          - .env
