# Y_lab
REST API для прил МЕНЮ

## Задача:
Написать REST API для Меню и реализовать методы CRUD.

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
