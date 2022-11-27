from sqlalchemy import Column, Table, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Contact(Base):
    __tablename__ = "Conctact"