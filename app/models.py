from sqlalchemy import Column
from sqlalchemy import String, Integer, Float, ForeignKey, Sequence
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.00)
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
