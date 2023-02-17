from pydantic import BaseModel, Field
from uuid import uuid4


class MenuBase(BaseModel):
    title: str = Field(
        title='Наименование',
    )
    description: str = Field(
        title='Описание',
    )


class OutDB(BaseModel):
    id: str
