from app.document.document_extractor import (
    extract_document_from_ocr,
    extract_document_from_pdf,
)
from app.document.document_model import Document, DocumentPage
from app.ocr.ocr_model import OCRResult
from app.pdf_analysis.pdf_model import PDFData


def test_extract_document_from_pdf():
    pdf_data = PDFData(
        path="sample.pdf",
        page_count=1,
        metadata={"title": "Sample PDF"},
        text="Hello from PDF",
    )

    document = extract_document_from_pdf(pdf_data)

    assert isinstance(document, Document)
    assert document.source == "sample.pdf"
    assert document.document_type == "pdf"
    assert document.page_count == 1
    assert document.metadata["title"] == "Sample PDF"

    assert len(document.pages) == 1
    assert isinstance(document.pages[0], DocumentPage)
    assert document.pages[0].page_number == 1
    assert document.pages[0].text == "Hello from PDF"


def test_extract_document_from_multi_page_pdf():
    pdf_data = PDFData(
        path="multi_page.pdf",
        page_count=3,
        metadata={},
        text="Combined PDF text",
    )

    document = extract_document_from_pdf(pdf_data)

    assert isinstance(document, Document)
    assert document.page_count == 3
    assert document.pages == []


def test_extract_document_from_ocr():
    ocr_result = OCRResult(
        text="Hello from OCR",
        confidence=94.5,
        language="eng",
        error=None,
    )

    document = extract_document_from_ocr(
        ocr_result,
        "test_image.png",
    )

    assert isinstance(document, Document)
    assert document.source == "test_image.png"
    assert document.document_type == "image"
    assert document.page_count == 1

    assert len(document.pages) == 1
    assert document.pages[0].page_number == 1
    assert document.pages[0].text == "Hello from OCR"

    assert document.metadata["confidence"] == 94.5
    assert document.metadata["language"] == "eng"


def test_extract_document_from_ocr_with_error():
    ocr_result = OCRResult(
        text="",
        confidence=0.0,
        language="eng",
        error="TESSERACT_ERROR",
    )

    document = extract_document_from_ocr(
        ocr_result,
        "failed_image.png",
    )

    assert isinstance(document, Document)
    assert document.metadata["confidence"] == 0.0
    assert document.metadata["language"] == "eng"
    assert document.metadata["error"] == "TESSERACT_ERROR"