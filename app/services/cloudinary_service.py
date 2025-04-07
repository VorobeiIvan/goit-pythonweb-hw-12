import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_avatar(file):
    """
    Uploads an avatar to Cloudinary.

    Args:
        file: The file to upload.

    Returns:
        str: The URL of the uploaded image.
    """
    result = cloudinary.uploader.upload(file.file, folder="avatars")
    return result["secure_url"]
