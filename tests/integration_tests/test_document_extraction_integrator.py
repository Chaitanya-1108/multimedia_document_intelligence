from app.document.document_model import Document, DocumentPage
from app.integration.document_extraction_integrator import (
    integrate_document_extraction,
)
from app.integration.integration_model import ExtractionResult
from app.url_extraction.url_model import URLData


def test_integrate_document_extraction_returns_extraction_result():
    document = Document(
        source="test.pdf",
        document_type="pdf",
        page_count=1,
        pages=[
            DocumentPage(
                page_number=1,
                text="Visit https://example.com",
            )
        ],
    )

    result = integrate_document_extraction(document)

    assert isinstance(result, ExtractionResult)


def test_integrate_document_extraction_combines_page_text():
    document = Document(
        source="test.pdf",
        document_type="pdf",
        page_count=2,
        pages=[
            DocumentPage(
                page_number=1,
                text="First page",
            ),
            DocumentPage(
                page_number=2,
                text="Second page",
            ),
        ],
    )

    result = integrate_document_extraction(document)

    assert result.normalized_text == "First page\nSecond page"


def test_integrate_document_extraction_extracts_urls():
    document = Document(
        source="test.pdf",
        document_type="pdf",
        page_count=2,
        pages=[
            DocumentPage(
                page_number=1,
                text="Visit https://example.com",
            ),
            DocumentPage(
                page_number=2,
                text="Visit https://example.org",
            ),
        ],
    )

    result = integrate_document_extraction(document)

    assert len(result.urls) == 2
    assert result.urls[0].domain == "example.com"
    assert result.urls[1].domain == "example.org"


def test_integrate_document_extraction_returns_url_data():
    document = Document(
        source="test.pdf",
        document_type="pdf",
        page_count=1,
        pages=[
            DocumentPage(
                page_number=1,
                text="https://example.com",
            )
        ],
    )

    result = integrate_document_extraction(document)

    assert isinstance(result.urls[0], URLData)


def test_integrate_document_extraction_handles_empty_document():
    document = Document(
        source="empty.pdf",
        document_type="pdf",
        page_count=0,
        pages=[],
    )

    result = integrate_document_extraction(document)

    assert result.normalized_text == ""
    assert result.urls == []


def test_integrate_document_extraction_handles_pages_without_urls():
    document = Document(
        source="test.pdf",
        document_type="pdf",
        page_count=2,
        pages=[
            DocumentPage(
                page_number=1,
                text="This is page one.",
            ),
            DocumentPage(
                page_number=2,
                text="This is page two.",
            ),
        ],
    )

    result = integrate_document_extraction(document)

    assert result.urls == []