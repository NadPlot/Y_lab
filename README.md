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


Отдельно была создана БД: menu в PostgreSQL.
Таблицы в БД созданы простым способом, при первом запуске приложения FastAPI.
Важно, чтобы до запуска была создана БД, имя которой указывается в переменной
окружения DATABASE_URL=postgresql://postgres:postgres@localhost:5432/menu.


    models.Base.metadata.create_all(bind=engine)  # Создание таблиц БД

Alembic не использовала.
Для подключения к БД использовала переменную окружения, пример:
    
    DATABASE_URL=postgresql://user:password@localhost:5432/db_name.


## Запуск проекта в виртуальной среде

    (venv)$ uvicorn app.main:app --reload

API будет доступно по ссылке: http://127.0.0.1:8000/  
Документация API (Swagger UI): http://127.0.0.1:8000/docs
