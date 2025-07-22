from app.db.base_class import Base
from app.db.models.associations import post_tags  # for alembic to pick it up
from app.db.models.user import User
from app.db.models.comment import Comment
from app.db.models.category import Category
from app.db.models.tag import Tag
from app.db.models.post import Post
