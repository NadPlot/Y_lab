import pytest
from fastapi.testclient import TestClient
from .test_db_app import app

client = TestClient(app)


@pytest.fixture()
def clear_menus():
    response = client.get("/api/v1/menus/")
    for menu in response.json():
        client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture()
def menu_id():
    response = client.get("api/v1/menus")
    for menu in response.json():
        return menu['id']


@pytest.fixture()
def submenu_id(menu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    for submenu in response.json():
        return submenu['id']


@pytest.fixture()
def dish_id(menu_id, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    for dish in response.json():
        return dish['id']
