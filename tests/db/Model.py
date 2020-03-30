from unittest import TestCase

from mako.runtime import _populate_self_namespace
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from chatbot.database import Base
from chatbot.database.db import DB


class AModel(Base):
    __tablename__ = "_testA"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bs = relationship("BModel", back_populates="A")


class BModel(Base):
    __tablename__ = "_testB"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    a_id = Column(Integer, ForeignKey("_testA.id"))

    A = relationship("AModel", back_populates="bs")


class TestModel(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = DB()
        self.db.create_all()

    def setUp(self) -> None:
        self.session = self.db.session

    def tearDown(self) -> None:
        self.session.rollback()

    def test_creation(self):
        a = AModel(name="Luise")
        self.session.add(a)
        a.bs = [BModel(name="Luke"), BModel(name="Lukas")]

        self.assertEqual(self.session.query(BModel).count(), 2)
        self.assertEqual(self.session.query(AModel).one().name, "Luise")
