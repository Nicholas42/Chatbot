from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base
from .utils import IDMixin
from .. import glob


class Song(IDMixin, Base):
    video_id = Column(String)
    title = Column(String)

    @hybrid_property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.video_id}"


glob.db.create_all()
