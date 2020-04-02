from sqlalchemy import Column, Integer, ForeignKey, String, types
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from chatbot import glob
from chatbot.database import Base
from chatbot.database.utils import IDMixin


def normalize_nickname(nickname: str):
    return nickname.strip().lower()


class NicknameColumn(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, db_entry: str, dialect) -> str:
        return db_entry

    def process_result_value(self, nickname: str, dialect) -> str:
        return normalize_nickname(nickname)

    def copy(self, **kw):
        return NicknameColumn(self.impl.length)


class Nickname(IDMixin, Base):
    nickname = Column(NicknameColumn, unique=True)
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
