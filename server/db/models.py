from math import fabs
from sqlalchemy.orm import declarative_base
from sqlalchemy import JSON, Column, ForeignKey, Integer, String

# Base for models
Base = declarative_base()


# User model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"User(name={self.username}), email={self.email})"


class TagsDB(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Tags(tag={self.tag})"
