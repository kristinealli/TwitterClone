"""empty message

Revision ID: 33a33d001711
Revises: 0879f0b4b47b
Create Date: 2023-08-12 20:16:35.327873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33a33d001711'
down_revision = '0879f0b4b47b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'tweet_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
