from dataclasses import dataclass


@dataclass(frozen=True)
class URLData:
    """Structured representation of an extracted URL."""

    url: str
    domain: str
    start: int
    end: int