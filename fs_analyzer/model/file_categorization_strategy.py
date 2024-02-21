from abc import ABC, abstractmethod
import filetype
import mimetypes

from fs_analyzer.model.file_category import UNKNOWN_FILE_CATEGORY, FileCategory

#interface
class FileCategorizationStrategy(ABC):
    @abstractmethod
    def categorize_file(filepath)->FileCategory:
        pass

class FileCategorizerBySignature(FileCategorizationStrategy):
    def categorize_file(self, filepath:str)->FileCategory:
        # if I use library here need to put try (especially if reads from file)!
        category = UNKNOWN_FILE_CATEGORY
        if (guessedType := filetype.guess(filepath)) is not None:
            category = FileCategory(guessedType.mime)
        return category


class FileCategorizerByExtension(FileCategorizationStrategy):
    def __init__(self):
        mimetypes.init()
        
    def categorize_file(self, filepath:str)->FileCategory:
        category = UNKNOWN_FILE_CATEGORY
        guessedMime, _ = mimetypes.guess_type(filepath)
        if guessedMime is not None:
            category = FileCategory(guessedMime)
        return category