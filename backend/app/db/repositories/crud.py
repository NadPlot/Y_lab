from app.db.repositories.base import BaseRepository
from app.models.schemas import MenuCreate, MenuRead



class MenuRepository(BaseRepository):
    """"
    All database actions associated with the Menu
    Посмотри как было в стажировке объявление моделей, metadata
    """

    async def create_menu(self, *, new_menu: MenuCreate) -> MenuRead:
        query = '11'
        values = new_menu.dict()
        new_menu = await self.db.execute(query=query, values=values)

        return MenuRead(**new_menu)


# import json

# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.orm import Session

# from app import models, schemas
# from app.cache import CacheBase
# from app.exceptions import (
#     DishExistsException,
#     MenuExistsException,
#     SubmenuExistsException,
# )


# # Просмотр определенного меню
# def get_menu(db: Session, id: str, cache: CacheBase):
#     if not cache.get(id):
#         menu = db.query(models.Menu).filter(models.Menu.id == id).first()
#         if not menu:
#             raise MenuExistsException()
#         result = jsonable_encoder(menu)

#         submenus = db.query(models.Submenu).filter(
#             models.Submenu.menu_id == id,
#         ).all()
#         if not submenus:
#             result['submenus_count'] = '0'
#             result['dishes_count'] = '0'
#         else:
#             result['submenus_count'] = len(submenus)
#             for submenu in submenus:
#                 dishes = db.query(models.Dishes).filter(
#                     models.Dishes.submenu_id == submenu.id,
#                 ).all()
#                 if not dishes:
#                     result['dishes_count'] = '0'
#                 else:
#                     result['dishes_count'] = len(dishes)
#         cache.set(id, json.dumps(result))
#         cache.expire(id, 300)
#         return result
#     else:
#         return json.loads(cache.get(id))


# # Выдача списка меню
# def get_menu_list(db: Session, cache: CacheBase):
#     if not cache.get('menu'):
#         all_menu = db.query(models.Menu).all()
#         if not all_menu:
#             return []
#         else:
#             list_menu = [
#                 get_menu(db, str(menu.id), cache)
#                 for menu in all_menu
#             ]
#             cache.set('menu', json.dumps(list_menu))
#             cache.expire('menu', 300)
#             return list_menu
#     else:
#         return json.loads(cache.get('menu'))


# # Создание меню
# def create_menu(db: Session, menu: schemas.MenuCreate, cache: CacheBase):
#     new_menu = models.Menu(**menu.dict())
#     db.add(new_menu)
#     db.commit()
#     db.refresh(new_menu)
#     result = jsonable_encoder(new_menu)
#     result['submenus_count'] = '0'
#     result['dishes_count'] = '0'
#     cache.delete('menu')
#     return result


# # Обновление меню
# def update_menu(db: Session, id: str, update_menu: schemas.MenuCreate, cache: CacheBase):
#     db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
#     if not db_menu:
#         raise MenuExistsException()
#     db_menu.title = update_menu.title
#     db_menu.description = update_menu.description
#     db.add(db_menu)
#     db.commit()
#     db.refresh(db_menu)
#     cache.delete('menu', id)
#     return db_menu


# # Удаление меню
# def delete_menu(db: Session, id: str, cache: CacheBase):
#     db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
#     db.delete(db_menu)
#     db.commit()
#     cache.delete(id)
#     cache.delete('menu', 'submenu', 'dishes')


# # Просмотр определенного подменю
# def get_submenu(db: Session, menu_id: str, submenu_id: str, cache: CacheBase):
#     if not cache.get(submenu_id):
#         submenu = db.query(models.Submenu).filter(
#             models.Submenu.menu_id == menu_id,
#         ).filter(models.Submenu.id == submenu_id).first()
#         if not submenu:
#             raise SubmenuExistsException()
#         result = jsonable_encoder(submenu)
#         dishes = db.query(models.Dishes).filter(
#             models.Dishes.submenu_id == submenu.id,
#         ).all()
#         if not dishes:
#             result['dishes_count'] = '0'
#         else:
#             result['dishes_count'] = len(dishes)
#         cache.set(submenu_id, json.dumps(result))
#         cache.expire(submenu_id, 300)
#         return result
#     else:
#         return json.loads(cache.get(submenu_id))


# # Просмотр списка подменю
# def get_submenu_list(db: Session, menu_id: str, cache: CacheBase):
#     if not cache.get('submenu'):
#         all_submenu = db.query(models.Submenu).filter(
#             models.Submenu.menu_id == menu_id,
#         ).all()
#         if not all_submenu:
#             return []
#         else:
#             list_submenu = [
#                 get_submenu(db, menu_id, str(submenu.id), cache)
#                 for submenu in all_submenu
#             ]
#             cache.set('submenu', json.dumps(list_submenu))
#             cache.expire('submenu', 300)
#             return list_submenu
#     else:
#         return json.loads(cache.get('submenu'))


