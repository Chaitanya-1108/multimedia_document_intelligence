from app.document.document_analyzer import analyze_document
from app.document.document_model import (
    Document,
    DocumentAnalysis,
    DocumentPage,
)


def test_analyze_document_with_text():
    document = Document(
        source="sample.pdf",
        document_type="pdf",
        page_count=2,
        pages=[
            DocumentPage(
                page_number=1,
                text="Hello world",
            ),
            DocumentPage(
                page_number=2,
                text="Document intelligence",
            ),
        ],
    )

    analysis = analyze_document(document)

    assert isinstance(analysis, DocumentAnalysis)

    assert analysis.page_count == 2
    assert analysis.text == "Hello world\nDocument intelligence"
    assert analysis.character_count == len(
        "Hello world\nDocument intelligence"
    )
    assert analysis.word_count == 4
    assert analysis.has_text is True
    assert analysis.empty_page_count == 0
    assert analysis.average_words_per_page == 2.0


def test_analyze_document_with_empty_page():
    document = Document(
        source="sample.pdf",
        document_type="pdf",
        page_count=3,
        pages=[
            DocumentPage(
                page_number=1,
                text="Hello world",
            ),
            DocumentPage(
                page_number=2,
                text="",
            ),
            DocumentPage(
                page_number=3,
                text="Document",
            ),
        ],
    )

    analysis = analyze_document(document)

    assert analysis.page_count == 3
    assert analysis.word_count == 3
    assert analysis.has_text is True
    assert analysis.empty_page_count == 1
    assert analysis.average_words_per_page == 1.0


def test_analyze_empty_document():
    document = Document(
        source="empty.pdf",
        document_type="pdf",
        page_count=0,
        pages=[],
    )

    analysis = analyze_document(document)

    assert isinstance(analysis, DocumentAnalysis)

    assert analysis.page_count == 0
    assert analysis.text == ""
    assert analysis.character_count == 0
    assert analysis.word_count == 0
    assert analysis.has_text is False
    assert analysis.empty_page_count == 0
    assert analysis.average_words_per_page == 0.0


def test_analyze_document_with_whitespace_only_page():
    document = Document(
        source="whitespace.pdf",
        document_type="pdf",
        page_count=1,
        pages=[
            DocumentPage(
                page_number=1,
                text="   \n   ",
            ),
        ],
    )

    analysis = analyze_document(document)

    assert analysis.text == "   \n   "
    assert analysis.character_count == 0
    assert analysis.word_count == 0
    assert analysis.has_text is False
    assert analysis.empty_page_count == 1
    assert analysis.average_words_per_page == 0.0