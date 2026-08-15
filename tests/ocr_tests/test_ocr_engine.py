from pathlib import Path

import cv2

from app.ocr.ocr_engine import run_ocr, run_ocr_data


def test_run_ocr():
    image_path = Path(__file__).resolve().parent.parent / "assets" / "test_ocr.png"

    image = cv2.imread(str(image_path))

    assert image is not None

    text = run_ocr(image)

    assert isinstance(text, str)
    assert len(text) > 0
    
def test_run_ocr_data():
    image_path = Path(__file__).resolve().parent.parent / "assets" / "test_ocr.png"

    assert image_path.exists()

    image = cv2.imread(str(image_path))

    assert image is not None

    data = run_ocr_data(image)

    assert isinstance(data, dict)

    assert "text" in data
    assert "conf" in data