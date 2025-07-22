from fastapi import APIRouter, Depends
from sqlalchemy import func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.deps import get_current_admin_user
from app.db.models.post import Post
from app.db.models.user import User
from app.db.models.tag import Tag
from app.db.models.category import Category

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin_user)
):
    # Total counts
    total_posts = await db.scalar(func.count(Post.id))
    total_users = await db.scalar(func.count(User.id))

    # Most used tag
    most_used_tag = await db.execute(
        func.count(Tag.id)
        .select()
        .join(Post.tags)
        .group_by(Tag.id)
        .order_by(desc(func.count()))
        .limit(1)
    )
    most_used_tag = most_used_tag.scalar()

    # Most used category
    most_used_cat = await db.execute(
        func.count(Category.id)
        .select()
        .join(Post)
        .group_by(Category.id)
        .order_by(desc(func.count()))
        .limit(1)
    )
    most_used_cat = most_used_cat.scalar()

    # Most recent post
    recent_post = await db.execute(
        Post.__table__.select().order_by(Post.created_at.desc()).limit(1)
    )
    recent_post = recent_post.fetchone()

    return {
        "total_posts": total_posts,
        "total_users": total_users,
        "most_used_tag": most_used_tag,
        "most_used_category": most_used_cat,
        "recent_post": {
            "id": recent_post.id if recent_post else None,
            "title": recent_post.title if recent_post else None,
            "created_at": recent_post.created_at if recent_post else None,
        }
    }
