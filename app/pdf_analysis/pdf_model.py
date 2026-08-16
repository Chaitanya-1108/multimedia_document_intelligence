from dataclasses import dataclass

@dataclass
class PDFData:

    path: str
    page_count: int
    metadata: dict
    text: str
    
@dataclass
class PDFAnalysis:

    page_count: int
    text: str
    character_count: int
    word_count: int
    has_text: bool