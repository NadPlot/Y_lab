from sqlalchemy import Column, Numeric, ForeignKey, String, text
#from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(String, server_default=text("gen_random_uuid()"), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(String, server_default=text("gen_random_uuid()"), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        String,
        ForeignKey('menu.id', ondelete='CASCADE'),
        nullable=False,
    )


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(String, server_default=text("gen_random_uuid()"), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    menu_id = Column(
        String,
        ForeignKey('menu.id', ondelete='CASCADE'),
        nullable=False,
    )
    submenu_id = Column(
        String,
        ForeignKey('submenu.id', ondelete='CASCADE'),
        nullable=False,
    )
