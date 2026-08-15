from pathlib import Path

import cv2

from app.input.file_validator import validate_file
from app.image.image_model import ImageData


def load_image(file_path: Path) -> tuple[bool, ImageData | str]:
    # Validate the file before attempting to load it
    is_valid, error = validate_file(file_path)

    if not is_valid:
        return False, error

    # Load the image using OpenCV
    image = cv2.imread(str(file_path))

    # OpenCV returns None if the image cannot be decoded
    if image is None:
        return False, "INVALID_IMAGE"

    # Extract image dimensions
    height, width, channels = image.shape

    # Extract the image format from the file extension
    image_format = file_path.suffix.replace(".", "").upper()

    # Create the image metadata object
    image_data = ImageData(
        path=str(file_path),
        format=image_format,
        width=width,
        height=height,
        channels=channels,
    )

    return True, image_data