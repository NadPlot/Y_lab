# Y_lab
REST API по работе с меню ресторана

## Задача:
Написать проект на FastAPI с использованием PostgreSQL в качестве БД.
В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции.

Даны 3 сущности: Меню, Подменю, Блюдо.
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
Была создана виртуальная среда и установлены пакеты:
 
fastapi   
sqlalchemy     
psycopg2-binary    
uvicorn   
python-dotenv      


Отдельно была создана БД в PostgreSQL.
Важно, чтобы до запуска приложения FastAPI (app) была создана БД,
имя которой указывается в переменной DATABASE_URL.

Таблицы в БД созданы простым способом, при первом запуске приложения FastAPI.

app/main.py

    models.Base.metadata.create_all(bind=engine)  # Создание таблиц БД

Alembic не использовала.
Для подключения к БД использовала переменную окружения, которая
хранится в файле .env, пример:
    
    DATABASE_URL=postgresql://username:password@localhost:5432/db_name.


## Запуск проекта в виртуальной среде

    (venv)$ uvicorn app.main:app --reload

API будет доступно по ссылке: http://127.0.0.1:8000/  
Документация API (Swagger UI): http://127.0.0.1:8000/docs
