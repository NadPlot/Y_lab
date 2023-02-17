from typing import List
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.models.schemas import MenuCreate, MenuRead
from app.db.repositories.crud import MenuRepository
from app.api.dependencies.database import get_repository


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menu"],
)


@router.post("/", response_model=MenuRead, name="menu:create-menu", status_code=HTTP_201_CREATED)
async def create_menu(
    new_menu: MenuCreate = Body(..., embed=True),
    db_repo: MenuRepository = Depends(get_repository(MenuRepository)),
) -> MenuRead:
    """
     - **id**: идентификатор меню
     - **title**: название меню
     - **description**: описание меню
     - **submenus_count**: Количество подменю в составе меню
     - **dishes_count**: Количество блюд в меню
    """
    return await db_repo.create_menu(new_menu=new_menu)

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
