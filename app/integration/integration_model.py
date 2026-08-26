from dataclasses import dataclass, field

from app.url_extraction.url_model import URLData


@dataclass
class ExtractionResult:
    """Structured result produced by the extraction integration layer."""

    normalized_text: str
    urls: list[URLData] = field(default_factory=list)