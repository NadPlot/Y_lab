from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine
from .config import settings
from app import models
from app.routers import menu, submenu, dishes
from app.exceptions import MenuExistsException, SubmenuExistsException
from app.exceptions import DishExistsException


description = 'Интенсив по Python (Y_lab)'


tags_metadata = [
    {
        "name": "Меню",
        "description": "Создание, обновление, удаление меню. Просмотр списка меню и отдельного меню",
    },
    {
        "name": "Подменю",
        "description": "Создание, обновление, удаление подменю. Просмотр списка подменю и отдельного подменю",
    },
    {
        "name": "Блюда",
        "description": "Создание, обновление, удаление блюд. Просмотр списка блюд и отдельного блюда",
    },
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="REST API по работе с меню ресторана",
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
