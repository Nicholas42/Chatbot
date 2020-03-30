from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from . import Base
from .utils import IDMixin, model_from_data_class
from chatbot.interface.messages import OutgoingMessage, IncomingMessage


@model_from_data_class(OutgoingMessage)
class OutgoingMessageModel(IDMixin, Base):
    sent = Column(DateTime)

    @hybrid_property
    def still_to_send(self, slack=timedelta(minutes=1)):
        return self.sent > (datetime.now() - slack)


@model_from_data_class(IncomingMessage)
class IncomingMessageModel(IDMixin, Base):
    pass
