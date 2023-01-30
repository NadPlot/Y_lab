from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, schemas
from app.exceptions import (
    DishExistsException,
    MenuExistsException,
    SubmenuExistsException,
)


# Просмотр определенного меню
def get_menu(db: Session, id: str):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not menu:
        raise MenuExistsException()
    result = jsonable_encoder(menu)

    submenus = db.query(models.Submenu).filter(
        models.Submenu.menu_id == id,
    ).all()
    if not submenus:
        result['submenus_count'] = 0
        result['dishes_count'] = 0
    else:
        result['submenus_count'] = len(submenus)
        for submenu in submenus:
            dishes = db.query(models.Dishes).filter(
                models.Dishes.submenu_id == submenu.id,
            ).all()
            if not dishes:
                result['dishes_count'] = 0
            else:
                result['dishes_count'] = len(dishes)
    return result


# Выдача списка меню
def get_menu_list(db: Session):
    all_menu = db.query(models.Menu).all()
    if not all_menu:
        return []
    else:
        list_menu = [get_menu(db, menu.id) for menu in all_menu]
        return list_menu


# Создание меню
def create_menu(db: Session, menu: schemas.MenuCreate):
    new_menu = models.Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    return new_menu


# Обновление меню
def update_menu(db: Session, id: str, update_menu: schemas.MenuCreate):
    db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not db_menu:
        raise MenuExistsException()
    db_menu.title = update_menu.title
    db_menu.description = update_menu.description
    db.add(db_menu)
    db.commit()
    return db_menu


# Удаление меню
def delete_menu(db: Session, id: str):
    db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    db.delete(db_menu)
    db.commit()


# Просмотр определенного подменю
def get_submenu(db: Session, menu_id: str, submenu_id: str):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id,
    ).filter(models.Submenu.id == submenu_id).first()
    if not submenu:
        raise SubmenuExistsException()
    result = jsonable_encoder(submenu)
    dishes = db.query(models.Dishes).filter(
        models.Dishes.submenu_id == submenu.id,
    ).all()
    if not dishes:
        result['dishes_count'] = 0
    else:
        result['dishes_count'] = len(dishes)
    return result


# Просмотр списка подменю
def get_submenu_list(db: Session, menu_id: str):
    all_submenu = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id,
    ).all()
    if not all_submenu:
        return []
    else:
        list_submenu = [
            get_submenu(db, menu_id, submenu.id)
            for submenu in all_submenu
        ]
        return list_submenu


# Создание подменю
def create_submenu(db: Session, menu_id: str, submenu: schemas.SubmenuCreate):
    new_submenu = models.Submenu(**submenu.dict())
    new_submenu.menu_id = menu_id
    db.add(new_submenu)
    db.commit()
    return new_submenu


# Обновление подменю
def update_submenu(db: Session, menu_id: str, submenu_id: str, update_submenu: schemas.SubmenuCreate):
    db_submenu = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id,
    ).filter(models.Submenu.id == submenu_id).first()
    if not db_submenu:
        raise SubmenuExistsException()
    else:
        db_submenu.title = update_submenu.title
        db_submenu.description = update_submenu.description
        db.add(db_submenu)
        db.commit()
    return db_submenu


# Удаление подменю
def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    db_submenu = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id,
    ).filter(models.Submenu.id == submenu_id).first()
    db.delete(db_submenu)
    db.commit()


# Просмотр определенного блюда
def get_dish(db: Session, submenu_id: str, id: str):
    dish = db.query(models.Dishes).filter(
        models.Dishes.submenu_id == submenu_id,
    ).filter(models.Dishes.id == id).first()
    if not dish:
        raise DishExistsException()
    return jsonable_encoder(dish)


# Создать блюдо
def create_dish(db: Session, submenu_id: str, dish: schemas.DishesCreate):
    new_dish = models.Dishes(**dish.dict())
    new_dish.price = round(dish.price, 2)
    new_dish.submenu_id = submenu_id
    db.add(new_dish)
    db.commit()
    return new_dish


# Обновить блюдо
def update_dish(db: Session, submenu_id: str, id: str, update_dish: schemas.DishesCreate):
    db_dish = db.query(models.Dishes).filter(
        models.Dishes.submenu_id == submenu_id,
    ).filter(models.Dishes.id == id).first()
    if not db_dish:
        raise DishExistsException()
    else:
        db_dish.title = update_dish.title
        db_dish.description = update_dish.description
        db_dish.price = round(update_dish.price, 2)
        db.add(db_dish)
        db.commit()
    return db_dish


# Просмотр списка блюд
def get_dishes_list(db: Session, submenu_id: str):
    all_dishes = db.query(models.Dishes).filter(
        models.Dishes.submenu_id == submenu_id,
    ).all()
    if not all_dishes:
        return []
    else:
        list_dishes = [
            get_dish(db, submenu_id, dish.id)
            for dish in all_dishes
        ]
        return list_dishes


# Удаление блюда
def delete_dish(db: Session, submenu_id: str, id: str):
    db_dish = db.query(models.Dishes).filter(
        models.Dishes.submenu_id == submenu_id,
    ).filter(models.Dishes.id == id).first()
    db.delete(db_dish)
    db.commit()
