"""create posts table

Revision ID: 10c9ce3a67b1
Revises: 
Create Date: 2022-10-21 16:50:39.513546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10c9ce3a67b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
