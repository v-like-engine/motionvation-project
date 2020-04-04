from sqlalchemy import orm, Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from ..db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    age = Column(Integer, nullable=True)
    hashed_password = Column(String, nullable=True)

    notes = orm.relation('Note', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)