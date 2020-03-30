import datetime
import enum
from dataclasses import dataclass
from typing import Type

from sqlalchemy import String, Integer, Boolean, DateTime, Enum, Column
from sqlalchemy.ext.declarative import declared_attr


class IDMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


def type_to_column(typ: Type):
    _LOOKUP = {str: String, int: Integer, bool: Boolean, datetime.datetime: DateTime}
    if typ in _LOOKUP:
        return _LOOKUP[typ]
    if issubclass(typ, enum.Enum):
        return Enum(typ)

    raise TypeError(f"No Column fitting to {typ} found.")


def model_from_data_class(dataklass: dataclass):
    def decorated(klass: Type):
        for k, v in dataklass.__annotations__.items():
            if k not in klass.__dict__:
                setattr(klass, k, v)
        return klass

    return decorated
