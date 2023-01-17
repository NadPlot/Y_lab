from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from app import models, schemas, crud
from app.exceptions import MenuExistsException, SubmenuExistsException
from app.database import SessionLocal, engine



description = """
Интенсив по Python (Y_lab)

REST API
Меню ресторана (Домашнее задание, Вебинар №1)

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
    menu = crud.create_menu(db, menu=data)
    return crud.get_menu(db, id=menu.id)


# Просмотр определенного меню
@app.get(
    "/api/v1/menus/{id}/",
    response_model=schemas.MenuBase,
    name="Просмотр определенного меню",
)
def get_menu(id: int, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id=id)
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
    menu = crud.get_menu(db, id=id)
    if not menu:
        raise MenuExistsException()
    update_menu = crud.update_menu(db, id, data)
    return crud.get_menu(db, id=update_menu.id)


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


# Просмотр определенного подменю
@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
    response_model=schemas.SubmenuBase,
    name="Просмотр определенного подменю",
)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if not submenu:
        raise SubmenuExistsException()
    return submenu


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
