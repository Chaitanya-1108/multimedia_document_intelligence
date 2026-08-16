from app.pdf_analysis.pdf_analyzer import analyze_pdf
from app.pdf_analysis.pdf_model import PDFData


def test_analyze_pdf():

    pdf_data = PDFData(
        path="test.pdf",
        page_count=3,
        metadata={
            "title": "Test Document"
        },
        text="This is a test PDF document."
    )

    result = analyze_pdf(pdf_data)

    assert result.page_count == 3
    assert result.text == "This is a test PDF document."
    assert result.character_count == 28
    assert result.word_count == 6
    assert result.has_text is True


def test_analyze_empty_text():

    pdf_data = PDFData(
        path="empty.pdf",
        page_count=2,
        metadata={},
        text=""
    )

    result = analyze_pdf(pdf_data)

    assert result.page_count == 2
    assert result.text == ""
    assert result.character_count == 0
    assert result.word_count == 0
    assert result.has_text is False


def test_analyze_whitespace_text():

    pdf_data = PDFData(
        path="whitespace.pdf",
        page_count=1,
        metadata={},
        text="   \n   "
    )

    result = analyze_pdf(pdf_data)

    assert result.character_count == 0
    assert result.word_count == 0
    assert result.has_text is False