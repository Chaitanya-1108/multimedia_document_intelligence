from dataclasses import dataclass


@dataclass
class OCRResult:
    text: str
    confidence: float
    language: str
    error: str | None = None