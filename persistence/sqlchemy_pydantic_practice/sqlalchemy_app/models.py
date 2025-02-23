from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    posts = relationship("Post", back_populates="owner", cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

"""
No.3.1 Add a Post Table and Create a Relationship

Define a new Post model with a foreign key to User.
Establish a relationship between User and Post.
Ensure users can have multiple posts.

"""
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))   
    owner = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(title={self.title}, user_id={self.user_id})>"