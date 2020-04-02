from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from chatbot.database import Base
from chatbot.database.utils import IDMixin


class Nickname(IDMixin, Base):
    nickname = Column(String)
    user_id = Column(Integer, ForeignKey("qedler.user_id"))

    qedler = relationship("QEDler", back_populates="nicknames")


class QEDler(IDMixin, Base):
    user_id = Column(Integer, unique=True)
    user_name = Column(String, unique=True)

    nicknames = relationship("Nickname", back_populates="qedler")
