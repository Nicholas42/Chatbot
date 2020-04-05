"""Tables for nicknames

Revision ID: a2b2ae34165f
Revises: 0413ee207d0d
Create Date: 2020-04-02 17:28:50.247250

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a2b2ae34165f'
down_revision = '0413ee207d0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qedler',
                    sa.Column('_column_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('user_name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('_column_id', name="qedler_column_id_pkey"),
                    sa.UniqueConstraint('user_id', name="qedler_user_id_unique"),
                    sa.UniqueConstraint('user_name', name="qeder_user_name_unique")
                    )
    op.create_table('nickname',
                    sa.Column('_column_id', sa.Integer(), nullable=False),
                    sa.Column('nickname', sa.String(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['qedler.user_id'], name='nickname_user_id_fkey'),
                    sa.PrimaryKeyConstraint('_column_id', name='nickname_column_id_pkey')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('nickname')
    op.drop_table('qedler')
    # ### end Alembic commands ###
