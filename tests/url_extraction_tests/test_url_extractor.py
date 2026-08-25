from app.url_extraction.url_extractor import extract_urls


def test_extracts_https_url():
    text = "Visit https://example.com/login"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com/login"
    assert results[0].domain == "example.com"


def test_extracts_http_url():
    text = "Visit http://example.com"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "http://example.com"
    assert results[0].domain == "example.com"


def test_extracts_multiple_urls():
    text = "Visit https://example.com and http://test.com"

    results = extract_urls(text)

    assert len(results) == 2
    assert results[0].url == "https://example.com"
    assert results[1].url == "http://test.com"


def test_returns_empty_list_when_no_url_exists():
    text = "This text contains no URLs."

    results = extract_urls(text)

    assert results == []


def test_extracts_url_with_path_query_and_fragment():
    text = "https://example.com/login?user=test&id=42#section"

    results = extract_urls(text)

    assert len(results) == 1
    assert (
        results[0].url
        == "https://example.com/login?user=test&id=42#section"
    )
    assert results[0].domain == "example.com"


def test_records_source_positions():
    text = "Visit https://example.com today."

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].start == 6
    assert results[0].end == 25
    
def test_removes_trailing_period():
    text = "Visit https://example.com."

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_removes_trailing_comma():
    text = "Visit https://example.com, then continue."

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_removes_trailing_exclamation_mark():
    text = "Visit https://example.com!"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_removes_trailing_semicolon():
    text = "Visit https://example.com;"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_preserves_query_and_fragment_punctuation():
    text = "https://example.com/path?x=1&y=2#section"

    results = extract_urls(text)

    assert len(results) == 1
    assert (
        results[0].url
        == "https://example.com/path?x=1&y=2#section"
    )


def test_updates_end_position_after_boundary_cleanup():
    text = "Visit https://example.com."

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].start == 6
    assert results[0].end == 25
    
def test_extracts_bare_domain():
    text = "Visit example.com"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "example.com"
    assert results[0].domain == "example.com"


def test_extracts_www_domain():
    text = "Visit www.example.com"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "www.example.com"
    assert results[0].domain == "www.example.com"


def test_does_not_duplicate_domain_inside_https_url():
    text = "Visit https://example.com"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_extracts_multiple_domain_forms():
    text = "Visit example.com and www.test.org"

    results = extract_urls(text)

    assert len(results) == 2
    assert results[0].url == "example.com"
    assert results[1].url == "www.test.org"


def test_does_not_extract_email_domain_as_url():
    text = "Contact user@example.com"

    results = extract_urls(text)

    assert results == []


def test_does_not_extract_simple_decimal_number_as_domain():
    text = "The version is 1.2.3"

    results = extract_urls(text)

    assert results == []
    
def test_removes_exact_duplicate_urls():
    text = (
        "Visit https://example.com "
        "and then visit https://example.com again."
    )

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "https://example.com"


def test_preserves_first_occurrence_of_duplicate_url():
    text = (
        "First https://example.com "
        "then https://example.com"
    )

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].start == 6


def test_keeps_different_urls_with_same_domain():
    text = (
        "Visit https://example.com "
        "and https://example.com/login"
    )

    results = extract_urls(text)

    assert len(results) == 2
    assert results[0].url == "https://example.com"
    assert results[1].url == "https://example.com/login"


def test_deduplicates_bare_domains():
    text = "Visit example.com and later example.com."

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].url == "example.com"


def test_deduplication_preserves_source_order():
    text = (
        "https://first.com "
        "https://second.com "
        "https://first.com"
    )

    results = extract_urls(text)

    assert len(results) == 2
    assert results[0].url == "https://first.com"
    assert results[1].url == "https://second.com"
    
def test_records_correct_positions_for_bare_domain():
    text = "Visit example.com today."

    results = extract_urls(text)

    assert len(results) == 1

    result = results[0]

    assert result.url == "example.com"
    assert text[result.start:result.end] == "example.com"


def test_records_correct_positions_for_www_domain():
    text = "Visit www.example.com today."

    results = extract_urls(text)

    assert len(results) == 1

    result = results[0]

    assert result.url == "www.example.com"
    assert text[result.start:result.end] == "www.example.com"


def test_records_correct_positions_after_trailing_punctuation():
    text = "Visit https://example.com, today."

    results = extract_urls(text)

    assert len(results) == 1

    result = results[0]

    assert result.url == "https://example.com"
    assert text[result.start:result.end] == "https://example.com"


def test_records_positions_for_multiple_urls():
    text = "A https://first.com B example.org C http://third.net"

    results = extract_urls(text)

    assert len(results) == 3

    assert text[results[0].start:results[0].end] == "https://first.com"
    assert text[results[1].start:results[1].end] == "example.org"
    assert text[results[2].start:results[2].end] == "http://third.net"


def test_positions_remain_correct_after_duplicate_removal():
    text = (
        "First https://example.com "
        "then https://other.com "
        "then https://example.com"
    )

    results = extract_urls(text)

    assert len(results) == 2

    assert results[0].url == "https://example.com"
    assert results[1].url == "https://other.com"

    assert text[results[0].start:results[0].end] == "https://example.com"
    assert text[results[1].start:results[1].end] == "https://other.com"
    
def test_empty_string_returns_empty_list():
    assert extract_urls("") == []


def test_whitespace_only_text_returns_empty_list():
    assert extract_urls("   \n\t  ") == []


def test_extracted_url_position_matches_source_text():
    text = "Security link: https://example.com/login"

    results = extract_urls(text)

    assert len(results) == 1

    result = results[0]

    assert text[result.start:result.end] == result.url


def test_domain_is_extracted_without_path():
    text = "Visit https://example.com/login"

    results = extract_urls(text)

    assert len(results) == 1
    assert results[0].domain == "example.com"


def test_mixed_url_types_are_returned_in_source_order():
    text = (
        "example.com "
        "https://secure.example.org/login "
        "www.test.net"
    )

    results = extract_urls(text)

    assert len(results) == 3

    assert results[0].url == "example.com"
    assert results[1].url == "https://secure.example.org/login"
    assert results[2].url == "www.test.net"


def test_no_url_text_does_not_raise_error():
    text = "This is ordinary OCR text without a web address."

    results = extract_urls(text)

    assert results == []