"""add foreign-key to posts table

Revision ID: 926d53378086
Revises: cfa200ef57f0
Create Date: 2022-10-21 23:06:44.931421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '926d53378086'
down_revision = 'cfa200ef57f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer, nullable=False))
    op.create_foreign_key(constraint_name='posts_users_fk', source_table='posts',
                          referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name='posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
