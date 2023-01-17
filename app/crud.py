from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import models, schemas
from app.exceptions import MenuExistsException, SubmenuExistsException


# Просмотр определенного меню
def get_menu(db: Session, id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not menu:
        raise MenuExistsException()
    result = jsonable_encoder(menu)

    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == id).all()
    if not submenus:
        result['submenus_count'] = 0
        result['dishes_count'] = 0
    else:
        result['submenus_count'] = len(submenus)
        for submenu in submenus:
            dishes = db.query(models.Dishes).filter(models.Dishes.submenu_id == submenu.id).all()
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
def update_menu(db: Session, id: int, update_menu: schemas.MenuCreate):
    db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not db_menu:
        raise MenuExistsException()
    db_menu.title = update_menu.title
    db_menu.description = update_menu.description
    db.add(db_menu)
    db.commit()
    return db_menu


# Удаление меню
def delete_menu(db: Session, id: int):
    db_menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    db.delete(db_menu)
    db.commit()


# Просмотр определенного подменю
def get_submenu(db: Session, menu_id: int, submenu_id: int):
    submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).filter(models.Submenu.id == submenu_id).first()
    if not submenu:
        raise SubmenuExistsException()
    result = jsonable_encoder(submenu)
    dishes = db.query(models.Dishes).filter(models.Dishes.submenu_id == submenu.id).all()
    if not dishes:
        result['dishes_count'] = 0
    else:
        result['dishes_count'] = len(dishes)
    return result


# Выдача списка подменю
def get_submenu_list(db: Session, menu_id: int):
    all_submenu = db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
    if not all_submenu:
        return []
    else:
        list_submenu = [get_submenu(db, menu.id) for menu in all_submenu]
        return list_submenu