# # Создание подменю
# def create_submenu(db: Session, menu_id: str, submenu: schemas.SubmenuCreate, cache: CacheBase):
#     new_submenu = models.Submenu(**submenu.dict())
#     new_submenu.menu_id = menu_id
#     db.add(new_submenu)
#     db.commit()
#     db.refresh(new_submenu)
#     result = jsonable_encoder(new_submenu)
#     result['dishes_count'] = '0'
#     cache.delete('menu', 'submenu')
#     return result


# # Обновление подменю
# def update_submenu(db: Session, menu_id: str, submenu_id: str, update_submenu: schemas.SubmenuCreate, cache: CacheBase):
#     db_submenu = db.query(models.Submenu).filter(
#         models.Submenu.menu_id == menu_id,
#     ).filter(models.Submenu.id == submenu_id).first()
#     if not db_submenu:
#         raise SubmenuExistsException()
#     else:
#         db_submenu.title = update_submenu.title
#         db_submenu.description = update_submenu.description
#         db.add(db_submenu)
#         db.commit()
#         db.refresh(db_submenu)
#         cache.delete('submenu', submenu_id)
#     return db_submenu


# # Удаление подменю
# def delete_submenu(db: Session, menu_id: str, submenu_id: str, cache: CacheBase):
#     db_submenu = db.query(models.Submenu).filter(
#         models.Submenu.menu_id == menu_id,
#     ).filter(models.Submenu.id == submenu_id).first()
#     db.delete(db_submenu)
#     db.commit()
#     cache.delete(menu_id, submenu_id)
#     cache.delete('menu', 'submenu', 'dishes')


# # Просмотр определенного блюда
# def get_dish(db: Session, submenu_id: str, dish_id: str, cache: CacheBase):
#     if not cache.get(dish_id):
#         dish = db.query(models.Dishes).filter(
#             models.Dishes.submenu_id == submenu_id,
#         ).filter(models.Dishes.id == dish_id).first()
#         if not dish:
#             raise DishExistsException()
#         result = jsonable_encoder(dish)
#         cache.set(dish_id, json.dumps(result))
#         cache.expire(dish_id, 300)
#         return dish
#     else:
#         return json.loads(cache.get(dish_id))


# # Создать блюдо
# def create_dish(db: Session, submenu_id: str, dish: schemas.DishesCreate, cache: CacheBase):
#     new_dish = models.Dishes(**dish.dict())
#     new_dish.price = round(dish.price, 2)
#     new_dish.submenu_id = submenu_id
#     db.add(new_dish)
#     db.commit()
#     db.refresh(new_dish)
#     cache.delete('menu', 'submenu', 'dishes')
#     return jsonable_encoder(new_dish)


# # Обновить блюдо
# def update_dish(db: Session, submenu_id: str, dish_id: str, update_dish: schemas.DishesCreate, cache: CacheBase):
#     db_dish = db.query(models.Dishes).filter(
#         models.Dishes.submenu_id == submenu_id,
#     ).filter(models.Dishes.id == dish_id).first()
#     if not db_dish:
#         raise DishExistsException()
#     else:
#         db_dish.title = update_dish.title
#         db_dish.description = update_dish.description
#         db_dish.price = round(update_dish.price, 2)
#         db.add(db_dish)
#         db.commit()
#         db.refresh(db_dish)
#         cache.delete('dishes', dish_id)


# # Просмотр списка блюд
# def get_dishes_list(db: Session, submenu_id: str, cache: CacheBase):
#     if not cache.get('dishes'):
#         all_dishes = db.query(models.Dishes).filter(
#             models.Dishes.submenu_id == submenu_id,
#         ).all()
#         if not all_dishes:
#             return []
#         else:
#             list_dishes = [
#                 get_dish(db, submenu_id, str(dish.id), cache)
#                 for dish in all_dishes
#             ]
#             cache.set('dishes', json.dumps(list_dishes))
#             cache.expire('dishes', 300)
#             return list_dishes
#     else:
#         return json.loads(cache.get('dishes'))


# # Удаление блюда
# def delete_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str, cache: CacheBase):
#     db_dish = db.query(models.Dishes).filter(
#         models.Dishes.submenu_id == submenu_id,
#     ).filter(models.Dishes.id == dish_id).first()
#     db.delete(db_dish)
#     db.commit()
#     cache.delete(menu_id, submenu_id, dish_id)
#     cache.delete('menu', 'submenu', 'dishes')
