from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from array_ex import MutableList

Base = declarative_base()

class Contact(Base):
    __tablename__ = "Conctact"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    telephone = Column(Integer)
    owner = Column(Integer, nullable=False) 
    shared = Column(MutableList.as_mutable(ARRAY(Integer)))