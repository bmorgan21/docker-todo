import inspect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy_types import Column, Base, Validate, types, Timestamp

db = SQLAlchemy()
db.Column = Column
db.Timestamp = Timestamp

for k, t in types.__dict__.items():
    if inspect.isclass(t) and issubclass(t, TypeEngine):
        setattr(db, k, t)


class BaseModel(object):
    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()

db.Model = declarative_base(cls=(db.Model, Base, Validate, BaseModel))

from todo import *
from user import *
