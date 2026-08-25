import re
from urllib.parse import urlparse

from app.url_extraction.url_model import URLData


_URL_PATTERN = re.compile(
    r"https?://[^\s]+",
    re.IGNORECASE,
)

_DOMAIN_PATTERN = re.compile(
    r"(?<![@\w.-])"
    r"(?:www\.)?"
    r"(?:[a-zA-Z0-9-]+\.)+"
    r"[a-zA-Z]{2,}"
    r"(?![\w.-])",
    re.IGNORECASE,
)

_TRAILING_BOUNDARY_PUNCTUATION = ".,!?;:"


def _clean_url_boundary(url: str) -> str:
    """Remove punctuation that clearly terminates a URL in surrounding text."""

    while url and url[-1] in _TRAILING_BOUNDARY_PUNCTUATION:
        url = url[:-1]

    return url


def _extract_explicit_urls(text: str) -> list[URLData]:
    """Extract HTTP and HTTPS URLs from text."""

    results: list[URLData] = []

    for match in _URL_PATTERN.finditer(text):
        raw_url = match.group(0)
        url = _clean_url_boundary(raw_url)

        if not url:
            continue

        parsed = urlparse(url)
        domain = parsed.hostname

        if not domain:
            continue

        start = match.start()
        end = start + len(url)

        results.append(
            URLData(
                url=url,
                domain=domain,
                start=start,
                end=end,
            )
        )

    return results


def _overlaps_existing_range(
    start: int,
    end: int,
    results: list[URLData],
) -> bool:
    """Return whether a candidate range overlaps an existing URL."""

    return any(
        start < result.end and end > result.start
        for result in results
    )


def _extract_bare_domains(
    text: str,
    existing_results: list[URLData],
) -> list[URLData]:
    """Extract bare domains that are not already part of explicit URLs."""

    results: list[URLData] = []

    for match in _DOMAIN_PATTERN.finditer(text):
        start = match.start()
        end = match.end()
        domain = match.group(0)

        if _overlaps_existing_range(start, end, existing_results):
            continue

        results.append(
            URLData(
                url=domain,
                domain=domain,
                start=start,
                end=end,
            )
        )

    return results


def extract_urls(text: str) -> list[URLData]:
    """Extract explicit URLs and bare domains from text."""

    if not text:
        return []

    explicit_results = _extract_explicit_urls(text)

    bare_domain_results = _extract_bare_domains(
        text,
        explicit_results,
    )

    results = sorted(
    explicit_results + bare_domain_results,
    key=lambda result: result.start,
    )

    return _deduplicate_urls(results)
    
def _deduplicate_urls(results: list[URLData]) -> list[URLData]:
    """Remove exact duplicate URLs while preserving first-seen order."""

    seen: set[str] = set()
    unique_results: list[URLData] = []

    for result in results:
        if result.url in seen:
            continue

        seen.add(result.url)
        unique_results.append(result)

    return unique_results