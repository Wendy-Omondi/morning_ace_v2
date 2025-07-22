from fastapi import APIRouter, UploadFile, File, Depends
from app.utils.cloudinary_upload import upload_image

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/image")
async def upload_blog_image(file: UploadFile = File(...)):
    url = upload_image(file)
    return {"url": url}
