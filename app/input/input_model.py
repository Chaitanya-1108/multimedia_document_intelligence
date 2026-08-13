from dataclasses import dataclass
from pathlib import Path


@dataclass
class InputFile:
    filename: str
    path: Path
    extension: str
    source_type: str