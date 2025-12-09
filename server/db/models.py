from sqlalchemy.orm import declarative_base, relationship
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

class WorldDB(Base):
    __tablename__ = "world"
    id = Column(Integer, primary_key=True)
    world = Column(JSON, nullable=False)

    stories = relationship("UserStoryDB", back_populates="world", cascade="all, delete-orphan")

class UserStoryDB(Base):
    __tablename__ = "user_stories"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    prompt = Column(String(120), nullable=False)
    world_id = Column(Integer, ForeignKey("world.id"), nullable=False)

    world = relationship("WorldDB", back_populates="stories")

    def __repr__(self) -> str:
        return f"""UserStory(id={self.id}, user_id={self.user_id}, title={self.title}, 
        tag_id={self.tag_id}, prompt={self.prompt}, world_id={self.world_id})"""
    