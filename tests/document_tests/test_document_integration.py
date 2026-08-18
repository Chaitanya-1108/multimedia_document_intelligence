from app.document.document_analyzer import analyze_document
from app.document.document_extractor import (
    extract_document_from_ocr,
    extract_document_from_pdf,
)
from app.document.document_model import Document, DocumentAnalysis
from app.ocr.ocr_model import OCRResult
from app.pdf_analysis.pdf_model import PDFData


def test_pdf_to_document_to_analysis():
    pdf_data = PDFData(
        path="integration.pdf",
        page_count=1,
        metadata={"title": "Integration Test"},
        text="This is a document integration test.",
    )

    document = extract_document_from_pdf(pdf_data)

    analysis = analyze_document(document)

    assert isinstance(document, Document)
    assert isinstance(analysis, DocumentAnalysis)

    assert document.source == "integration.pdf"
    assert document.document_type == "pdf"
    assert document.page_count == 1

    assert len(document.pages) == 1
    assert document.pages[0].text == (
        "This is a document integration test."
    )

    assert analysis.page_count == 1
    assert analysis.text == (
        "This is a document integration test."
    )
    assert analysis.word_count == 6
    assert analysis.has_text is True

def test_ocr_to_document_to_analysis():
    ocr_result = OCRResult(
        text="OCR integration test",
        confidence=96.5,
        language="eng",
        error=None,
    )

    document = extract_document_from_ocr(
        ocr_result,
        "integration.png",
    )

    analysis = analyze_document(document)

    assert isinstance(document, Document)
    assert isinstance(analysis, DocumentAnalysis)

    assert document.source == "integration.png"
    assert document.document_type == "image"
    assert document.page_count == 1

    assert len(document.pages) == 1
    assert document.pages[0].text == "OCR integration test"

    assert document.metadata["confidence"] == 96.5
    assert document.metadata["language"] == "eng"

    assert analysis.page_count == 1
    assert analysis.text == "OCR integration test"
    assert analysis.word_count == 3
    assert analysis.has_text is True
    
def test_invalid_ocr_data_to_document_to_analysis():

    ocr_result = OCRResult(
        text="",
        confidence=0.0,
        language="eng",
        error="OCR_INVALID_DATA",
    )

    document = extract_document_from_ocr(
        ocr_result,
        "invalid_ocr.png",
    )

    analysis = analyze_document(document)

    assert isinstance(document, Document)
    assert isinstance(analysis, DocumentAnalysis)

    assert document.source == "invalid_ocr.png"
    assert document.document_type == "image"
    assert document.page_count == 1

    assert len(document.pages) == 1
    assert document.pages[0].text == ""

    assert document.metadata["confidence"] == 0.0
    assert document.metadata["language"] == "eng"
    assert document.metadata["error"] == "OCR_INVALID_DATA"

    assert analysis.page_count == 1
    assert analysis.text == ""
    assert analysis.word_count == 0
    assert analysis.has_text is False