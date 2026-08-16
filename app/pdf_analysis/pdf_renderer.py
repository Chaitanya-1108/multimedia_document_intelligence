import fitz
import cv2
import numpy as np
from pathlib import Path

from app.input.file_validator import validate_file


def render_pdf_page(
    file_path: Path,
    page_number: int = 0
) -> tuple[bool, np.ndarray | str]:

    # Validate the file before rendering
    is_valid, error = validate_file(file_path)

    if not is_valid:
        return False, error

    try:
        # Open the PDF
        document = fitz.open(str(file_path))

        # Validate page number
        if page_number < 0 or page_number >= len(document):
            document.close()
            return False, "INVALID_PAGE_NUMBER"

        # Get the requested page
        page = document[page_number]

        # Render page to a pixmap
        pixmap = page.get_pixmap()

        # Convert pixmap bytes to NumPy array
        image_array = np.frombuffer(
            pixmap.samples,
            dtype=np.uint8
        )

        # Determine the correct image shape
        if pixmap.alpha:
            image = image_array.reshape(
                pixmap.height,
                pixmap.width,
                4
            )

            image = cv2.cvtColor(
                image,
                cv2.COLOR_RGBA2BGR
            )

        else:
            image = image_array.reshape(
                pixmap.height,
                pixmap.width,
                3
            )

            image = cv2.cvtColor(
                image,
                cv2.COLOR_RGB2BGR
            )

        document.close()

        return True, image

    except Exception:
        return False, "PDF_RENDER_ERROR"