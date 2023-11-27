from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Label(Base):
    __tablename__ = 'label'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    desc = Column(String)
    
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    
    
     