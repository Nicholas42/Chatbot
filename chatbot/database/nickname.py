from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from chatbot import glob
from chatbot.database import Base
from chatbot.database.utils import IDMixin, normalize_nickname, CaseInsensitiveComparator, NicknameColumn


class Nickname(IDMixin, Base):
    nickname = Column(NicknameColumn, unique=True)
    original = Column(String, unique=True)  # The nickname before normalization.
    user_id = Column(Integer, ForeignKey("qedler.user_id"))

    qedler = relationship("QEDler", back_populates="nickname_objects")

    def __str__(self):
        return self.original


def create_nickname(nickname, original=None):
    if original is None:
        original = nickname
    return Nickname(nickname=nickname, original=original)


class QEDler(IDMixin, Base):
    user_id = Column(Integer, unique=True)
    forename = Column(String)
    surname = Column(String)

    nickname_objects = relationship("Nickname", back_populates="qedler")

    nicknames = association_proxy("nickname_objects", "nickname", creator=create_nickname)

    @hybrid_property
    def user_name(self):
        return self.forename + self.surname

    @hybrid_property
    def user_name_insensitive(self):
        return (self.forename + self.surname).lower()

    @user_name_insensitive.comparator
    def user_name_insensitive(cls):
        return CaseInsensitiveComparator(cls.forename + cls.surname)


def get_user(nickname: str):
    nickname = normalize_nickname(nickname)
    user = glob.db.session.query(QEDler).filter(QEDler.user_name_insensitive == nickname).one_or_none()
    if user:
        return user
    return glob.db.session.query(Nickname).filter(Nickname.nickname == nickname).one_or_none()
