from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas import DishesBase, DishesCreate
from app import crud
from app.exceptions import DishExistsException

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=['Блюда'],
    dependencies=[Depends(get_db)],
)



@router.get(
    "/",
    response_model=List[DishesBase],
    name="Выдача списка блюд",
)
def get_dishes_list(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_dishes_list(db, submenu_id)


@router.get(
    "/{id}",
    response_model=DishesBase,
    name="Просмотр определенного блюда",
)
def get_dish(submenu_id: int, id: int, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, submenu_id, id)
    if not dish:
        raise DishExistsException()
    return dish


@router.post(
    "/",
    response_model=DishesBase,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(menu_id: int, submenu_id: int, data: DishesCreate, db: Session = Depends(get_db)):
    dish = crud.create_dish(db, submenu_id, data)
    return crud.get_dish(db, submenu_id, dish.id)


@router.patch(
    "/{id}",
    response_model=DishesBase,
    name="Обновить блюдо",
)
def update_dish(menu_id: int, submenu_id: int, id: int, data: DishesCreate, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, submenu_id, id)
    if not dish:
        raise DishExistsException()
    update_dish = crud.update_dish(db, submenu_id, id, data)
    return crud.get_dish(db, submenu_id, update_dish.id)


@router.delete(
    "/{id}",
    name="Удалить блюдо",
)
def delete_dish(menu_id: int, submenu_id: int, id: int, db: Session = Depends(get_db)):
    crud.delete_dish(db, submenu_id, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )
