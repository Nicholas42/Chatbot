from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_method

from chatbot import glob
from chatbot.interface.messages import OutgoingMessage, IncomingMessage
from . import Base
from .utils import IDMixin, model_from_data_class


@model_from_data_class(OutgoingMessage)
class OutgoingMessageModel(IDMixin, Base):
    sent = Column(Boolean)
    send_time = Column(DateTime)

    @hybrid_method
    def still_to_send(self, slack=timedelta(minutes=1)):
        return not self.sent and self.send_time > (datetime.now() - slack)


@model_from_data_class(IncomingMessage)
class IncomingMessageModel(IDMixin, Base):
    pass


glob.db.create_all()
