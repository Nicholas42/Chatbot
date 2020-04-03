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

    user = relationship("QEDler", back_populate="pings")
    target = relationship("Nickname", back_populate="pings")

    @hybrid_property
    def is_active(self):
        return self.activation_time > datetime.datetime.now(datetime.timezone.utc)


# Does NOT destroy the pings!
def get_ping(targetname, user_id=None, session=None):
    ret = []
    if session is None:
        session = glob.db.session

    if user_id is not None:
        ret.extend(session.query(QEDler.pings).filter(QEDler.user_id == user_id).filter(Ping.is_active).all())

    target = get_user(targetname)
    if target and not (user_id is not None and target.user_id == user_id):
        ret.extend(target.pings.filter(Ping.is_active))
    return ret


def create_ping(targetname, **kwargs):
    target = get_user(targetname)
    with glob.db.context as session:
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
