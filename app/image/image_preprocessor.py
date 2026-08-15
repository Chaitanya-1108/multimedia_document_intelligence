import cv2
import numpy as np


def preprocess_image(
    image: np.ndarray,
    mode: str = "general"
) -> np.ndarray:
    """
    Preprocess an image for downstream OCR or QR detection.

    Modes:
        general:
            Grayscale, resize, and light denoising.

        ocr:
            Grayscale, resize, denoising, contrast enhancement,
            and adaptive thresholding.

        qr:
            Grayscale, resize, and light denoising without
            aggressive thresholding.

    Args:
        image: OpenCV image represented as a NumPy array.
        mode: Preprocessing mode.

    Returns:
        Preprocessed image.

    Raises:
        ValueError: If an unsupported preprocessing mode is provided.
    """

    supported_modes = {"general", "ocr", "qr"}

    if mode not in supported_modes:
        raise ValueError(
            f"Unsupported preprocessing mode: {mode}"
        )

    # Create a copy so the original image remains unchanged
    processed_image = image.copy()

    # Convert color image to grayscale
    if len(processed_image.shape) == 3:
        processed_image = cv2.cvtColor(
            processed_image,
            cv2.COLOR_BGR2GRAY
        )

    # Resize small images
    height, width = processed_image.shape[:2]

    min_width = 1200

    if width < min_width:
        scale = min_width / width

        new_width = int(width * scale)
        new_height = int(height * scale)

        processed_image = cv2.resize(
            processed_image,
            (new_width, new_height),
            interpolation=cv2.INTER_CUBIC
        )

    # Apply light denoising
    processed_image = cv2.GaussianBlur(
        processed_image,
        (3, 3),
        0
    )

    # OCR-specific preprocessing
    if mode == "ocr":

        # Improve local contrast
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        processed_image = clahe.apply(
            processed_image
        )

        # Convert to a high-contrast binary image
        processed_image = cv2.adaptiveThreshold(
            processed_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

    return processed_image