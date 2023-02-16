from uuid import uuid4

from sqlalchemy import Column, Numeric, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=False), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=False), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        UUID(as_uuid=False),
        ForeignKey('menu.id', ondelete='CASCADE'),
        nullable=False,
    )


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=False), default=uuid4, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    menu_id = Column(
        UUID(as_uuid=False),
        ForeignKey('menu.id', ondelete='CASCADE'),
        nullable=False,
    )
    submenu_id = Column(
        UUID(as_uuid=False),
        ForeignKey('submenu.id', ondelete='CASCADE'),
        nullable=False,
    )
