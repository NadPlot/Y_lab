from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import models
from app.database import engine
from app.exceptions import (
    DishExistsException,
    MenuExistsException,
    SubmenuExistsException,
)
from app.routers import dishes, menu, submenu

description = 'Интенсив по Python (Y_lab)'


tags_metadata = [
    {
        'name': 'Меню',
        'description': 'Операции CRUD меню. Просмотр списка меню, отдельного меню',
    },
    {
        'name': 'Подменю',
        'description': 'Операции CRUD подменю. Просмотр списка подменю, отдельного подменю',
    },
    {
        'name': 'Блюда',
        'description': 'Операции CRUD блюд. Просмотр списка блюд, отдельного блюда',
    },
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='REST API по работе с меню ресторана',
    description=description,
    openapi_tags=tags_metadata,
)


app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dishes.router)


# Обработчики ошибок
@app.exception_handler(MenuExistsException)
async def menu_exists_handler(request: Request, exc: MenuExistsException):
    return JSONResponse(
        status_code=404,
        content={'detail': 'menu not found'},
    )


@app.exception_handler(SubmenuExistsException)
async def submenu_exists_handler(request: Request, exc: SubmenuExistsException):
    return JSONResponse(
        status_code=404,
        content={'detail': 'submenu not found'},
    )


@app.exception_handler(DishExistsException)
async def dish_exists_handler(request: Request, exc: DishExistsException):
    return JSONResponse(
        status_code=404,
        content={'detail': 'dish not found'},
    )
