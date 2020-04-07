from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = orm.relation('User')