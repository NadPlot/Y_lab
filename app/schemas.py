from pydantic import BaseModel
from typing import Optional, List


# База чтение и запись, таблица Menu
class MenuBase(BaseModel):
    id: int
    title: str
    description: str
    submenus_count: Optional[int]
    dishes_count: Optional[int]
    
    class Config:
        orm_mode = True



# class MenuList(BaseModel):
#     menu: List[MenuBase]

#     class Config:
#         orm_mode = True
