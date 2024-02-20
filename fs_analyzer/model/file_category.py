from dataclasses import dataclass

@dataclass(frozen=True)
class FileCategory:
    name: str

UNKNOWN_FILE_CATEGORY = FileCategory("unknown")
