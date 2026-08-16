from pathlib import Path

import fitz
import numpy as np

from app.pdf_analysis.pdf_reader import read_pdf
from app.pdf_analysis.pdf_renderer import render_pdf_page
from app.pdf_analysis.pdf_analyzer import analyze_pdf


def create_test_pdf(path: Path) -> None:
    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text(
        (72, 72),
        "Digital Safety Intelligence Platform"
    )

    page2 = document.new_page()
    page2.insert_text(
        (72, 72),
        "Multimedia and Document Intelligence"
    )

    document.set_metadata({
        "title": "Integration Test PDF",
        "author": "Test System"
    })

    document.save(str(path))
    document.close()


def test_pdf_full_pipeline(tmp_path):
    pdf_path = tmp_path / "integration.pdf"

    create_test_pdf(pdf_path)

    # Step 1: Read the PDF
    success, pdf_data = read_pdf(pdf_path)

    assert success is True
    assert pdf_data.page_count == 2
    assert "Digital Safety Intelligence Platform" in pdf_data.text
    assert "Multimedia and Document Intelligence" in pdf_data.text

    # Step 2: Analyze the PDF
    analysis = analyze_pdf(pdf_data)

    assert analysis.page_count == 2
    assert analysis.has_text is True
    assert analysis.character_count > 0
    assert analysis.word_count > 0

    # Step 3: Render the first page
    success, rendered_page = render_pdf_page(
        pdf_path,
        page_number=0
    )

    assert success is True
    assert isinstance(rendered_page, np.ndarray)
    assert rendered_page.ndim == 3
    assert rendered_page.shape[0] > 0
    assert rendered_page.shape[1] > 0