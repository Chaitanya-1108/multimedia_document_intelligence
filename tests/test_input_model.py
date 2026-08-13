from pathlib import Path

from app.input.input_model import InputFile


input_file = InputFile(
    filename="sample.pdf",
    path=Path("samples/pdfs/sample.pdf"),
    extension=".pdf",
    source_type="pdf"
)

print(input_file)