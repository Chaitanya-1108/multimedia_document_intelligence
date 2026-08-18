from pathlib import Path
from unittest.mock import patch

import pytesseract
import cv2

from app.ocr.ocr_engine import run_ocr, run_ocr_data


def test_run_ocr():
    image_path = Path(__file__).resolve().parent.parent / "assets" / "test_ocr.png"

    image = cv2.imread(str(image_path))

    assert image is not None

    text = run_ocr(image)

    assert isinstance(text, str)
    assert len(text) > 0
    
def test_run_ocr_data():
    image_path = Path(__file__).resolve().parent.parent / "assets" / "test_ocr.png"

    assert image_path.exists()

    image = cv2.imread(str(image_path))

    assert image is not None

    data = run_ocr_data(image)

    assert isinstance(data, dict)

    assert "text" in data
    assert "conf" in data

def test_run_ocr_data_handles_tesseract_not_found():

    with patch(
        "app.ocr.ocr_engine.pytesseract.image_to_data",
        side_effect=pytesseract.TesseractNotFoundError()
    ):

        try:
            run_ocr_data(None)
            assert False, "Expected RuntimeError"
        except RuntimeError as error:
            assert str(error) == "TESSERACT_NOT_FOUND"


def test_run_ocr_data_handles_ocr_failure():

    with patch(
        "app.ocr.ocr_engine.pytesseract.image_to_data",
        side_effect=Exception("Unexpected OCR failure")
    ):

        try:
            run_ocr_data(None)
            assert False, "Expected RuntimeError"
        except RuntimeError as error:
            assert str(error) == "OCR_FAILED"
            
def test_run_ocr_data_passes_language_to_tesseract():

    expected_data = {
        "text": ["Hello"],
        "conf": ["95.0"]
    }

    with patch(
        "app.ocr.ocr_engine.pytesseract.image_to_data",
        return_value=expected_data
    ) as mock_ocr:

        result = run_ocr_data(
            None,
            language="eng"
        )

    assert result == expected_data

    mock_ocr.assert_called_once_with(
        None,
        lang="eng",
        output_type=pytesseract.Output.DICT
    )