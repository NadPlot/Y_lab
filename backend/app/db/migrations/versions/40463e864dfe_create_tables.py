"""create_tables

Revision ID: 40463e864dfe
Revises: 
Create Date: 2023-02-19 18:34:11.113850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '40463e864dfe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.String(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submenu',
    sa.Column('id', sa.String(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('menu_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dishes',
    sa.Column('id', sa.String(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('menu_id', sa.String(), nullable=False),
    sa.Column('submenu_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
