from dataclasses import dataclass

@dataclass
class ImageData:
    path: str
    format: str
    width: int
    height: int
    channels: int