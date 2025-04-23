from db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import *


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    tasks = relationship('Task', back_populates='user', uselist=True, cascade="all, delete-orphan",)
