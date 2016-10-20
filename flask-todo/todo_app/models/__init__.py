import inspect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy_types import Column, Base, Validate, types, Timestamp

from todo_app import app

db = SQLAlchemy(app)
db.Column = Column
db.Timestamp = Timestamp

for k, t in types.__dict__.items():
    if inspect.isclass(t) and issubclass(t, TypeEngine):
        setattr(db, k, t)

db.Model = declarative_base(cls=(db.Model, Base, Validate))

from todo import *
