from abc import ABC, abstractmethod
import filetype
import mimetypes

from fs_analyzer.model.file_category import UNKNOWN_FILE_CATEGORY, FileCategory


class FileCategorizationStrategy(ABC):
    """An abstract class representing a strategy for classifying files modeled
    through the behavioural "Strategy" OO pattern.
    It isolates the file classification logic so allowing to reuse it in different scenarios
    and make its implementations interchangeable without affecting the context using them, as well
    as to make the current context compatible with future implementations.
    """
    
    
    @abstractmethod
    def categorize_file(file_path: str) -> FileCategory:
        """Classifies the file pointed by the provided path.

        Args:
            file_path (str): the path of the file to be classified.

        Returns:
            FileCategory: the category of the file.
        """
        pass


class FileCategorizerBySignature(FileCategorizationStrategy):
    """A concrete implementation of FileCategorizationStrategy that classifies files by inspecting its 
    file signature rather than its file extension.

    Args:
        FileCategorizationStrategy: the abstract file categorization strategy.
    """
    def categorize_file(self, file_path: str) -> FileCategory:
        category = UNKNOWN_FILE_CATEGORY
        if (guessed_category_info := filetype.guess(file_path)) is not None:
            category = FileCategory((guessed_category_info).mime)
        return category


class FileCategorizerByExtension(FileCategorizationStrategy):
    """A concrete implementation of FileCategorizationStrategy that classifies files by inspecting its 
    file extension rather than its file signature.

    Args:
        FileCategorizationStrategy: the abstract file categorization strategy.
    """
    def __init__(self):
        mimetypes.init()
        
    def categorize_file(self, filepath: str) -> FileCategory:
        category = UNKNOWN_FILE_CATEGORY
        guessed_mime, _ = mimetypes.guess_type(filepath)
        if guessed_mime is not None:
            category = FileCategory(guessed_mime)
        return category
    