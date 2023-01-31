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
*● У меню есть подменю, которые к ней привязаны.*
*● У подменю есть блюда.*

Условия:

*● Блюдо не может быть привязано напрямую к меню, минуя подменю.*
*● Блюдо не может находиться в 2-х подменю одновременно.*
*● Подменю не может находиться в 2-х меню одновременно.*
*● Если удалить меню, должны удалиться все подменю и блюда этого меню.*
*● Если удалить подменю, должны удалиться все блюда этого подменю.*
*● Цены блюд выводить с округлением до 2 знаков после запятой.*
*● Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.*
*● Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.*
*● Во время запуска тестового сценария БД должна быть пуста.*


ВАЖНО: переписала models.py (id: int -> id: UUID)

Нужен файл .env для запуска

## Сборка и Запуск контейнера приложение FastAPI, PostgreSQL, Redis

    $ docker-compose up -d --build

API будет доступно по ссылке: http://0.0.0.0:8000/
Документация API (Swagger UI): http://0.0.0.0:8000/api/openapi
Документация в формате OpenAPI: http://0.0.0.0:8000/api/v1/openapi.json


Нужен файл .env.tests для запуска
## Сборка и запуск контейнера для тестирования приложения FastAPI

    $ docker-compose -f docker-compose.tests.yml up -d --build

Postman тесты запускала после тестов pytest

## Подключение к БД

В процессе запуска контейнера будет созданы две БД - postgres (для работы приложения)
и test (для тестов).
Таблицы в БД созданы простым способом, при первом запуске приложения FastAPI.

app/main.py

    models.Base.metadata.create_all(bind=engine)  # Создание таблиц БД

Alembic не использовала.

### Пример файла .env:

    DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    PGUSER=postgres

### Пример файла .env.tests:

    DATABASE_URL=postgresql://postgres:postgres@db:5432/test
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=test
    PGUSER=postgres
    SQLALCHEMY_SILENCE_UBER_WARNING=1

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
python-dotenv==0.21.0
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
