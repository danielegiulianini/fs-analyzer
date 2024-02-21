from fs_analyzer.view_model.directory_observer import DirectoryObserver
from fs_analyzer.model.file_categorization_strategy import FileCategorizationStrategy

from fs_analyzer.model.file_listing_generators import *


class DirectoryAnalizer():
    
    def __init__(self,
                 directory_path:str,
                 file_categorization_strategy: FileCategorizationStrategy, 
                 permission_reporting_strategy: FilePermissionsReportingStrategy,
                 observer: DirectoryObserver) -> None:
        self._directory_path = directory_path
        self._file_categorization_strategy = file_categorization_strategy
        self._permission_reporting_strategy = permission_reporting_strategy
        self._observer = observer

        
    #1
    def categorize_files(self)->None:
        for (filepath, category) in yield_file_categories(directory_path=self._directory_path, 
                                                          file_categorization_strategy = self._file_categorization_strategy,
                                                          on_error=self._walk_error_handler):
           self._observer.on_new_categorized_file(filepath, category)

    #2
    def analize_category_sizes(self)->None:
        for (category, size) in yield_categories_sizes(directory_path = self._directory_path, 
                                                       file_categorization_strategy = self._file_categorization_strategy,
                                                       on_error=self._walk_error_handler):
            self._observer.on_new_file_category_size(category, size)

    #3
    def report_permissions(self)->None:
        for (filepath, permissions) in yield_unusual_permissions(directory_path=self._directory_path,
                                                                 permission_reporting_strategy = self._permission_reporting_strategy,
                                                                 on_error=self._walk_error_handler):
            self._observer.on_new_file_with_unusual_permission(filepath, permissions)

    #4
    def identify_large_files(self,file_size_in_bytes:int)->None:
        if file_size_in_bytes < 0:
            self._observer.on_invalid_input("size must be >0")
        else:
            for (filepath, size) in yield_files_larger_than(directory_path=self._directory_path, 
                                                            threshold_in_bytes=file_size_in_bytes, 
                                                            on_error=self._walk_error_handler):
                self._observer.on_new_large_file(filepath, size)


    #un decorator check che controlla la cartella se:
    # 1. esiste
    # 2. hai i permessi su di essa
    # e lo dice alla view? (mi tocca aggiungere dipendenza ad os)...

    #or as a method (need a parameter then to generators methods) (if use a library for file signature must check what exceptions can cause)
    def _walk_error_handler(self, exception_instance):
        match exception_instance:
            case FileNotFoundError():
                self._observer.on_file_not_found()
            case PermissionError(): 
                self._observer.on_permission_error() 
            case Exception():
                self._observer.on_unknown_error()
                
