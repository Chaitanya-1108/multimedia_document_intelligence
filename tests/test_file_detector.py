from pathlib import Path

from app.input.file_detector import detect_file_type


test_files = [
    "photo.JPG",
    "photo.JPEG",
    "photo.PNG",
    "photo.WEBP",
    "document.PDF",
]
file_path = Path("malicious.exe")

file_type = detect_file_type(file_path)

print("Detected type:", file_type)

for filename in test_files:
    file_path = Path(filename)

    file_type = detect_file_type(file_path)

    print(f"{filename} -> {file_type}")