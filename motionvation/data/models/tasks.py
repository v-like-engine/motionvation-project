from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = orm.relation('User')

    category = orm.relation('Category')
