from dataclasses import dataclass, field


@dataclass
class DocumentPage:
    page_number: int
    text: str
    elements: list[dict] = field(default_factory=list)


@dataclass
class Document:
    source: str
    document_type: str
    page_count: int
    pages: list[DocumentPage] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
@dataclass
class DocumentAnalysis:
    page_count: int
    text: str
    character_count: int
    word_count: int
    has_text: bool
    empty_page_count: int
    average_words_per_page: float