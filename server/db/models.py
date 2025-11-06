from math import fabs
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# Base for models
Base = declarative_base()

# User model
class UserDB(Base): 
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'User(name={self.username}), email={self.email})'