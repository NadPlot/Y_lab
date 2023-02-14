import http

from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud
from app.cache import get_redis, CacheBase
#from app.dependencies import get_db
from app.schemas import MenuBase, MenuCreate

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menu"],
)


@router.get("/")
async def get_all_cleanings() -> List[dict]:
    cleanings = [
        {"id": 1, "name": "My house", "cleaning_type": "full_clean", "price_per_hour": 29.99},
        {"id": 2, "name": "Someone else's house", "cleaning_type": "spot_clean", "price_per_hour": 19.99}
    ]
    return cleanings

# @router.get(
#     '/',
#     response_model=list[MenuBase],
#     name='Выдача списка меню',
#     status_code=http.HTTPStatus.OK,
# )
# async def get_menu_list(
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ) -> List[dict]:
#     """
#     Просмотр списка меню:

#     - **id**: идентификатор меню
#     - **title**: название меню
#     - **description**: описание меню
#     - **submenus_count**: Количество подменю в составе меню
#     - **dishes_count**: Количество блюд в меню
#     """
#     return crud.get_menu_list(db, cache)


# @router.post(
#     '/',
#     response_model=MenuBase,
#     name='Создать меню',
#     status_code=201,
# )
# def add_menu(
#     data: MenuCreate,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     Создать новое меню:

#     - **title**: название меню
#     - **description**: описание меню
#     """
#     return crud.create_menu(db, data, cache)


# @router.get(
#     '/{id}',
#     response_model=MenuBase,
#     name='Просмотр определенного меню',
#     status_code=http.HTTPStatus.OK,
# )
# def get_menu(
#     id: str,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По id меню посмотреть определенное меню:

#     - **id**: идентификатор меню
#     - **title**: название меню
#     - **description**: описание меню
#     - **submenus_count**: Количество подменю в составе меню
#     - **dishes_count**: Количество блюд в меню
#     """

#     return crud.get_menu(db, id, cache)


# @router.patch(
#     '/{id}',
#     response_model=MenuBase,
#     name='Обновить меню',
#     status_code=http.HTTPStatus.OK,
# )
# def update_menu(
#     id: str,
#     data: MenuCreate,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По Id меню обновить меню:

#     - **id**: идентификатор меню
#     - **title**: название меню
#     - **description**: описание меню
#     """
#     crud.update_menu(db, id, data, cache)
#     return crud.get_menu(db, id, cache)


# @router.delete(
#     '/{id}',
#     name='Удаление меню',
#     status_code=http.HTTPStatus.OK,
# )
# def delete_menu(
#     id: str,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По id меню удалить меню:

#     - **id**: идентификатор меню
#     """
#     crud.delete_menu(db, id, cache)
#     return JSONResponse(
#         status_code=200,
#         content={'status': 'true', 'message': 'The menu has been deleted'},
#     )
