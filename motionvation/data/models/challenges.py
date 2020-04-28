from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, orm
from sqlalchemy_serializer import SerializerMixin

from motionvation.data.db_session import SqlAlchemyBase


class Challenge(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    required = Column(Integer)
    current = Column(Integer)
    add_task = Column(Boolean)
    delete_task = Column(Boolean)
    do_task = Column(Boolean)
    add_note = Column(Boolean)
    delete_note = Column(Boolean)
    do_challenge = Column(Boolean)
    get_level = Column(Boolean)
    get_xp = Column(Boolean)
    difficulty = Column(Integer)

    user = orm.relation('User')
