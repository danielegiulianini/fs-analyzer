from abc import ABC, abstractmethod
import filetype

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
        if (guessedMime := filetype.guess(filepath).mime) is not None:
            category = guessedMime
        return category

class FileCategorizerByExtension(FileCategorizationStrategy):
   pass