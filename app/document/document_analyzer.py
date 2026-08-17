from app.document.document_model import Document, DocumentAnalysis


def analyze_document(document: Document) -> DocumentAnalysis:
    page_texts = [
        page.text
        for page in document.pages
        if page.text
    ]

    text = "\n".join(page_texts)

    stripped_text = text.strip()

    character_count = len(stripped_text)

    word_count = len(stripped_text.split()) if stripped_text else 0

    has_text = bool(stripped_text)

    empty_page_count = sum(
        1
        for page in document.pages
        if not page.text.strip()
    )

    if document.page_count > 0:
        average_words_per_page = (
            word_count / document.page_count
        )
    else:
        average_words_per_page = 0.0

    return DocumentAnalysis(
        page_count=document.page_count,
        text=text,
        character_count=character_count,
        word_count=word_count,
        has_text=has_text,
        empty_page_count=empty_page_count,
        average_words_per_page=round(
            average_words_per_page,
            2
        ),
    )