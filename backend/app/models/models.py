from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy import text
from sqlalchemy.orm import column_property
from sqlalchemy import select, func

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(
        String,
        server_default=text("gen_random_uuid()"),
        primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    menu_id = Column(
        String,
        ForeignKey("menu.id", ondelete="CASCADE"),
        nullable=False,
    )
    submenu_id = Column(
        String,
        ForeignKey("submenu.id", ondelete="CASCADE"),
        nullable=False,
    )


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(
        String,
        server_default=text("gen_random_uuid()"),
        primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        String,
        ForeignKey("menu.id", ondelete="CASCADE"),
        nullable=False,
    )
    dishes_count = column_property(
        select(func.count(Dishes.id))
        .where(Dishes.submenu_id == id)
        .correlate_except(Dishes)
        .scalar_subquery()
    )


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        String,
        server_default=text("gen_random_uuid()"),
        primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery()
    )
    dishes_count = column_property(
        select(func.count(Dishes.id))
        .where(Dishes.menu_id == id)
        .correlate_except(Dishes)
        .scalar_subquery()
    )
