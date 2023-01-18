from pydantic import BaseModel


# Чтение таблица Menu
class MenuBase(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


# Запись и обновление таблица Menu
class MenuCreate(BaseModel):
    title: str
    description: str


# Чтение таблица Submenu
class SubmenuBase(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


# Запись и обновление таблица Submenu
class SubmenuCreate(BaseModel):
    title: str
    description: str


# Чтение таблица Dishes
class DishesBase(BaseModel):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


# Запись и обновление таблица Dishes
class DishesCreate(BaseModel):
    title: str
    description: str
    price: float
