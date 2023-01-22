from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_menu_empty_list():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []




