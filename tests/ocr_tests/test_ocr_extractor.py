from pathlib import Path
from unittest.mock import patch
import cv2

from app.ocr.ocr_extractor import extract_text
from app.ocr.ocr_model import OCRResult


def test_extract_text():
    image_path = Path(__file__).resolve().parent.parent / "assets" / "test_ocr.png"

    assert image_path.exists()

    image = cv2.imread(str(image_path))

    assert image is not None

    result = extract_text(image)

    assert isinstance(result, OCRResult)

    assert isinstance(result.text, str)
    assert len(result.text) > 0

    assert isinstance(result.confidence, float)
    assert result.confidence >= 0

    assert result.language == "eng"
    assert result.error is None
    
def test_extract_text_handles_ocr_failure():

    with patch(
        "app.ocr.ocr_extractor.run_ocr_data",
        side_effect=RuntimeError("OCR_FAILED")
    ):

        result = extract_text(None, language="eng")

    assert result.text == ""
    assert result.confidence == 0.0
    assert result.language == "eng"
    assert result.error == "OCR_FAILED"