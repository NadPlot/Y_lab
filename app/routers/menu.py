import http
import json

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud
from app.cache import get_redis
from app.dependencies import get_db
from app.exceptions import MenuExistsException
from app.schemas import CacheBase, MenuBase, MenuCreate

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Меню'],
)


@router.get(
    '/',
    response_model=list[MenuBase],
    name='Выдача списка меню',
    status_code=http.HTTPStatus.OK,
)
def get_menu_list(
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Просмотр списка меню:

    - **id**: идентификатор меню
    - **title**: название меню
    - **description**: описание меню
    - **submenus_count**: Количество подменю в составе меню
    - **dishes_count**: Количество блюд в меню
    """
    if not cache.get('menu'):
        list_menu = crud.get_menu_list(db)
        cache.set('menu', json.dumps(list_menu))
        cache.expire('menu', 300)
        return list_menu
    else:
        return json.loads(cache.get('menu'))


@router.post(
    '/',
    response_model=MenuBase,
    name='Создать меню',
    status_code=201,
)
def add_menu(
    data: MenuCreate,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    Создать новое меню:

    - **title**: название меню
    - **description**: описание меню
    """
    menu = crud.create_menu(db, data)
    cache.delete('menu')
    return crud.get_menu(db, menu.id)


@router.get(
    '/{id}',
    response_model=MenuBase,
    name='Просмотр определенного меню',
)
def get_menu(
    id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    По id меню посмотреть определенное меню:

    - **id**: идентификатор меню
    - **title**: название меню
    - **description**: описание меню
    - **submenus_count**: Количество подменю в составе меню
    - **dishes_count**: Количество блюд в меню
    """
    if not cache.get(id):
        menu = crud.get_menu(db, id)
        cache.set(id, json.dumps(menu))
        cache.expire(id, 300)
        if not menu:
            raise MenuExistsException()
        return menu
    else:
        return json.loads(cache.get(id))


@router.patch(
    '/{id}',
    response_model=MenuBase,
    name='Обновить меню',
)
def update_menu(
    id: str,
    data: MenuCreate,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    По Id меню обновить меню:

    - **id**: идентификатор меню
    - **title**: название меню
    - **description**: описание меню
    """
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuExistsException()
    update_menu = crud.update_menu(db, id, data)
    cache.delete(id)
    cache.delete('menu')
    return crud.get_menu(db, update_menu.id)


@router.delete(
    '/{id}',
    name='Удаление меню',
)
def delete_menu(
    id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis),
):
    """
    По id меню удалить меню:

    - **id**: идентификатор меню
    """
    crud.delete_menu(db, id)
    cache.delete(id)
    cache.delete('menu', 'submenu', 'dishes')

    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'The menu has been deleted'},
    )
