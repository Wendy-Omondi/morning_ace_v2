from pydantic import BaseModel
from typing import Optional, List

from app.schemas.tag import TagOut
from app.schemas.category import CategoryOut

class PostCreate(BaseModel):
    title: str
    content: str
    slug: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    content_html: str
    author_id: int
    tags: List[TagOut]
    category: Optional[CategoryOut]

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm_with_html(post):
        return PostOut(
            id=post.id,
            title=post.title,
            slug=post.slug,
            content=post.content,
            content_html=markdown(post.content),
            author_id=post.author_id,
            tags=post.tags,
            category=post.category,
        )

class PostUpdate(BaseModel):
    title: str
    content: str
    slug: Optional[str] = None
