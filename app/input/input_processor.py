from pathlib import Path

from app.input.file_detector import detect_file_type
from app.input.file_validator import validate_file
from app.input.input_model import InputFile


def process_input(file_path: Path) -> tuple[InputFile | None, str | None]:
    is_valid, error = validate_file(file_path)

    if not is_valid:
        return None, error

    source_type = detect_file_type(file_path)

    if source_type == "unknown":
        return None, "UNSUPPORTED_FILE_TYPE"

    input_file = InputFile(
        filename=file_path.name,
        path=file_path,
        extension=file_path.suffix.lower(),
        source_type=source_type
    )

    return input_file, None