from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PDF_EXTENSIONS = {".pdf"}


def detect_file_type(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension in IMAGE_EXTENSIONS:
        return "image"

    if extension in PDF_EXTENSIONS:
        return "pdf"

    return "unknown"