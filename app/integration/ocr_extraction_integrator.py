from app.integration.integration_model import ExtractionResult
from app.ocr.ocr_model import OCRResult
from app.ocr_cleaning.ocr_cleaner import clean_ocr_result

from app.integration.extraction_integrator import integrate_extraction


def integrate_ocr_extraction(result: OCRResult) -> ExtractionResult:
    """Clean an OCR result and integrate its extracted URLs."""

    cleaned_result = clean_ocr_result(result)

    return integrate_extraction(cleaned_result.text)