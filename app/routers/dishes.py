import http

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud
from app.cache import get_redis
from app.dependencies import get_db
from app.schemas import CacheBase, DishesBase, DishesCreate

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Блюда'],
)


@router.get(
    '/',
    response_model=list[DishesBase],
    name='Выдача списка блюд',
    status_code=http.HTTPStatus.OK,
)
def get_dishes_list(
    menu_id: str,
    submenu_id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Просмотр списка блюд по id меню и id подменю:

    - **menu_id**: идентификатор меню
    - **submenu_id**: идентификатор подменю
    - **title**: название блюда
    - **description**: описание блюда
    - **price**: цена блюда
    """
    return crud.get_dishes_list(db, submenu_id, cache)


@router.get(
    '/{id}',
    response_model=DishesBase,
    name='Просмотр определенного блюда',
    status_code=http.HTTPStatus.OK,
)
def get_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Просмотр определенного блюда по id меню и id подменю:

    - **menu_id**: идентификатор меню
    - **submenu_id**: идентификатор подменю
    - **id**: идентификатор блюда
    - **title**: название блюда
    - **description**: описание блюда
    - **price**: цена блюда
    """
    return crud.get_dish(db, submenu_id, dish_id, cache)


@router.post(
    '/',
    response_model=DishesBase,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(
    menu_id: str,
    submenu_id: str,
    data: DishesCreate,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Создать новое блюдо:

    - **menu_id**: идентификатор меню
    - **submenu_id**: идентификатор подменю
    - **title**: название блюда
    - **description**: описание блюда
    - **price**: цена блюда
    """
    return crud.create_dish(db, submenu_id, data, cache)


@router.patch(
    '/{id}',
    response_model=DishesBase,
    name='Обновить блюдо',
    status_code=http.HTTPStatus.OK,
)
def update_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    data: DishesCreate,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Обновить блюдо:

    - **menu_id**: идентификатор меню
    - **submenu_id**: идентификатор подменю
    - **id**: идентификатор блюда
    - **title**: название блюда
    - **description**: описание блюда
    - **price**: цена блюда
    """
    crud.update_dish(db, submenu_id, dish_id, data, cache)
    return crud.get_dish(db, submenu_id, dish_id, cache)


@router.delete(
    '/{id}',
    name='Удалить блюдо',
    status_code=http.HTTPStatus.OK,
)
def delete_dish(
    menu_id: str,
    submenu_id: str,
    dish_id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Удалить блюдо:

    - **menu_id**: идентификатор меню
    - **submenu_id**: идентификатор подменю
    - **id**: идентификатор блюда
    """
    crud.delete_dish(db, menu_id, submenu_id, dish_id, cache)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'The dish has been deleted'},
    )
