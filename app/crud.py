from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import models, schemas
from app.exceptions import MenuExistsException


# Просмотр определенного меню
def get_menu(db:Session, id: int):
    menu = db.query(models.Menu).filter(models.Menu.id == id).first()
    if not menu:
        raise MenuExistsException(id)
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == id).all()
    for submenu in submenus:
        dishes = db.query(models.Dishes).filter(models.Dishes.submenu_id == submenu.id).all()
    result = jsonable_encoder(menu)
    result['submenus_count'] = len(submenus)
    result['dishes_count'] = len(dishes)
    return result


# Выдача списка меню
# def get_menu_list(db: Session):
#     get_all_menu = db.query(models.Menu).all()
#     list = [jsonable_encoder(menu) for menu in get_all_menu]
#     return list
