"""NOT NULL

Revision ID: 145b9d5f7c35
Revises: 90443bd32493
Create Date: 2020-04-03 17:44:46.576619

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from chatbot.database.utils import UTCNow

revision = '145b9d5f7c35'
down_revision = '90443bd32493'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('incomingmessagemodel', 'id',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('nickname', 'nickname',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('nickname', 'original',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('outgoingmessagemodel', 'send_time',
                    existing_type=sa.VARCHAR(),
                    nullable=False,
                    server_default=UTCNow())
    op.alter_column('outgoingmessagemodel', 'sent',
                    existing_type=sa.BOOLEAN(),
                    nullable=False,
                    server_default="false")
    op.alter_column('qedler', 'forename',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('qedler', 'surname',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('song', 'title',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('song', 'video_id',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('song', 'video_id',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('song', 'title',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('qedler', 'surname',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('qedler', 'forename',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('outgoingmessagemodel', 'sent',
                    existing_type=sa.BOOLEAN(),
                    nullable=True)
    op.alter_column('outgoingmessagemodel', 'send_time',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('nickname', 'original',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('nickname', 'nickname',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('incomingmessagemodel', 'id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    # ### end Alembic commands ###
