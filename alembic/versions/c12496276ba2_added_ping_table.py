"""Added ping table.

Revision ID: c12496276ba2
Revises: 145b9d5f7c35
Create Date: 2020-04-03 17:51:10.733847

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c12496276ba2'
down_revision = '145b9d5f7c35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ping',
                    sa.Column('_column_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('target', sa.Integer(), nullable=True),
                    sa.Column('message', sa.Text(), nullable=False),
                    sa.Column('ping_time', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
                    sa.Column('sender', sa.String(), nullable=False),
                    sa.Column('activation_time', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
                    sa.ForeignKeyConstraint(['target'], ['nickname._column_id'], name='ping_target_fkey'),
                    sa.ForeignKeyConstraint(['user_id'], ['qedler.user_id'], name='ping_user_id_fkey'),
                    sa.PrimaryKeyConstraint('_column_id', name='ping_column_id_pkey')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ping')
    # ### end Alembic commands ###
