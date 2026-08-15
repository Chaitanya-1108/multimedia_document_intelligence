from pathlib import Path

import cv2

from app.image.image_loader import load_image
from app.image.image_preprocessor import preprocess_image


image_path = Path("tests/image_tests/sample.png")

success, image_data = load_image(image_path)

if not success:
    print("Image loading failed:", image_data)
else:
    image = cv2.imread(str(image_path))

    print("Original shape:", image.shape)

    # General preprocessing
    general_image = preprocess_image(
        image,
        mode="general"
    )

    print("General processed shape:", general_image.shape)
    print("General channels:", len(general_image.shape))

    # OCR preprocessing
    ocr_image = preprocess_image(
        image,
        mode="ocr"
    )

    print("OCR processed shape:", ocr_image.shape)
    print("OCR channels:", len(ocr_image.shape))

    # QR preprocessing
    qr_image = preprocess_image(
        image,
        mode="qr"
    )

    print("QR processed shape:", qr_image.shape)
    print("QR channels:", len(qr_image.shape))

    # Verify grayscale output
    assert len(general_image.shape) == 2
    assert len(ocr_image.shape) == 2
    assert len(qr_image.shape) == 2

    # Verify that the original image was not modified
    assert len(image.shape) == 3
    assert image.shape == (907, 1898, 3)

    # Save processed images
    cv2.imwrite(
        "tests/image_tests/processed_general.png",
        general_image
    )

    cv2.imwrite(
        "tests/image_tests/processed_ocr.png",
        ocr_image
    )

    cv2.imwrite(
        "tests/image_tests/processed_qr.png",
        qr_image
    )

    print("All preprocessing tests passed successfully.")