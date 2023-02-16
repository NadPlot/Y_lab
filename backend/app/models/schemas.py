from pydantic import Field
from app.models.core import MenuBase, OutDB


# Чтение таблица Menu
class MenuRead(MenuBase, OutDB):
    submenus_count: int = Field(
        title='Количество подменю в меню',
        default='0',
    )
    dishes_count: int = Field(
        title='Количество блюд в меню',
        default='0',
    )

    class Config:
        orm_mode = True


# Запись и обновление таблица Menu
class MenuCreate(MenuBase):
    pass

    class Config:
        schema_extra = {
            'example': {
                'title': 'My menu',
                'description': 'My description',
            },
        }


# Чтение таблица Submenu
class SubmenuRead(MenuBase, OutDB):
    dishes_count: int = Field(
        title='Количество блюд в меню',
    )

    class Config:
        orm_mode = True


# Запись и обновление таблица Submenu
class SubmenuCreate(MenuBase):
    pass

    class Config:
        schema_extra = {
            'example': {
                'title': 'My submenu',
                'description': 'My submenu description',
            },
        }


# Чтение таблица Dishes
class DishesRead(MenuBase, OutDB):
    price: str

    class Config:
        orm_mode = True


# Запись и обновление таблица Dishes
class DishesCreate(MenuBase):
    price: float = Field(
        title='Цена блюда',
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My dish',
                'description': 'My dish description',
                'price': '12.55',
            },
        }
