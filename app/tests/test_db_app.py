from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app
from app.dependencies import get_db

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

test_id = 'f7ec56be-f27b-4603-8416-03667696d6c6'

def test_get_menu_list_empty(clear_menus):
    """
    Выдача списка меню.
    Нет меню
    """
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu_not_exists(clear_menus):
    """
    Просмотр определенного меню.
    Не найдено меню
    """
    response = client.get(f"/api/v1/menus/{test_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}


def test_get_submenu_list_empty(clear_menus):
    """
    Выдача списка подменю.
    Нет подменю
    """
    response = client.get(f"/api/v1/menus/{test_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_get_submenu_not_exists(clear_menus):
    """
    Просмотр определенного подменю.
    Не найдено подменю
    """
    response = client.get(f"/api/v1/menus/{test_id}/submenus/{test_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_get_dish_list_empty(clear_menus):
    """
    Просмотр списка блюд.
    Не найдено блюд
    """
    response = client.get(f"/api/v1/menus/{test_id}/submenus/{test_id}/dishes")
    assert response.status_code == 200
    assert response.json() == []


def test_get_dish_not_exists(clear_menus):
    """
    Просмотр определенного блюда.
    Не найдено блюдо
    """
    response = client.get(f"/api/v1/menus/{test_id}/submenus/{test_id}/dishes/{test_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_add_menu(clear_menus):
    """
    Создание нового меню.
    """
    data = {"title": "Test Menu", "description": "Test description menu"}
    response = client.post("/api/v1/menus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_get_menu(menu_id):
    """
    Просмотр определенного меню.
    """
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    menu = response.json()
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_update_menu(menu_id):
    """
    Обновить меню.
    """
    data = {"title": "Test Update Menu", "description": "Test Update description menu"}
    response = client.patch(f"/api/v1/menus/{menu_id}/", json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_add_submenu(menu_id):
    """
    Создание нового подменю.
    """
    data = {"title": "Test Submenu", "description": "Test description Submenu"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "dishes_count" in menu


def test_get_sub_menu(menu_id, submenu_id):
    """
    Просмотр определенного подменю.
    """
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert response.status_code == 200
    menu = response.json()
    assert "dishes_count" in menu


def test_update_submenu(menu_id, submenu_id):
    """
    Обновить подменю.
    """
    data = {"title": "Test Update Submenu", "description": "Test Update description Submenu"}
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/", json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "dishes_count" in menu



def test_add_dish(menu_id, submenu_id):
    """
    Создание нового блюда.
    """
    data = {"title": "Test Dish", "description": "Test description Dish", "price": "12.551"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=data)
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_update_dish(menu_id, submenu_id, dish_id):
    """
    Обновить блюдо.
    """
    data = {"title": "Test Update Dish", "description": "Test Update description Dish", "price": "12.4421"}
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=data)
    assert response.status_code == 200
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_get_menu_list(menu_id):
    """
    Выдача списка меню.
    """
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{menu_id}",
            "title": "Test Update Menu",
            "description": "Test Update description menu",
            "submenus_count": 1,
            "dishes_count": 1
        }
    ]


def test_get_submenu_list(menu_id, submenu_id):
    """
    Выдача списка подменю.
    """
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{submenu_id}",
            "title": "Test Update Submenu",
            "description": "Test Update description Submenu",
            "dishes_count": 1
        }
    ]


def test_get_dish_list(menu_id, submenu_id, dish_id):
    """
    Просмотр списка блюд.
    """
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{dish_id}",
            "title": "Test Update Dish",
            "description": "Test Update description Dish",
            "price": "12.44"
        }
    ]


def test_delete_dish(menu_id, submenu_id, dish_id):
    """
    Удалить блюдо.
    """
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "The dish has been deleted"}


def test_delete_submenu(menu_id, submenu_id):
    """
    Удалить подменю.
    """
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "The submenu has been deleted"}


def test_delete_menu(menu_id):
    """
    Удалить меню.
    """
    response = client.delete(f"/api/v1/menus/{menu_id}/")
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "The menu has been deleted"}



