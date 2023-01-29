from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Float, ForeignKey
from uuid import uuid4
from app.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False, default=0.00)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)
