import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary with environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),  # Cloudinary cloud name
    api_key=os.getenv("CLOUDINARY_API_KEY"),  # Cloudinary API key
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),  # Cloudinary API secret
)


def upload_avatar(file):
    """
    Uploads an avatar image to Cloudinary.

    This function takes a file object, uploads it to the Cloudinary service
    under the "avatars" folder, and returns the secure URL of the uploaded image.

    Args:
        file: The file object to upload. It should have a `file` attribute
              that contains the file data.

    Returns:
        str: The secure URL of the uploaded image hosted on Cloudinary.

    Raises:
        cloudinary.exceptions.Error: If the upload fails for any reason.
    """
    # Upload the file to Cloudinary under the "avatars" folder
    result = cloudinary.uploader.upload(file.file, folder="avatars")

    # Return the secure URL of the uploaded image
    return result["secure_url"]
