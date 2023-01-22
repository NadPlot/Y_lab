from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_db


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


def test_get_menu_list_empty():
    """
    Выдача списка меню.
    Если в БД нет меню, должен вернуть пустой список
    """

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu_not_exists():
    """
    Просмотр определенного меню.
    Если меню не найдено, возвращает сообщение 'menu not found'
    """

    response = client.get("/api/v1/menus/1001")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

def test_menu(new_menu):
    """
    Создание нового меню.
    Просмотр определенного меню.
    Выдача списка меню.
    """

    response = client.post(
        "/api/v1/menus",
        json=new_menu,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_menu["title"]
    assert data["description"] == new_menu["description"]
    assert "id" in data
    assert "submenus_count" in data
    assert "dishes_count" in data
    menu_id = data["id"]

    response = client.get(f"/api/v1/menus/{int(menu_id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_menu["title"]
    assert data["description"] == new_menu["description"]
    assert data["id"] == menu_id

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == [
        {
            f"id": {menu_id},
            "title": new_menu["title"],
            "description": new_menu["description"],
            "submenus_count": 0,
            "dishes_count": 0
        }
    ]
