from unittest import TestCase

from mako.runtime import _populate_self_namespace
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute

from chatbot.database import Base
from chatbot.database.db import DB


class AModel(Base):
    __tablename__ = "_testA"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    bs = relationship("BModel", back_populates="A")

    @hybrid_property
    def has_b(self):
        return self.bs.any()

    @hybrid_method
    def is_named(self, name):
        return self.name == name


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

    def test_property(self):
        a = AModel(name="Luise")
        self.session.add(a)
        self.session.flush()

        self.assertEqual(self.session.query(AModel).filter(AModel.has_b).all(), [])
        self.assertEqual(self.session.query(AModel).filter(AModel.is_named("Luise")).one(), a)
        self.assertEqual(self.session.query(AModel).filter(AModel.is_named("Luke")).count(), 0)

        b = BModel(name="Luke")
        self.session.add(b)
        a.bs.append(b)

        self.assertEqual(self.session.query(AModel).filter(AModel.has_b).one(), a)

    def test_creation(self):
        a = AModel(name="Luise")
        self.session.add(a)
        a.bs = [BModel(name="Luke"), BModel(name="Lukas")]

        self.assertEqual(self.session.query(BModel).count(), 2)
        self.assertEqual(self.session.query(AModel).one().name, "Luise")
