"""rewrite posts table

Revision ID: 50a4077b7318
Revises: ea07665cc60a
Create Date: 2022-10-21 23:50:45.765283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50a4077b7318'
down_revision = 'ea07665cc60a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(),
                              nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(
                        timezone=True), nullable=False, server_default=sa.text('now()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
