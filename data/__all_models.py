import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False)
    chatid = sqlalchemy.Column(sqlalchemy.String,
                               nullable=False)
