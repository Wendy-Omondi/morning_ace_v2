from sqlalchemy import Column, ForeignKey, Integer, Table
from app.db.base_class import Base

# Many to many table
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    extend_existing=True
)
