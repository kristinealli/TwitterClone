"""alter column date of birth

Revision ID: 5758c7d9268f
Revises: f1c9d5721df1
Create Date: 2023-08-09 22:25:33.789765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5758c7d9268f'
down_revision = 'f1c9d5721df1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE customers
            ALTER COLUMN date_of_birth SET DEFAULT now();
        """
    )

def downgrade():
    op.execute(
        """
        DROP TABLE table3;
        DROP TABLE table2;
        DROP TABLE table1;
        """
    )
