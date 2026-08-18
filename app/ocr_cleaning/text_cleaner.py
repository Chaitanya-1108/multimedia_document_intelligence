import re
import unicodedata


def _normalize_unicode(text: str) -> str:
    """
    Normalize Unicode characters to NFC representation.
    """
    return unicodedata.normalize("NFC", text)


def _remove_control_characters(text: str) -> str:
    """
    Remove non-printable control characters while preserving
    whitespace characters that are handled by later normalization.
    """
    cleaned_characters = []

    for character in text:
        if character in ("\t", "\r", "\n"):
            cleaned_characters.append(character)
            continue

        category = unicodedata.category(character)

        if category.startswith("C"):
            continue

        cleaned_characters.append(character)

    return "".join(cleaned_characters)


def clean_text(text: str) -> str:
    """
    Normalize OCR text while preserving meaningful document structure
    and security-relevant characters.

    Args:
        text: Raw OCR text.

    Returns:
        Cleaned and normalized text.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Normalize Unicode representation.
    text = _normalize_unicode(text)

    # Remove non-printable control characters.
    text = _remove_control_characters(text)

    # Normalize all line endings to '\n'.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Normalize tabs and other horizontal whitespace to a single space.
    text = re.sub(r"[^\S\n]+", " ", text)

    # Remove unnecessary spaces at the beginning/end of each line.
    text = "\n".join(line.strip() for line in text.split("\n"))

    # Remove excessive blank lines while preserving a single line break.
    text = re.sub(r"\n{2,}", "\n", text)

    # Remove leading/trailing whitespace from the complete text.
    return text.strip()