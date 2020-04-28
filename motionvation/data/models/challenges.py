from sqlalchemy import Column, Integer, String, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class Challenge(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    required = Column(Integer)
    current = Column(Integer)
    add_task = Column(Integer)
    delete_task = Column(Integer)
    do_task = Column(Integer)
    add_note = Column(Integer)
    delete_note = Column(Integer)
    do_challenge = Column(Integer)
    get_level = Column(Integer)
    get_xp = Column(Integer)
    difficulty = Column(Integer)

    user = orm.relation('User')
