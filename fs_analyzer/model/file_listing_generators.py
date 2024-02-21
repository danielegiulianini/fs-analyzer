from typing import Generator, Set
import os

from fs_analyzer.model.file_categorization_strategy import *
from fs_analyzer.model.file_permission_reporting_strategy import *
from fs_analyzer.model.file_category import FileCategory
from fs_analyzer.model.file_permissions import FilePermission


def yield_files_sizes(directory_path: str, on_error = None)->Generator[tuple[str, str],None, None]:    
    for root, _, filenames in os.walk(directory_path, 
                                      onerror=on_error):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            filesize = os.stat(filepath).st_size
            yield (filepath, filesize)


def yield_file_categories(directory_path: str, 
                          file_categorization_strategy: FileCategorizationStrategy, 
                          on_error = None)->Generator[tuple[str, FileCategory],None, None]:    
    for root, _, filenames in os.walk(directory_path, onerror=on_error):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            filecategory = file_categorization_strategy.categorize_file(filepath)
            yield (filepath, filecategory)
 
def yield_files_larger_than(directory_path: str, threshold_in_bytes: int, on_error = None)->Generator[tuple[str, int], None, None]:    
    for (filename, filesize_in_bytes) in yield_files_sizes(directory_path, on_error=on_error):
        if filesize_in_bytes > threshold_in_bytes:
            yield (filename, filesize_in_bytes)
            
def yield_unusual_permissions(directory_path:str, 
                              permission_reporting_strategy: FilePermissionsReportingStrategy = LooserPermissionsReporting(), 
                              on_error = None)->Generator[tuple[str, Set[FilePermission]], None, None]:
    for root, _, filenames in os.walk(directory_path, onerror=on_error):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            stat = os.stat(filepath)
            yield (filepath, permission_reporting_strategy.report_unusual_permissions(stat))
        
# categorizzazione on-line (cos' non sono costretto ad avere una struttura dati gigantesca di tutti i file in memoria)
def yield_categories_sizes(directory_path:str,  file_categorization_strategy: FileCategorizationStrategy = FileCategorizerByExtension(), on_error = None)->Generator[tuple[FileCategory, int], None, None]:
    sizes_by_categories = {}
    for root, _, filenames in os.walk(directory_path, onerror=on_error):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            filesize = os.stat(filepath).st_size
            filecategory =  file_categorization_strategy.categorize_file(filepath)
            if filecategory in sizes_by_categories:
                sizes_by_categories[filecategory]+=filesize
            else:
                sizes_by_categories[filecategory]=filesize
    return  ((category, sizes) for category, sizes in sizes_by_categories.items()) #(catefoty_sizes for catefoty_sizes in sizes_by_categories)  #if want to return as generator (if categories are too many?): (catefoty_sizes for catefoty_sizes in sizes_by_categories)