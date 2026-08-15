from pathlib import Path

import cv2

from app.image.image_loader import load_image
from app.image.image_preprocessor import preprocess_image


TEST_DIR = Path("tests/image_tests")

VALID_IMAGE = TEST_DIR / "sample.png"
EMPTY_FILE = TEST_DIR / "empty.png"
INVALID_IMAGE = TEST_DIR / "corrupt.png"
MISSING_IMAGE = TEST_DIR / "missing.png"


def test_missing_image():
    success, result = load_image(MISSING_IMAGE)

    assert success is False
    assert result == "FILE_NOT_FOUND"

    print("1. Missing image test: PASSED")


def test_empty_image():
    success, result = load_image(EMPTY_FILE)

    assert success is False
    assert result == "EMPTY_FILE"

    print("2. Empty image test: PASSED")


def test_invalid_image():
    success, result = load_image(INVALID_IMAGE)

    assert success is False
    assert result == "INVALID_IMAGE"

    print("3. Invalid image test: PASSED")


def test_valid_image():
    success, result = load_image(VALID_IMAGE)

    assert success is True

    print("4. Valid image test: PASSED")
    print(f"   ImageData: {result}")


def test_general_preprocessing():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    processed_image = preprocess_image(
        image,
        mode="general"
    )

    assert len(processed_image.shape) == 2

    print("5. General preprocessing test: PASSED")


def test_ocr_preprocessing():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    processed_image = preprocess_image(
        image,
        mode="ocr"
    )

    assert len(processed_image.shape) == 2

    print("6. OCR preprocessing test: PASSED")


def test_qr_preprocessing():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    processed_image = preprocess_image(
        image,
        mode="qr"
    )

    assert len(processed_image.shape) == 2

    print("7. QR preprocessing test: PASSED")


def test_original_image_unchanged():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    original_shape = image.shape
    original_copy = image.copy()

    preprocess_image(
        image,
        mode="ocr"
    )

    assert image.shape == original_shape
    assert (image == original_copy).all()

    print("8. Original image immutability test: PASSED")


def test_small_image_resize():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    small_image = cv2.resize(
        image,
        (800, 600)
    )

    processed_image = preprocess_image(
        small_image,
        mode="general"
    )

    assert processed_image.shape[1] >= 1200

    print("9. Small-image resize test: PASSED")


def test_unsupported_mode():
    image = cv2.imread(str(VALID_IMAGE))

    assert image is not None

    try:
        preprocess_image(
            image,
            mode="unsupported"
        )

        assert False

    except ValueError as error:
        assert "Unsupported preprocessing mode" in str(error)

    print("10. Unsupported preprocessing mode test: PASSED")


def main():
    print("=" * 60)
    print("DAY 3 — IMAGE LAYER TESTS")
    print("=" * 60)

    test_missing_image()
    test_empty_image()
    test_invalid_image()
    test_valid_image()
    test_general_preprocessing()
    test_ocr_preprocessing()
    test_qr_preprocessing()
    test_original_image_unchanged()
    test_small_image_resize()
    test_unsupported_mode()

    print("=" * 60)
    print("ALL DAY 3 IMAGE LAYER TESTS PASSED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()