from pydantic import BaseModel, Field


# Чтение таблица Menu
class MenuBase(BaseModel):
    id: str
    title: str = Field(
        title='Наименование меню',
    )
    description: str = Field(
        title='Описание меню',
    )
    submenus_count: int = Field(
        title='Количество подменю в меню',
    )
    dishes_count: int = Field(
        title='Количество блюд в меню',
    )

    class Config:
        orm_mode = True


# Запись и обновление таблица Menu
class MenuCreate(BaseModel):
    title: str = Field(
        title='Наименование меню',
        max_length=30,
    )
    description: str = Field(
        title='Описание меню',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My menu',
                'description': 'My description',
            },
        }


# Чтение таблица Submenu
class SubmenuBase(BaseModel):
    id: str
    title: str = Field(
        title='Наименование подменю',
    )
    description: str = Field(
        title='Описание подменю',
    )
    dishes_count: int = Field(
        title='Количество блюд в меню',
    )

    class Config:
        orm_mode = True


# Запись и обновление таблица Submenu
class SubmenuCreate(BaseModel):
    title: str = Field(
        title='Наименование подменю',
        max_length=30,
    )
    description: str = Field(
        title='Описание подменю',
        max_length=255,
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My submenu',
                'description': 'My submenu description',
            },
        }


# Чтение таблица Dishes
class DishesBase(BaseModel):
    id: str
    title: str = Field(
        title='Наименование блюда',
    )
    description: str = Field(
        title='Описание блюда',
    )
    price: str

    class Config:
        orm_mode = True


# Запись и обновление таблица Dishes
class DishesCreate(BaseModel):
    title: str = Field(
        title='Наименование блюда',
        max_length=30,
    )
    description: str = Field(
        title='Описание блюда',
        max_length=255,
    )
    price: float = Field(
        title='Цена блюда, формата 0.00',
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'My dish',
                'description': 'My dish description',
                'price': '12.55',
            },
        }


# для получения и записи кэша
class CacheBase(BaseModel):
    key: str
