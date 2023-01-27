from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas import SubmenuBase, SubmenuCreate
from app import crud
from app.exceptions import SubmenuExistsException

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus",
    tags=['Подменю'],
    dependencies=[Depends(get_db)],
)


@router.get(
    "/",
    response_model=List[SubmenuBase],
    name="Просмотр списка подменю",
)
def get_submenu_list(menu_id: int, db: Session = Depends(get_db)):
    return crud.get_submenu_list(db, menu_id)


@router.post(
    "/",
    response_model=SubmenuBase,
    name='Создать подменю',
    status_code=201,
)
def add_submenu(menu_id: int, data: SubmenuCreate, db: Session = Depends(get_db)):
    submenu = crud.create_submenu(db, menu_id, data)
    return crud.get_submenu(db, menu_id, submenu.id)


@router.get(
    "/{submenu_id}",
    response_model=SubmenuBase,
    name="Просмотр определенного подменю",
)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, menu_id, submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    return submenu


@router.patch(
    "/{submenu_id}",
    response_model=SubmenuBase,
    name="Обновить подменю",
)
def update_submenu(menu_id: int, submenu_id: int, data: SubmenuCreate, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, menu_id, submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    update_submenu = crud.update_submenu(db, menu_id, submenu_id, data)
    return crud.get_submenu(db, menu_id, update_submenu.id)


@router.delete(
    "/{submenu_id}",
    name="Удаление подменю",
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    crud.delete_submenu(db, menu_id, submenu_id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The submenu has been deleted"}
    )
