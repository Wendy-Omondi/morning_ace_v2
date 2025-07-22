from fastapi import FastAPI
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db import base
from app.api.v1 import auth, post, comment, dashboard

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}


@app.get("/db-check")
async def check_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"db_working": result.scalar() == 1}

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(post.router, prefix="/api/v1/posts")
app.include_router(comment.router)
app.include_router(dashboard.router)
