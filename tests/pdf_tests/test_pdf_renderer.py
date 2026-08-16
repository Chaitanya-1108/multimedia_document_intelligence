from pathlib import Path

import fitz
import numpy as np

from app.pdf_analysis.pdf_renderer import render_pdf_page


def create_test_pdf(path: Path) -> None:
    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text(
        (72, 72),
        "First PDF Page"
    )

    page2 = document.new_page()
    page2.insert_text(
        (72, 72),
        "Second PDF Page"
    )

    document.save(str(path))
    document.close()


def test_render_first_page(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    success, result = render_pdf_page(pdf_path)

    assert success is True
    assert isinstance(result, np.ndarray)
    assert result.ndim == 3
    assert result.shape[0] > 0
    assert result.shape[1] > 0


def test_render_second_page(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    success, result = render_pdf_page(
        pdf_path,
        page_number=1
    )

    assert success is True
    assert isinstance(result, np.ndarray)
    assert result.ndim == 3


def test_invalid_page_number(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    success, result = render_pdf_page(
        pdf_path,
        page_number=2
    )

    assert success is False
    assert result == "INVALID_PAGE_NUMBER"


def test_negative_page_number(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    success, result = render_pdf_page(
        pdf_path,
        page_number=-1
    )

    assert success is False
    assert result == "INVALID_PAGE_NUMBER"


def test_pdf_file_not_found(tmp_path):
    pdf_path = tmp_path / "missing.pdf"

    success, result = render_pdf_page(pdf_path)

    assert success is False
    assert result == "FILE_NOT_FOUND"


def test_pdf_empty_file(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    pdf_path.touch()

    success, result = render_pdf_page(pdf_path)

    assert success is False
    assert result == "EMPTY_FILE"


def test_invalid_pdf(tmp_path):
    pdf_path = tmp_path / "invalid.pdf"

    pdf_path.write_text(
        "This is not a valid PDF."
    )

    success, result = render_pdf_page(pdf_path)

    assert success is False
    assert result == "PDF_RENDER_ERROR"