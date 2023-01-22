from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_menu_list_empty():
    """Выдача списка меню. Если в БД нет меню, должен вернуть пустой список"""
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu_not_exists():
    """Просмотр определенного меню. Если меню не найдено, возвращает сообщение 'menu not found'"""
    response = client.get("/api/v1/menus/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
