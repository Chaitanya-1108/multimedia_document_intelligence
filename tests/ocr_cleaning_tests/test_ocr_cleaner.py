import pytest

from app.ocr.ocr_model import OCRResult
from app.ocr_cleaning.ocr_cleaner import clean_ocr_result


def test_clean_ocr_result_cleans_text():
    result = OCRResult(
        text="   Hello     World   ",
        confidence=91.5,
        language="eng",
        error=None,
    )

    cleaned = clean_ocr_result(result)

    assert cleaned.text == "Hello World"


def test_clean_ocr_result_preserves_confidence():
    result = OCRResult(
        text="  Hello World  ",
        confidence=87.5,
        language="eng",
        error=None,
    )

    cleaned = clean_ocr_result(result)

    assert cleaned.confidence == 87.5


def test_clean_ocr_result_preserves_language():
    result = OCRResult(
        text="  Hello World  ",
        confidence=87.5,
        language="fra",
        error=None,
    )

    cleaned = clean_ocr_result(result)

    assert cleaned.language == "fra"


def test_clean_ocr_result_preserves_error():
    result = OCRResult(
        text="",
        confidence=0.0,
        language="eng",
        error="OCR_INVALID_DATA",
    )

    cleaned = clean_ocr_result(result)

    assert cleaned.error == "OCR_INVALID_DATA"


def test_clean_ocr_result_returns_ocr_result():
    result = OCRResult(
        text="  Hello World  ",
        confidence=90.0,
        language="eng",
        error=None,
    )

    cleaned = clean_ocr_result(result)

    assert isinstance(cleaned, OCRResult)


def test_clean_ocr_result_preserves_url():
    result = OCRResult(
        text="Visit   https://example.com/login?id=123",
        confidence=95.0,
        language="eng",
        error=None,
    )

    cleaned = clean_ocr_result(result)

    assert cleaned.text == "Visit https://example.com/login?id=123"


def test_clean_ocr_result_rejects_invalid_input():
    with pytest.raises(TypeError):
        clean_ocr_result(None)