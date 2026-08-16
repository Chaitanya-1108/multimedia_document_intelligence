from pathlib import Path

import fitz

from app.pdf_analysis.pdf_reader import read_pdf


def create_test_pdf(path: Path) -> None:
    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Digital Safety Intelligence Platform"
    )

    document.set_metadata({
        "title": "Test PDF",
        "author": "Multimedia Intelligence"
    })

    document.save(str(path))
    document.close()


def test_read_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    success, result = read_pdf(pdf_path)

    assert success is True
    assert result.path == str(pdf_path)
    assert result.page_count == 1
    assert "Digital Safety Intelligence Platform" in result.text


def test_pdf_metadata(tmp_path):
    pdf_path = tmp_path / "metadata.pdf"

    create_test_pdf(pdf_path)

    success, result = read_pdf(pdf_path)

    assert success is True
    assert result.metadata["title"] == "Test PDF"
    assert result.metadata["author"] == "Multimedia Intelligence"


def test_pdf_file_not_found(tmp_path):
    pdf_path = tmp_path / "missing.pdf"

    success, result = read_pdf(pdf_path)

    assert success is False
    assert result == "FILE_NOT_FOUND"


def test_pdf_empty_file(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    pdf_path.touch()

    success, result = read_pdf(pdf_path)

    assert success is False
    assert result == "EMPTY_FILE"


def test_invalid_pdf(tmp_path):
    pdf_path = tmp_path / "invalid.pdf"

    pdf_path.write_text(
        "This is not a valid PDF file."
    )

    success, result = read_pdf(pdf_path)

    assert success is False
    assert result == "INVALID_PDF"