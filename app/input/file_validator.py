from pathlib import Path


def validate_file(file_path: Path) -> tuple[bool, str | None]:
    if not file_path.exists():
        return False, "FILE_NOT_FOUND"

    if not file_path.is_file():
        return False, "INVALID_FILE"

    if file_path.stat().st_size == 0:
        return False, "EMPTY_FILE"

    return True, None