import datetime
import enum
from dataclasses import dataclass
from functools import wraps
from typing import Type, Union

from sqlalchemy import String, Integer, Boolean, DateTime, Enum, Column, func, types
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import Comparator
from sqlalchemy.sql import expression

from chatbot.database.db import database
from chatbot.interface.message_helpers import Color


def inject_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "session" not in kwargs:
            with database.context as session:
                return f(*args, session=session, **kwargs)
        else:
            return f(*args, **kwargs)

    return decorated


class ColorColumn(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, value: Color, dialect) -> str:
        return value.to_hex()

    def process_result_value(self, value: str, dialect) -> Color:
        return Color(value)

    def copy(self, **kw):
        return ColorColumn(self.impl.length)


class IDMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    _column_id = Column(Integer, primary_key=True)


def unwrap_optional(typ):
    for i in typ.__args__:
        if not isinstance(None, i):
            return i
    raise ValueError(f"{typ} has only NoneTypes.")


def type_to_column(typ):
    _LOOKUP = {str: String, int: Integer, bool: Boolean, datetime.datetime: DateTime, Color: ColorColumn}
    if hasattr(typ, "__origin__") and typ.__origin__ == Union:
        typ = unwrap_optional(typ)
    if typ in _LOOKUP:
        return Column(_LOOKUP[typ])
    if issubclass(typ, enum.Enum):
        return Column(Enum(typ))

    raise TypeError(f"No Column fitting to {typ} found.")


def model_from_data_class(dataklass: dataclass):
    def decorated(klass: Type):
        for k, v in dataklass.__annotations__.items():
            if k not in klass.__dict__:
                setattr(klass, k, type_to_column(v))

        def construct(cls, dataobject: dataklass, *args, **kwargs) -> klass:
            return cls(*args, **kwargs, **dataobject.__dict__)

        klass.construct = classmethod(construct)

        def convert(self) -> dataklass:
            d = dict((key, getattr(self, key)) for key in dataklass.__annotations__)
            return dataklass(**d)

        klass.convert = convert

        return klass

    return decorated


def normalize_nickname(nickname: str):
    return nickname.strip().lower()


class CaseInsensitiveComparator(Comparator):
    def reverse_operate(self, op, other, **kwargs):
        return op(func.lower(other), func.lower(self.__clause_element__()))

    def operate(self, op, *other, **kwargs):
        return op(func.lower(self.__clause_element__()), func.lower(other))


class NicknameColumn(types.TypeDecorator):
    impl = types.String

    def process_bind_param(self, nickname: str, dialect) -> str:
        return normalize_nickname(nickname)

    def process_result_value(self, db_entry: str, dialect) -> str:
        return db_entry

    def copy(self, **kw):
        return NicknameColumn(self.impl.length)


class UTCNow(expression.FunctionElement):
    type = DateTime()


@compiles(UTCNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(UTCNow, 'mssql')
def ms_utcnow(element, compiler, **kw):
    return "GETUTCDATE()"
