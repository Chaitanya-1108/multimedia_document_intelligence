from app.ocr.ocr_model import OCRResult

from app.ocr_cleaning.text_cleaner import clean_text


def clean_ocr_result(result: OCRResult) -> OCRResult:
    """
    Clean the text contained in an OCRResult while preserving
    OCR metadata and error information.

    Args:
        result: OCRResult containing raw OCR output.

    Returns:
        OCRResult with normalized text and preserved metadata.

    Raises:
        TypeError: If result is not an OCRResult.
    """
    if not isinstance(result, OCRResult):
        raise TypeError("result must be an OCRResult")

    return OCRResult(
        text=clean_text(result.text),
        confidence=result.confidence,
        language=result.language,
        error=result.error,
    )