from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, Session

from chatbot import glob
from chatbot.config import adapt_config


class DB:
    def __init__(self, _config=None):
        if _config is None:
            _config = glob.config
        self.active = _config["db"]["active"]
        conf = adapt_config(_config[self.active], _config[self.active]["adaptor"])

        self.engine = create_engine(self._create_url(conf))
        self._session_class = sessionmaker(bind=self.engine)

    @property
    def session(self) -> Session:
        return self._session_class()

    @staticmethod
    def _create_url(conf):
        _URL_ARGS = ["drivername", "username", "password", "host", "port", "database", "query"]
        return URL(**dict((i, conf.get(i)) for i in _URL_ARGS))

    @property
    def context(self):
        return self.Context(self.session)

    class Context:
        def __init__(self, session: Session):
            self.session: Session = session

        def __enter__(self):
            return self.session

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()

            self.session.close()
