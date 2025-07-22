import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

def upload_image(file):
    result = cloudinary.uploader.upload(file.file, folder="blog-images")
    return result["secure_url"]
