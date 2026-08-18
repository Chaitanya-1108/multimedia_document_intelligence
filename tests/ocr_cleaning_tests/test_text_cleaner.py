import pytest

from app.ocr_cleaning.text_cleaner import clean_text


def test_clean_text_removes_leading_and_trailing_whitespace():
    result = clean_text("   Hello World   ")

    assert result == "Hello World"


def test_clean_text_collapses_repeated_spaces():
    result = clean_text("Hello     World")

    assert result == "Hello World"


def test_clean_text_normalizes_tabs():
    result = clean_text("Hello\t\tWorld")

    assert result == "Hello World"


def test_clean_text_normalizes_line_endings():
    result = clean_text("Hello\r\nWorld\rAgain")

    assert result == "Hello\nWorld\nAgain"


def test_clean_text_preserves_line_boundaries():
    result = clean_text("Name: John\nEmail: john@example.com")

    assert result == "Name: John\nEmail: john@example.com"


def test_clean_text_removes_excessive_blank_lines():
    result = clean_text("Hello\n\n\nWorld")

    assert result == "Hello\nWorld"


def test_clean_text_preserves_urls():
    result = clean_text("Visit   https://example.com/login")

    assert result == "Visit https://example.com/login"


def test_clean_text_preserves_special_characters():
    result = clean_text("Price: $100 | ID: #123 | Email: test@example.com")

    assert result == "Price: $100 | ID: #123 | Email: test@example.com"


def test_clean_text_rejects_non_string_input():
    with pytest.raises(TypeError):
        clean_text(None)
        
def test_clean_text_normalizes_unicode_to_nfc():
    decomposed_text = "Cafe\u0301"

    result = clean_text(decomposed_text)

    assert result == "Café"


def test_clean_text_removes_null_character():
    result = clean_text("Hello\x00World")

    assert result == "HelloWorld"


def test_clean_text_removes_control_characters():
    result = clean_text("Hello\x01World\x02Test")

    assert result == "HelloWorldTest"


def test_clean_text_preserves_newlines():
    result = clean_text("Hello\nWorld")

    assert result == "Hello\nWorld"


def test_clean_text_preserves_unicode_text():
    result = clean_text("नमस्ते 世界")

    assert result == "नमस्ते 世界"


def test_clean_text_preserves_url_punctuation():
    result = clean_text(
        "https://example.com/path?id=123&user=test@example.com"
    )

    assert result == "https://example.com/path?id=123&user=test@example.com"


def test_clean_text_preserves_security_relevant_symbols():
    result = clean_text(
        "https://example.com/login?redirect=https://evil.example"
    )

    assert result == (
        "https://example.com/login?redirect=https://evil.example"
    )
    
def test_clean_text_handles_empty_string():
    result = clean_text("")

    assert result == ""


def test_clean_text_handles_whitespace_only_text():
    result = clean_text("   \n\t   ")

    assert result == ""


def test_clean_text_is_idempotent():
    text = "  Hello   World\n\nVisit https://example.com  "

    first_result = clean_text(text)
    second_result = clean_text(first_result)

    assert second_result == first_result


def test_clean_text_preserves_multiline_document_structure():
    result = clean_text(
        "Name: John Doe\n"
        "Address: Pune\n"
        "Website: https://example.com"
    )

    assert result == (
        "Name: John Doe\n"
        "Address: Pune\n"
        "Website: https://example.com"
    )


def test_clean_text_handles_mixed_whitespace():
    result = clean_text("  Hello\t\tWorld  \r\n  Test   ")

    assert result == "Hello World\nTest"


def test_clean_text_preserves_ip_address_and_port():
    result = clean_text("Server: 192.168.1.10:8080")

    assert result == "Server: 192.168.1.10:8080"


def test_clean_text_preserves_url_query_parameters():
    result = clean_text(
        "https://example.com/login?user=test&id=123&redirect=/home"
    )

    assert result == (
        "https://example.com/login?user=test&id=123&redirect=/home"
    )