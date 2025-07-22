from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.schemas.tag import TagCreate, TagOut
from app.db.models.tag import Tag
from app.core.deps import get_current_admin_user

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=TagOut)
async def create_tag(
    tag: TagCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin_user)  # ⬅️ restrict to admin only
):
    result = await db.execute(select(Tag).where(Tag.name == tag.name))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")

    new_tag = Tag(name=tag.name)
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag

@router.get("/", response_model=List[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag))
    return result.scalars().all()
