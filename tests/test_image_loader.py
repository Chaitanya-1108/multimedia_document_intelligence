from pathlib import Path

from app.image.image_loader import load_image


image_path = Path("tests/image_tests/corrupt.png")

success, result = load_image(image_path)

print("Success:", success)
print("Result:", result)