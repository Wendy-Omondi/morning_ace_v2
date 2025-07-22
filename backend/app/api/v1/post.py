from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.orm import selectinload
from app.db.session import get_db

from app.db.models.post import Post
from app.db.models.user import User
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.services.auth import get_current_user
from slugify import slugify

router = APIRouter()

@router.post("/", response_model=PostOut)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    slug = post.slug or slugify(post.title)

    # Check slug is unique
    result = await db.execute(select(Post).where(Post.slug == slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Load tags
    tags = []
    if post.tag_ids:
        tag_q = await db.execute(select(Tag).where(Tag.id.in_(post.tag_ids)))
        tags = tag_q.scalars().all()

    new_post = Post(
        title=post.title,
        content=post.content,
        slug=slug,
        author_id=current_user.id,
        category_id=post.category_id,
        tags=tags,
    )
    
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get("/", response_model=list[PostOut])
async def list_posts(
    db: AsyncSession = Depends(get_db),
    tag: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    query = select(Post).options(
        selectinload(Post.tags),
        selectinload(Post.category)
    )

    if category:
        query = query.join(Post.category).where(Category.name.ilike(category))

    if tag:
        query = query.join(Post.tags).where(Tag.name.ilike(tag))

    result = await db.execute(query)
    posts = result.scalars().unique().all()
    return [PostOut.from_orm_with_html(p) for p in posts]

@router.get("/me", response_model=list[PostOut])
async def get_my_posts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.author_id == current_user.id))
    return result.scalars().all()

@router.get("/{slug}", response_model=PostOut)
async def get_post_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.slug == slug))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    updated: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this post")

    post.title = updated.title
    post.content = updated.content
    post.slug = updated.slug or slugify(updated.title)

    await db.commit()
    await db.refresh(post)
    return PostOut.from_orm_with_html(post)

@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")

    await db.delete(post)
    await db.commit()
    return
