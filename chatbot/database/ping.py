import datetime

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from chatbot import glob
from chatbot.database import Base
from chatbot.database.nickname import get_user, QEDler, create_nickname
from chatbot.database.utils import IDMixin, utcnow

MIN_DATE = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)


class Ping(IDMixin, Base):
    user_id = Column(Integer, ForeignKey("qedler.user_id"))
    target_id = Column(Integer, ForeignKey("nickname._column_id"))
    message = Column(Text, nullable=False)
    ping_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=utcnow())
    sender = Column(String, nullable=False)
    activation_time = Column(TIMESTAMP(timezone=True), server_default=utcnow(), nullable=False)

    user = relationship("QEDler", back_populates="pings")
    target = relationship("Nickname", back_populates="pings")

    @hybrid_property
    def is_active(self):
        return self.activation_time > datetime.datetime.now(datetime.timezone.utc)


# Does NOT destroy the pings!
def get_pings(session, targetname, user_id=None):
    ret = []
    if session is None:
        session = glob.db.session

    target = get_user(session, targetname)
    user_id = user_id if user_id is not None or target is None else target.user_id
    if user_id is not None:
        ret.extend(i for i in session.query(QEDler).filter(QEDler.user_id == user_id).scalar().pings if i.is_active)

    if target:
        ret.extend(i for i in target.pings if i.is_active)
    return set(ret)


def create_ping(session, targetname, **kwargs):
    target = get_user(session, targetname)
    target = session.merge(target)
    p = Ping(**kwargs)
    if isinstance(target, QEDler):
        p.user = target
    else:
        if target is None:
            target = create_nickname(targetname)
            session.add(target)
        p.target = target
        p.user_id = target.user_id
    session.add(p)
    return p
