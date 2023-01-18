from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from app import models, schemas, crud
from app.exceptions import MenuExistsException, SubmenuExistsException, DishExistsException
from app.database import SessionLocal, engine


description = """
Интенсив по Python (Y_lab)

REST API по работе с меню ресторана

"""
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REST API Меню (Y_lab)",
    description=description,
)


# Dependency (database session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Выдача списка меню
@app.get(
    "/api/v1/menus",
    response_model=List[schemas.MenuBase],
    name="Выдача списка меню",
)
def get_menu_list(db: Session = Depends(get_db)):
    return crud.get_menu_list(db)


# Создание меню
@app.post(
    "/api/v1/menus",
    response_model=schemas.MenuBase,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = crud.create_menu(db, data)
    return crud.get_menu(db, menu.id)


# Просмотр определенного меню
@app.get(
    "/api/v1/menus/{id}/",
    response_model=schemas.MenuBase,
    name="Просмотр определенного меню",
)
def get_menu(id: int, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuExistsException()
    return menu


# Обновить меню
@app.patch(
    "/api/v1/menus/{id}/",
    response_model=schemas.MenuBase,
    name="Обновить меню",
)
def update_menu(id: int, data: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuExistsException()
    update_menu = crud.update_menu(db, id, data)
    return crud.get_menu(db, update_menu.id)


# Удаление меню
@app.delete(
    "/api/v1/menus/{id}/",
    name="Удаление меню",
)
def delete_menu(id: int, db: Session = Depends(get_db)):
    crud.delete_menu(db, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The menu has been deleted"}
    )


# Просмотр списка подменю
@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=List[schemas.SubmenuBase],
    name="Просмотр списка подменю",
)
def get_submenu_list(menu_id: int, db: Session = Depends(get_db)):
    return crud.get_submenu_list(db, menu_id)


# Создание подменю
@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=schemas.SubmenuBase,
    name='Создать подменю',
    status_code=201,
)
def add_submenu(menu_id: int, data: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    submenu = crud.create_submenu(db, menu_id, data)
    return crud.get_submenu(db, menu_id, submenu.id)


# Просмотр определенного подменю
@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
    response_model=schemas.SubmenuBase,
    name="Просмотр определенного подменю",
)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, menu_id, submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    return submenu


# Обновить подменю
@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
    response_model=schemas.SubmenuBase,
    name="Обновить подменю",
)
def update_submenu(menu_id: int, submenu_id: int, data: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, menu_id, submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    update_submenu = crud.update_submenu(db, menu_id, submenu_id, data)
    return crud.get_submenu(db, menu_id, update_submenu.id)


# Удаление подменю
@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
    name="Удаление подменю",
)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    crud.delete_submenu(db, menu_id, submenu_id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The submenu has been deleted"}
    )


# Просмотр списка блюд
@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[schemas.DishesBase],
    name="Выдача списка блюд",
)
def get_dishes_list(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return crud.get_dishes_list(db, submenu_id)


# Просмотр определенного блюда
@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}",
    response_model=schemas.DishesBase,
    name="Просмотр определенного блюда",
)
def get_dish(submenu_id: int, id: int, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, submenu_id, id)
    if not dish:
        raise DishExistsException()
    return dish


# Создать блюдо
@app.post(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=schemas.DishesBase,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(menu_id: int, submenu_id: int, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = crud.create_dish(db, submenu_id, data)
    return crud.get_dish(db, submenu_id, dish.id)


# Обновить блюдо
@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}",
    response_model=schemas.DishesBase,
    name="Обновить блюдо",
)
def update_dish(menu_id: int, submenu_id: int, id: int, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, submenu_id, id)
    if not dish:
        raise DishExistsException()
    update_dish = crud.update_dish(db, submenu_id, id, data)
    return crud.get_dish(db, submenu_id, update_dish.id)


# Удаление блюда
@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{id}",
    name="Удалить блюдо",
)
def delete_dish(menu_id: int, submenu_id: int, id: int, db: Session = Depends(get_db)):
    crud.delete_dish(db, submenu_id, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )


# Обработчики ошибок
@app.exception_handler(MenuExistsException)
async def menu_exists_handler(request: Request, exc: MenuExistsException):
    return JSONResponse(
        status_code=404,
        content={"detail": "menu not found"}
    )


@app.exception_handler(SubmenuExistsException)
async def submenu_exists_handler(request: Request, exc: SubmenuExistsException):
    return JSONResponse(
        status_code=404,
        content={"detail": "submenu not found"}
    )


@app.exception_handler(DishExistsException)
async def dish_exists_handler(request: Request, exc: DishExistsException):
    return JSONResponse(
        status_code=404,
        content={"detail": "dish not found"}
    )
