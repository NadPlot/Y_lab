# import http

# from fastapi import APIRouter, Depends
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session

# from app import crud
# from app.cache import get_redis, CacheBase
# from app.dependencies import get_db
# from app.schemas import SubmenuBase, SubmenuCreate

# router = APIRouter(
#     prefix='/api/v1/menus/{menu_id}/submenus',
#     tags=['Подменю'],
# )


# @router.get(
#     '/',
#     response_model=list[SubmenuBase],
#     name='Просмотр списка подменю',
#     status_code=http.HTTPStatus.OK,
# )
# def get_submenu_list(
#     menu_id: str,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     Просмотр списка подменю по id меню:

#     - **menu_id**: идентификатор меню
#     - **title**: название подменю
#     - **description**: описание подменю
#     - **dishes_count**: Количество блюд в подменю
#     """
#     return crud.get_submenu_list(db, menu_id, cache)


# @router.post(
#     '/',
#     response_model=SubmenuBase,
#     name='Создать подменю',
#     status_code=201,
# )
# def add_submenu(
#     menu_id: str,
#     data: SubmenuCreate,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     Создать новое подменю:

#     - **menu_id**: идентификатор меню
#     - **title**: название подменю
#     - **description**: описание подменю
#     """
#     return crud.create_submenu(db, menu_id, data, cache)


# @router.get(
#     '/{submenu_id}',
#     response_model=SubmenuBase,
#     name='Просмотр определенного подменю',
#     status_code=http.HTTPStatus.OK,
# )
# def get_submenu(
#     menu_id: str,
#     submenu_id: str,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По id меню и id подменю посмотреть подменю:

#     - **menu_id**: идентификатор меню
#     - **submenu_id**: идентификатор подменю
#     - **title**: название подменю
#     - **description**: описание подменю
#     - **dishes_count**: Количество блюд в подменю
#     """
#     return crud.get_submenu(db, menu_id, submenu_id, cache)


# @router.patch(
#     '/{submenu_id}',
#     response_model=SubmenuBase,
#     name='Обновить подменю',
#     status_code=http.HTTPStatus.OK,
# )
# def update_submenu(
#     menu_id: str,
#     submenu_id: str,
#     data: SubmenuCreate,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По id меню и id подменю обновить подменю:

#     - **menu_id**: идентификатор меню
#     - **submenu_id**: идентификатор подменю
#     - **title**: название подменю
#     - **description**: описание подменю
#     """
#     crud.update_submenu(db, menu_id, submenu_id, data, cache)
#     return crud.get_submenu(db, menu_id, submenu_id, cache)


# @router.delete(
#     '/{submenu_id}',
#     name='Удаление подменю',
#     status_code=http.HTTPStatus.OK,
# )
# def delete_submenu(
#     menu_id: str,
#     submenu_id: str,
#     db: Session = Depends(get_db),
#     cache: CacheBase = Depends(get_redis),
# ):
#     """
#     По id меню и id подменю удалить подменю:

#     - **menu_id**: идентификатор меню
#     - **submenu_id**: идентификатор подменю
#     """
#     crud.delete_submenu(db, menu_id, submenu_id, cache)
#     return JSONResponse(
#         status_code=200,
#         content={'status': 'true', 'message': 'The submenu has been deleted'},
#     )
