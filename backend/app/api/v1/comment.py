from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.comment import CommentCreate, CommentOut
from app.db.session import get_db
from app.core.deps import get_current_user
from app.db.models.comment import Comment
from app.db.models.post import Post

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])


@router.post("/", response_model=CommentOut, status_code=201)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
        author_id=user.id,
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


@router.get("/", response_model=list[CommentOut])
async def get_comments(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id)
    )
    return result.scalars().all()