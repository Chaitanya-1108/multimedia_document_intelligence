from pathlib import Path

import cv2

from app.image.image_preprocessor import preprocess_image
from app.ocr.ocr_extractor import extract_text
from app.ocr.ocr_model import OCRResult


def test_image_preprocessing_to_ocr():
    image_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "test_ocr.png"
    )

    assert image_path.exists()

    image = cv2.imread(str(image_path))

    assert image is not None

    processed_image = preprocess_image(
        image,
        mode="ocr"
    )

    assert processed_image is not None
    assert processed_image.size > 0

    result = extract_text(processed_image)

    assert isinstance(result, OCRResult)

    assert isinstance(result.text, str)
    assert len(result.text) > 0

    assert isinstance(result.confidence, float)
    assert result.confidence >= 0

    assert result.language == "eng"
    assert result.error is None