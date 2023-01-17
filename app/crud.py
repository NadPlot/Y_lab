from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import models, schemas
from app.exceptions import MenuExistsException


# Просмотр определенного меню
def get_menu(db: Session, id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not menu:
        raise MenuExistsException(id)
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
