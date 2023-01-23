def test_get_menu_list_empty(empty_list_response):
    """
    Выдача списка меню.
    Если в БД нет меню, должен вернуть пустой список
    """
    assert empty_list_response.status_code == 200
    assert empty_list_response.json() == []


# def test_get_menu_not_exists(menu_not_found_response):
#     """
#     Просмотр определенного меню.
#     Если меню не найдено, возвращает сообщение 'menu not found'
#     """
#     assert menu_not_found_response.status_code == 404
#     assert menu_not_found_response.json() == {"detail": "menu not found"}

# def test_menu(new_menu):
#     """
#     Создание нового меню.
#     Просмотр определенного меню.
#     Выдача списка меню.
#     Удаление меню.
#     """

#     response = client.post(
#         "/api/v1/menus",
#         json=new_menu,
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["title"] == new_menu["title"]
#     assert data["description"] == new_menu["description"]
#     assert "id" in data
#     assert "submenus_count" in data
#     assert "dishes_count" in data
#     menu_id = data["id"]

#     response = client.get(f"/api/v1/menus/{int(menu_id)}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["title"] == new_menu["title"]
#     assert data["description"] == new_menu["description"]
#     assert data["id"] == menu_id

#     response = client.get("/api/v1/menus")
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             f"id": {menu_id},
#             "title": new_menu["title"],
#             "description": new_menu["description"],
#             "submenus_count": 0,
#             "dishes_count": 0
#         }
#     ]

#     response = client.delete(
#         "/api/v1/menus/{id}/"

#         )
