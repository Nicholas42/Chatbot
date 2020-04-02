"""Message Tables

Revision ID: d28b73899ae5
Revises: 
Create Date: 2020-04-02 14:08:58.783100

"""
import sqlalchemy as sa
from alembic import op

import chatbot.database.utils

# revision identifiers, used by Alembic.
revision = 'd28b73899ae5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('incomingmessagemodel',
                    sa.Column('_column_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('message', sa.String(), nullable=True),
                    sa.Column('channel', sa.String(), nullable=True),
                    sa.Column('date', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('delay', sa.Integer(), nullable=True),
                    sa.Column('bottag', sa.Boolean(), nullable=True),
                    sa.Column('type', sa.Enum('post', 'ping', 'pong', 'ack', name='messagetype'), nullable=True),
                    sa.Column('color', chatbot.database.utils.ColorColumn(), nullable=True),
                    sa.PrimaryKeyConstraint('_column_id')
                    )
    op.create_table('outgoingmessagemodel',
                    sa.Column('_column_id', sa.Integer(), nullable=False),
                    sa.Column('sent', sa.Boolean(), nullable=True),
                    sa.Column('send_time', sa.DateTime(), nullable=True),
                    sa.Column('channel', sa.String(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('message', sa.String(), nullable=True),
                    sa.Column('delay', sa.Integer(), nullable=True),
                    sa.Column('publicid', sa.Integer(), nullable=True),
                    sa.Column('bottag', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('_column_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('outgoingmessagemodel')
    op.drop_table('incomingmessagemodel')
    # ### end Alembic commands ###
