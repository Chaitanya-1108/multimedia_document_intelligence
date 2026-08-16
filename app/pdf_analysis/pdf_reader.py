import fitz
from pathlib import Path

from app.input.file_validator import validate_file
from app.pdf_analysis.pdf_model import PDFData


def read_pdf(file_path: Path) -> tuple[bool, PDFData | str]:
    # Validate the file before attempting to read it
    is_valid, error = validate_file(file_path)

    if not is_valid:
        return False, error

    try:
        # Open the PDF using PyMuPDF
        document = fitz.open(str(file_path))

        # Extract page count
        page_count = len(document)

        # Extract PDF metadata
        metadata = document.metadata

        # Extract text from every page
        text_parts = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                text_parts.append(page_text)

        # Combine all extracted page text
        extracted_text = "\n".join(text_parts)

        # Close the PDF document
        document.close()

        # Create the PDF data object
        pdf_data = PDFData(
            path=str(file_path),
            page_count=page_count,
            metadata=metadata,
            text=extracted_text,
        )

        return True, pdf_data

    except Exception:
        return False, "INVALID_PDF"