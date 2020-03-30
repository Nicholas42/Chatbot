from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session

from chatbot import config
from chatbot.config import adapt_config
from chatbot.database import Base


class DB:
    def __init__(self, _config=None):
        if _config is None:
            _config = config
        self.active = _config["db"]["active"]
        conf = adapt_config(_config[self.active], _config[self.active]["adaptor"])

        self.engine = create_engine(**conf)
        self._session_class = sessionmaker(bind=self.engine)

    @property
    def session(self) -> Session:
        return self._session_class()

    def create_all(self, base: DeclarativeMeta = Base):
        base.metadata.create_all(self.engine)
