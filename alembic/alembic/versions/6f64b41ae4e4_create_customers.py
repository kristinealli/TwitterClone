"""create customers

Revision ID: 6f64b41ae4e4
Revises: 
Create Date: 2023-08-08 23:35:30.649551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f64b41ae4e4'
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
