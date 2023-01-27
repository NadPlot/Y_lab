from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas import MenuBase, MenuCreate
from app import crud
from app.exceptions import MenuExistsException

router = APIRouter(
    prefix="/api/v1/menus",
    tags=['Меню'],
    dependencies=[Depends(get_db)],
)


@router.get(
    "/",
    response_model=List[MenuBase],
    name="Выдача списка меню"
)
def get_menu_list(db: Session = Depends(get_db)):
    return crud.get_menu_list(db)


@router.post(
    "/",
    response_model=MenuBase,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: MenuCreate, db: Session = Depends(get_db)):
    menu = crud.create_menu(db, data)
    return crud.get_menu(db, menu.id)


@router.get(
    "/{id}",
    response_model=MenuBase,
    name="Просмотр определенного меню",
)
def get_menu(id: int, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuExistsException()
    return menu


@router.patch(
    "/{id}",
    response_model=MenuBase,
    name="Обновить меню",
)
def update_menu(id: int, data: MenuCreate, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuExistsException()
    update_menu = crud.update_menu(db, id, data)
    return crud.get_menu(db, update_menu.id)


@router.delete(
    "/api/v1/menus/{id}/",
    name="Удаление меню",
)
def delete_menu(id: int, db: Session = Depends(get_db)):
    crud.delete_menu(db, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The menu has been deleted"}
    )
