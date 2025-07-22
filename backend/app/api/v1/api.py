from fastapi import APIRouter
from app.api.v1 import auth, post, tag, category

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(post.router, prefix="/posts", tags=["Posts"])
api_router.include_router(tag.router)
api_router.include_router(category.router)
