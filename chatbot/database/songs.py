from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from chatbot.bots.utils.youtube import check_valid
from .db import Base
from .utils import IDMixin


class Song(IDMixin, Base):
    video_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    valid = Column(Boolean, server_default="true")

    @hybrid_property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.video_id}"


def check_song_validity(session):
    ret = []
    for i in session.query(Song.video_id).all():
        if not check_valid(i):
            ret.append(i)
            i.valid = False

    return ret
