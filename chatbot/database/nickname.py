from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from chatbot.database import Base
from chatbot.database.utils import IDMixin


class Nickname(IDMixin, Base):
    nickname = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("qedler.user_id"))

    qedler = relationship("QEDler", back_populates="nicknames")


class QEDler(IDMixin, Base):
    user_id = Column(Integer, unique=True)
    forename = Column(String)
    surname = Column(String)

    nicknames = relationship("Nickname", back_populates="qedler")

    @hybrid_property
    def user_name(self):
        return self.forename + self.surname
