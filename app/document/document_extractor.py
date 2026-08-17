from app.document.document_model import Document, DocumentPage
from app.ocr.ocr_model import OCRResult
from app.pdf_analysis.pdf_model import PDFData


def extract_document_from_pdf(pdf_data: PDFData) -> Document:
    pages = []

    if pdf_data.page_count == 1:
        pages.append(
            DocumentPage(
                page_number=1,
                text=pdf_data.text,
            )
        )

    return Document(
        source=pdf_data.path,
        document_type="pdf",
        page_count=pdf_data.page_count,
        pages=pages,
        metadata=pdf_data.metadata,
    )


def extract_document_from_ocr(
    ocr_result: OCRResult,
    source: str,
) -> Document:
    page = DocumentPage(
        page_number=1,
        text=ocr_result.text,
    )

    metadata = {
        "confidence": ocr_result.confidence,
        "language": ocr_result.language,
    }

    if ocr_result.error:
        metadata["error"] = ocr_result.error

    return Document(
        source=source,
        document_type="image",
        page_count=1,
        pages=[page],
        metadata=metadata,
    )