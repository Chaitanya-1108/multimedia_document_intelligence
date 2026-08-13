from pathlib import Path

from app.input.input_processor import process_input


file_path = Path("samples/unsupported.txt")

input_file, error = process_input(file_path)

print("Input File:", input_file)
print("Error:", error)