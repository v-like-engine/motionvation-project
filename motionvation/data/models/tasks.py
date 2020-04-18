from sqlalchemy import Column, Integer, String, ForeignKey, orm, Boolean
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    is_performed = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = orm.relation('User')

    category = orm.relation('Category')
