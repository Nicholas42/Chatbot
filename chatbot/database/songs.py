from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base
from .utils import IDMixin
from .. import glob
from ..bots.utils.youtube import check_valid


class Song(IDMixin, Base):
    video_id = Column(String, unique=True)
    title = Column(String)

    @hybrid_property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.video_id}"


glob.db.create_all()


def check_song_validity():
    ret = {}
    with glob.db.context as session:
        for i in session.query(Song.video_id).all():
            ret[i] = check_valid(i)

    return ret
