# defines the database models using SQLAlchemy's ORM - models are Python classes that represent database tables
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default= 'TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    owner = relationship("User") # defines a relationship between the Post and User models - allows us to access the user who created a post using post.owner - SQLAlchemy will automatically handle the join between the posts and users tables based on the foreign key relationship defined by owner_id
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key=True)