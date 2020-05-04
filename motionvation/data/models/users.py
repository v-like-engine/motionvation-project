from sqlalchemy import orm, Column, Integer, String, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from ..db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    country = Column(String)
    city = Column(String)
    email = Column(String, index=True, unique=True)
    age = Column(Integer)
    rank = Column(String, default='New')
    hide_email = Column(Boolean, default=False)
    xp = Column(Integer, default=0)
    hashed_password = Column(String)
    number_of_style = Column(Integer)

    notes = orm.relation('Note', back_populates='user')

    categories = orm.relation('Category', back_populates='user')

    tasks = orm.relation('Task', back_populates='user')

    news = orm.relation('News', back_populates='user')

    challenges = orm.relation('Challenge', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)