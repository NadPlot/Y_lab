"""create_main_tables

Revision ID: 33fe0b340403
Revises: 
Create Date: 2023-02-14 18:38:49.000419

"""
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '33fe0b340403'
down_revision = None
branch_labels = None
depends_on = None

def create_menu_table() -> None:
    op.create_table(
        "menu",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=False), default=uuid4, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
    )


def create_submenu_table() -> None:
    op.create_table(
        "submenu",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=False), default=uuid4, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("menu_id", sa.dialects.postgresql.UUID(as_uuid=False), sa.ForeignKey("menu.id", ondelete="CASCADE"), nullable=False),
    )


def create_dishes_table() -> None:
    op.create_table(
        "dishes",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=False), default=uuid4, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("menu_id", sa.dialects.postgresql.UUID(as_uuid=False), sa.ForeignKey("menu.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submenu_id", sa.dialects.postgresql.UUID(as_uuid=False), sa.ForeignKey("submenu.id", ondelete="CASCADE"), nullable=False),
    )


def upgrade() -> None:
    create_menu_table()
    create_submenu_table()
    create_dishes_table()


def downgrade() -> None:
    pass

