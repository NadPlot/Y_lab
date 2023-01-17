from pydantic import BaseModel
from typing import Optional, List


# База чтение таблица Menu
class MenuBase(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int
    
    class Config:
        orm_mode = True

# База запись таблица Menu
class MenuCreate(BaseModel):
    title: str
    description: str