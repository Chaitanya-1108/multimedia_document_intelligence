from app.integration.extraction_integrator import integrate_extraction
from app.url_extraction.url_model import URLData


def test_integrate_extraction_preserves_text():
    text = "Visit https://example.com"

    result = integrate_extraction(text)

    assert result.normalized_text == text


def test_integrate_extraction_extracts_url():
    result = integrate_extraction("Visit https://example.com")

    assert len(result.urls) == 1
    assert result.urls[0].url == "https://example.com"


def test_integrate_extraction_supports_multiple_urls():
    text = "Visit https://example.com and https://example.org"

    result = integrate_extraction(text)

    assert len(result.urls) == 2
    assert result.urls[0].domain == "example.com"
    assert result.urls[1].domain == "example.org"


def test_integrate_extraction_returns_empty_urls_when_none_found():
    result = integrate_extraction("This text contains no links.")

    assert result.urls == []


def test_integrate_extraction_handles_empty_text():
    result = integrate_extraction("")

    assert result.normalized_text == ""
    assert result.urls == []


def test_integrate_extraction_returns_url_data_objects():
    result = integrate_extraction("https://example.com")

    assert isinstance(result.urls[0], URLData)