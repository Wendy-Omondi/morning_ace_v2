from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.models.associations import post_tags

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    author = relationship("app.db.models.user.User", back_populates="posts")
    comments = relationship("app.db.models.comment.Comment", back_populates="post")

    tags = relationship("app.db.models.tag.Tag", secondary=post_tags, back_populates="posts")
    category = relationship("app.db.models.category.Category", back_populates="posts")
