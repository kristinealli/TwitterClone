"""add customers date_of_birth

Revision ID: 311c26ec627f
Revises: 6f64b41ae4e4
Create Date: 2023-08-08 23:40:24.594891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '311c26ec627f'
down_revision = '6f64b41ae4e4'
branch_labels = None
depends_on = None


def upgrade():
    op. execute (
        """
        ALTER TABLE customers
        ADD COLUMN date_of_birth TIMESTAMP;
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE customers
        DROP COLUMN date_of_birth:
        """
    )
    
