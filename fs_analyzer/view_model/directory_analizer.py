from fs_analyzer.view_model.directory_observer import DirectoryObserver
from fs_analyzer.model.file_categorization_strategy import FileCategorizationStrategy
from fs_analyzer.model.file_listing_generators import *


class DirectoryAnalizer():
    """Represents the high-level features of the fs_analyzer app, namely:
        - File Type Categorization: Classify files into categories (e.g., text, image, 
            executable, etc.) based on their extensions or file signatures.
        - Size Analysis: Calculate the total size for each file type category.
        - File Permissions Report: Generate a report of files with unusual permission 
            settings (e.g., world-writable files).
        - Large Files Identification: Identify and list files above a certain size threshold.
        
        It is modeled as an observable (through the "Observer" design pattern) to
        be compatible with many observers.

        Note that:
            - Symbolic links are ignored.
            - Directories names and sizes are not reported (only those of files).
            - For files at the same depth level of the tree, no assumptions are made 
                regarding the order by which observer method are called.
            - Exceptions during walk are handled through observer methods.
    """
    
    def __init__(self,
                 directory_path:str,
                 file_categorization_strategy: FileCategorizationStrategy, 
                 permission_reporting_strategy: FilePermissionsReportingStrategy,
                 observer: DirectoryObserver) -> None:
        """Configures the analyzer.

        Args:
            directory_path (str): the path where the directory root of the tree to be analyzed
                resides.
            file_categorization_strategy (FileCategorizationStrategy): the strategy by
            which to classify files. 
            permission_reporting_strategy (FilePermissionsReportingStrategy): the strategy by
            which to identify unusual permissions. 
            observer (DirectoryObserver): the observer to be notified of the file analysis
                events during traversal.
        """
        self._directory_path = directory_path
        self._file_categorization_strategy = file_categorization_strategy
        self._permission_reporting_strategy = permission_reporting_strategy
        self._observer = observer
        if not os.path.isdir(self._directory_path):
            self._observer.on_invalid_input()


    
    def categorize_files(self)->None:
        """Walks the directory tree classifying files.
        """
        for (filepath, category) in yield_file_categories(directory_path=self._directory_path, 
                                                          file_categorization_strategy = self._file_categorization_strategy,
                                                          on_error=self._walk_error_handler):
           self._observer.on_new_categorized_file(filepath, category)

    
    def analize_category_sizes(self)->None:
        """"Walks the directory tree reporting files categories' sizes.
        """
        for (category, size) in yield_categories_sizes(directory_path = self._directory_path, 
                                                       file_categorization_strategy = self._file_categorization_strategy,
                                                       on_error=self._walk_error_handler):
            self._observer.on_new_file_category_size(category, size)

    def report_permissions(self)->None:
        """"Walks the directory tree by reporting files with unusual permissions settings.
        """
        for (filepath, permissions) in yield_unusual_permissions(directory_path=self._directory_path,
                                                                 permission_reporting_strategy = self._permission_reporting_strategy,
                                                                 on_error=self._walk_error_handler):
            self._observer.on_new_file_with_unusual_permission(filepath, permissions)


    def identify_large_files(self,file_size_in_bytes:int)->None:
        """Walks the directory tree by identifying files with size greater than the provided
        threshold.
        Args:
            file_size_in_bytes (int): The size threshold in bytes. Files with sizes greater
            than this threshold will be included in the results.
        """
        if file_size_in_bytes < 0:
            self._observer.on_invalid_input()
        else:
            for (filepath, size) in yield_files_larger_than(directory_path=self._directory_path, 
                                                            threshold_in_bytes=file_size_in_bytes, 
                                                            on_error=self._walk_error_handler):
                self._observer.on_new_large_file(filepath, size)

    def _walk_error_handler(self, exception_instance):
        match exception_instance:
            case FileNotFoundError():
                self._observer.on_file_not_found()
            case PermissionError(): 
                self._observer.on_permission_error() 
            case Exception():
                self._observer.on_unknown_error()