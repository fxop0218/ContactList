from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
from array_ex import MutableList
Base = declarative_base()

class User(Base):
    __tablename__ = "user_"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    contact_id = Column(MutableList.as_mutable(ARRAY(Integer)))