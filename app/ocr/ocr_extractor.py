from app.ocr.ocr_engine import run_ocr_data
from app.ocr.ocr_model import OCRResult


def extract_text(processed_image, language="eng"):
    """
    Extract text and confidence information from a processed image.

    Args:
        processed_image: OpenCV image prepared for OCR.
        language: Tesseract language code.

    Returns:
        OCRResult containing extracted text and confidence.
    """

    try:
        data = run_ocr_data(
            processed_image,
            language=language
        )

        if not isinstance(data, dict):
            return OCRResult(
                text="",
                confidence=0.0,
                language=language,
                error="OCR_INVALID_DATA"
            )

        if "text" not in data or "conf" not in data:
            return OCRResult(
                text="",
                confidence=0.0,
                language=language,
                error="OCR_INVALID_DATA"
            )

        text_parts = []
        confidence_values = []

        for text, confidence in zip(
            data["text"],
            data["conf"]
        ):
            text = text.strip()

            if not text:
                continue

            text_parts.append(text)

            try:
                confidence = float(confidence)

                if confidence >= 0:
                    confidence_values.append(confidence)

            except (ValueError, TypeError):
                continue

        extracted_text = " ".join(text_parts)

        if confidence_values:
            average_confidence = (
                sum(confidence_values)
                / len(confidence_values)
            )
        else:
            average_confidence = 0.0

        return OCRResult(
            text=extracted_text,
            confidence=round(average_confidence, 2),
            language=language,
            error=None
        )

    except RuntimeError as error:
        return OCRResult(
            text="",
            confidence=0.0,
            language=language,
            error=str(error)
        )