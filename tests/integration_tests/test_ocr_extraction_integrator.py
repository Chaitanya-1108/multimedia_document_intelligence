import pytest

from app.integration.ocr_extraction_integrator import integrate_ocr_extraction
from app.integration.integration_model import ExtractionResult
from app.ocr.ocr_model import OCRResult
from app.url_extraction.url_model import URLData


def test_integrate_ocr_extraction_returns_extraction_result():
    result = OCRResult(
        text="Visit https://example.com",
        confidence=0.95,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert isinstance(integrated, ExtractionResult)


def test_integrate_ocr_extraction_cleans_text_before_extraction():
    result = OCRResult(
        text="  Visit   https://example.com   ",
        confidence=0.95,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert integrated.normalized_text == "Visit https://example.com"


def test_integrate_ocr_extraction_extracts_urls():
    result = OCRResult(
        text="Visit https://example.com",
        confidence=0.95,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert len(integrated.urls) == 1
    assert integrated.urls[0].url == "https://example.com"


def test_integrate_ocr_extraction_supports_multiple_urls():
    result = OCRResult(
        text="https://example.com and https://example.org",
        confidence=0.95,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert len(integrated.urls) == 2
    assert integrated.urls[0].domain == "example.com"
    assert integrated.urls[1].domain == "example.org"


def test_integrate_ocr_extraction_handles_empty_text():
    result = OCRResult(
        text="",
        confidence=0.0,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert integrated.normalized_text == ""
    assert integrated.urls == []


def test_integrate_ocr_extraction_returns_url_data():
    result = OCRResult(
        text="https://example.com",
        confidence=0.95,
        language="en",
    )

    integrated = integrate_ocr_extraction(result)

    assert isinstance(integrated.urls[0], URLData)


def test_integrate_ocr_extraction_rejects_invalid_input():
    with pytest.raises(TypeError):
        integrate_ocr_extraction("not an OCRResult")