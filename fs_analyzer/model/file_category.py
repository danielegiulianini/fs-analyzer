from dataclasses import dataclass


@dataclass(frozen=True)
class FileCategory:
    """ Represents a possible classification of a file, which cannot be edited at runtime.
    
    Args:
            name (str): a human-readable name for the category assigned to the file.

    """
    name: str

    """Represents the category of the files for which it was not possible to identify a category.
    """
UNKNOWN_FILE_CATEGORY = FileCategory("unknown")
