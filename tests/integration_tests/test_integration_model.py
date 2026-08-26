from app.integration.integration_model import ExtractionResult
from app.url_extraction.url_model import URLData


def test_extraction_result_stores_normalized_text():
    result = ExtractionResult(
        normalized_text="Visit example.com"
    )

    assert result.normalized_text == "Visit example.com"


def test_extraction_result_defaults_to_empty_urls():
    result = ExtractionResult(
        normalized_text="No URLs here"
    )

    assert result.urls == []


def test_extraction_result_stores_url_data():
    url = URLData(
        url="https://example.com",
        domain="example.com",
        start=0,
        end=19,
    )

    result = ExtractionResult(
        normalized_text="https://example.com",
        urls=[url],
    )

    assert result.urls == [url]


def test_extraction_result_supports_multiple_urls():
    urls = [
        URLData(
            url="https://example.com",
            domain="example.com",
            start=0,
            end=19,
        ),
        URLData(
            url="https://example.org",
            domain="example.org",
            start=20,
            end=39,
        ),
    ]

    result = ExtractionResult(
        normalized_text="https://example.com https://example.org",
        urls=urls,
    )

    assert len(result.urls) == 2
    assert result.urls[0].domain == "example.com"
    assert result.urls[1].domain == "example.org"