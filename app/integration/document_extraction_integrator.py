from app.document.document_model import Document
from app.integration.extraction_integrator import integrate_extraction
from app.integration.integration_model import ExtractionResult


def integrate_document_extraction(document: Document) -> ExtractionResult:
    """Extract text from document pages and integrate URL extraction."""

    text = "\n".join(page.text for page in document.pages)

    return integrate_extraction(text)