"""alter date of birth set default now

Revision ID: f871a4268104
Revises: 5758c7d9268f
Create Date: 2023-08-09 22:39:09.390091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f871a4268104'
down_revision = '5758c7d9268f'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
