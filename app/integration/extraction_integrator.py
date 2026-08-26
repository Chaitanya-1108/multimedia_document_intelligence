from app.integration.integration_model import ExtractionResult
from app.url_extraction.url_extractor import extract_urls


def integrate_extraction(text: str) -> ExtractionResult:
    """Integrate normalized text with URL extraction results."""

    urls = extract_urls(text)

    return ExtractionResult(
        normalized_text=text,
        urls=urls,
    )