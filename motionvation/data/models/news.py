from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)

    user = orm.relation('User')
