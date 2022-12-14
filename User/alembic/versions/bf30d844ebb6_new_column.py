"""New column

Revision ID: bf30d844ebb6
Revises: 92877f9ecd12
Create Date: 2022-11-28 18:17:27.710282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf30d844ebb6'
down_revision = '92877f9ecd12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_', sa.Column('contact_id', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_', 'contact_id')
    # ### end Alembic commands ###
