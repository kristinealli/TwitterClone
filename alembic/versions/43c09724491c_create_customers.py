"""create customers

Revision ID: 43c09724491c
Revises: 
Create Date: 2023-08-08 22:43:22.250379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43c09724491c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE customers(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
        """
    )


def downgrade():
    op.execute(
        """
        DROP TABLE customers;
        """
    )
