from pydantic import BaseModel
from typing import Optional, List


# База чтение таблица Menu
class MenuBase(BaseModel):
    id: int
    title: str
    description: str
    submenus_count: Optional[int]
    dishes_count: Optional[int]
    
    class Config:
        orm_mode = True

# База запись таблица Menu
class MenuCreate(BaseModel):
    title: str
    description: str


class MenuList(BaseModel):
    menu: List[MenuBase]

    class Config:
        orm_mode = True
