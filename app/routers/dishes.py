import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_redis
from app.schemas import DishesBase, DishesCreate, CacheBase
from app import crud
from app.exceptions import DishExistsException


router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=['Блюда'],
)



@router.get(
    "/",
    response_model=List[DishesBase],
    name="Выдача списка блюд",
)
def get_dishes_list(menu_id: str, submenu_id: str, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    if not cache.get('dishes'):
        list_dishes = crud.get_dishes_list(db, submenu_id)
        cache.set('dishes', json.dumps(list_dishes))
        cache.expire('dishes', 300)
        return list_dishes
    else:
        return json.loads(cache.get('dishes'))


@router.get(
    "/{id}",
    response_model=DishesBase,
    name="Просмотр определенного блюда",
)
def get_dish(submenu_id: str, id: str, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    if not cache.get(id):
        dish = crud.get_dish(db, submenu_id, id)
        cache.set(id, json.dumps(dish))
        cache.expire(submenu_id, 300)
        if not dish:
            raise DishExistsException()
        return dish
    else:
        return json.loads(cache.get(id))


@router.post(
    "/",
    response_model=DishesBase,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(menu_id: str, submenu_id: str, data: DishesCreate, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    dish = crud.create_dish(db, submenu_id, data)
    cache.delete('menu', 'submenu', 'dishes')
    return crud.get_dish(db, submenu_id, dish.id)


@router.patch(
    "/{id}",
    response_model=DishesBase,
    name="Обновить блюдо",
)
def update_dish(menu_id: str, submenu_id: str, id: str, data: DishesCreate, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    dish = crud.get_dish(db, submenu_id, id)
    if not dish:
        raise DishExistsException()
    update_dish = crud.update_dish(db, submenu_id, id, data)
    cache.delete(id)
    cache.delete('dishes')
    return crud.get_dish(db, submenu_id, update_dish.id)


@router.delete(
    "/{id}",
    name="Удалить блюдо",
)
def delete_dish(menu_id: str, submenu_id: str, id: str, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    crud.delete_dish(db, submenu_id, id)
    cache.delete(id)
    cache.delete('menu', 'submenu', 'dishes')
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )
