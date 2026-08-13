from pathlib import Path

from app.input.file_validator import validate_file


file_path = Path("samples/empty_test.pdf")

is_valid, error = validate_file(file_path)

print("Valid:", is_valid)
print("Error:", error)