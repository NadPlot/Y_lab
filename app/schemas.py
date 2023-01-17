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
