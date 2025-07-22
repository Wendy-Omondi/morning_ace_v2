from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.schemas.tag import TagOut
from app.db.models.tag import Tag

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=List[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag))
    return result.scalars().all()
