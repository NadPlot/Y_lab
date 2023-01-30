import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List

from app.dependencies import get_db, get_redis
from app.schemas import SubmenuBase, SubmenuCreate, CacheBase
from app import crud
from app.exceptions import SubmenuExistsException


router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=['Подменю'],
)


@router.get(
    "/",
    response_model=List[SubmenuBase],
    name="Просмотр списка подменю",
)
def get_submenu_list(
    menu_id: str,
    db: Session = Depends(get_db),
    cache: CacheBase = Depends(get_redis)
):
    if not cache.get('submenu'):
        list_submenu = crud.get_submenu_list(db, menu_id)
        cache.set('submenu', json.dumps(list_submenu))
        cache.expire('submenu', 300)
        return list_submenu
    else:
        return json.loads(cache.get('submenu'))


@router.post(
    "/",
    response_model=SubmenuBase,
    name='Создать подменю',
    status_code=201,
)
def add_submenu(menu_id: str, data: SubmenuCreate, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    submenu = crud.create_submenu(db, menu_id, data)
    cache.delete('menu', 'submenu')
    return crud.get_submenu(db, menu_id, submenu.id)


@router.get(
    "/{submenu_id}",
    response_model=SubmenuBase,
    name="Просмотр определенного подменю",
)
def get_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    if not cache.get(submenu_id):
        submenu = crud.get_submenu(db, menu_id, submenu_id)
        cache.set(submenu_id, json.dumps(submenu))
        cache.expire(submenu_id, 300)
        if not submenu:
            raise SubmenuExistsException()
        return submenu
    else:
        return json.loads(cache.get(submenu_id))


@router.patch(
    "/{submenu_id}",
    response_model=SubmenuBase,
    name="Обновить подменю",
)
def update_submenu(menu_id: str, submenu_id: str, data: SubmenuCreate, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    submenu = crud.get_submenu(db, menu_id, submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    update_submenu = crud.update_submenu(db, menu_id, submenu_id, data)
    cache.delete(submenu_id)
    cache.delete('submenu')
    return crud.get_submenu(db, menu_id, update_submenu.id)


@router.delete(
    "/{submenu_id}",
    name="Удаление подменю",
)
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db), cache: CacheBase = Depends(get_redis)):
    crud.delete_submenu(db, menu_id, submenu_id)
    cache.delete(menu_id, submenu_id)
    cache.delete('menu', 'submenu', 'dishes')
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The submenu has been deleted"}
    )
