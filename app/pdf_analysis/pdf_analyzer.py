from app.pdf_analysis.pdf_model import PDFAnalysis, PDFData


def analyze_pdf(pdf_data: PDFData) -> PDFAnalysis:

    text = pdf_data.text.strip()

    character_count = len(text)

    word_count = len(text.split()) if text else 0

    has_text = bool(text)

    return PDFAnalysis(
        page_count=pdf_data.page_count,
        text=pdf_data.text,
        character_count=character_count,
        word_count=word_count,
        has_text=has_text,
    )