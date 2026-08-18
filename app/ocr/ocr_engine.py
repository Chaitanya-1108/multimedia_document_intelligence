import pytesseract

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def run_ocr(processed_image):
    """
    Run Tesseract OCR on a processed image.

    Args:
        processed_image: OpenCV image prepared for OCR.

    Returns:
        Extracted text as a string.

    Raises:
        RuntimeError: If Tesseract OCR fails.
    """

    try:
        text = pytesseract.image_to_string(processed_image)

        return text.strip()

    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError("TESSERACT_NOT_FOUND") from error

    except Exception as error:
        raise RuntimeError("OCR_FAILED") from error
    
def run_ocr_data(processed_image, language="eng"):
    """
    Run Tesseract OCR and return structured OCR data.

    Args:
        processed_image: OpenCV image prepared for OCR.
        language: Tesseract language code.

    Returns:
        Dictionary containing OCR text, confidence, and positional data.

    Raises:
        RuntimeError: If Tesseract OCR fails.
    """

    try:
        data = pytesseract.image_to_data(
            processed_image,
            lang=language,
            output_type=pytesseract.Output.DICT
        )

        return data

    except pytesseract.TesseractNotFoundError as error:
        raise RuntimeError("TESSERACT_NOT_FOUND") from error

    except Exception as error:
        raise RuntimeError("OCR_FAILED") from error