import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db

# При запуске тестов - подключается к БД для тестов
# БД test создается при запуске контейнера
DATABASE_URL = "postgresql://postgres:postgres@db:5432/test"


engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def clear_menus():
    response = client.get("/api/v1/menus/")
    for menu in response.json():
        client.delete(f"/api/v1/menus/{menu['id']}/")

@pytest.fixture()
def empty_list_response(clear_menus):
    return client.get("/api/v1/menus")


# @pytest.fixture
# def menu_not_found_response():
#     response = client.get("/api/v1/menus/1")
#     return client.get("/api/v1/menus/1001")


# @pytest.fixture()
# def new_menu():
# 	return {"title": "Test Menu", "description": "Test description menu"}

