from typing import Generator, Set
import os

from fs_analyzer.model.file_categorization_strategy import *
from fs_analyzer.model.file_permission_reporting_strategy import *
from fs_analyzer.model.file_category import FileCategory
from fs_analyzer.model.file_permissions import FilePermission
from fs_analyzer.model.func_utils import call_if_not_none_with_param as call_if_not_none

def yield_files_sizes(directory_path: str, 
                      on_error = None)->Generator[tuple[str, int],None, None]:
    """ Generate the file names and corresponding file sizes contained in the 
    directory tree pointed by the path provided, one by one, by walking the tree
    top-down.
    
    Note that:
    - Symbolic links are ignored.
    - Directories names and sizes are not returned (only those of files).
    - For files at the same depth level of the tree, no assumptions are made 
        regarding the order by which filenames are returned.
    - if no on_error is provided, exceptions during walk are silently ignored.

    Args:
        directory_path (str): the path where the directory root of the tree resides.
        on_error (optional): the handler for any errors happening during the walk.
            Defaults to None.

    Yields:
        Generator[tuple[str, int], None, None]: the generator of (file name, file 
        size) tuples.
    """
    for root, _, filenames in os.walk(directory_path, 
                                      onerror=on_error):
        for file_name in filenames:
            try:
                file_path = os.path.join(root, file_name)
                file_size = os.stat(file_path).st_size
            except OSError as e:
                if on_error is not None:
                    on_error(e)
                continue
            yield (file_path, file_size)


def yield_file_categories(directory_path: str, 
                          file_categorization_strategy: FileCategorizationStrategy = FileCategorizerByExtension, 
                          on_error = None) -> Generator[tuple[str, FileCategory], None, None]:
    """Generate the file names and corresponding file categories contained in the 
    directory tree pointed by the path provided, one by one, by walking the tree
    top-down.
    
    Note that:
    - Symbolic links are ignored.
    - Directories names and sizes are not returned (only those of files).
    - For files at the same depth level of the tree, no assumptions are made 
        regarding the order by which filenames are returned.
    - if no on_error is provided, exceptions during walk are silently ignored.

    Args:
        directory_path (str):  the path where the directory root of the tree resides.
        file_categorization_strategy (FileCategorizationStrategy, optional): the strategy by
            which to classify files. 
            Defaults to FileCategorizerByExtension.
        on_error (_type_, optional): the handler for any errors happening during the walk.
            Defaults to None.

    Yields:
        Generator[tuple[str, FileCategory], None, None]:  the generator of (file_name, 
        file category) tuples.
    """
    for root, _, filenames in os.walk(directory_path, onerror=on_error):
        for file_name in filenames:
            try:
                file_path = os.path.join(root, file_name)
                file_category = file_categorization_strategy.categorize_file(file_path)
            except OSError as e:
                if on_error is not None:
                    on_error(e)
                continue
            yield (file_path, file_category)
 
def yield_files_larger_than(directory_path: str,
                            threshold_in_bytes: int, 
                            on_error = None)->Generator[tuple[str, int], None, None]:
    """Generate the file names and corresponding sizes for the files with a size greater
    than the given threshold in bytes, contained in the directory tree pointed by 
    the provided path. This is done one by one by walking the tree top-down.

    Note that:
    - Symbolic links are ignored.
    - Directories names and sizes are not returned (only those of files).
    - For files at the same depth level of the tree, no assumptions are made 
        regarding the order by which filenames are returned.
    - if no on_error is provided, exceptions during walk are silently ignored.
    
    Args:
        directory_path (str): the path where the directory root of the tree resides.
        threshold_in_bytes (int): The size threshold in bytes. Files with sizes greater
            than this threshold will be included in the results.
        on_error (_type_, optional): the handler for any errors happening during the walk.
            Defaults to None.

    Yields:
        Generator[tuple[str, int], None, None]:  the generator of (file_name, 
        file size) tuples.
    """
    for (filename, file_size_in_bytes) in yield_files_sizes(directory_path, on_error=on_error):
        if file_size_in_bytes > threshold_in_bytes:
            yield (filename, file_size_in_bytes)
            
def yield_unusual_permissions(directory_path:str, 
                              permission_reporting_strategy: FilePermissionsReportingStrategy = LooserPermissionsReporting(), 
                              on_error = None)->Generator[tuple[str, Set[FilePermission]], None, None]:
    """Generate the file names with unusual permissions contained in the directory tree pointed by 
    the provided path, along with a human readable name for those permission. This is done one
    by one by walking the tree top-down.

    Note that:
    - Symbolic links are ignored.
    - Directories names and sizes are not returned (only those of files).
    - For files at the same depth level of the tree, no assumptions are made 
        regarding the order by which filenames are returned.
    - if no on_error is provided, exceptions during walk are silently ignored.

    Args:
        directory_path (str): the path where the directory root of the tree resides.
        permission_reporting_strategy (FilePermissionsReportingStrategy, optional): the strategy by
            which to identify unusual permissions. 
            Defaults to LooserPermissionsReporting().
        on_error (_type_, optional): the handler for any errors happening during the walk.
            Defaults to None.
    Yields:
        Generator[tuple[str, Set[FilePermission]], None, None]: the generator of (file_name, 
        file size) tuples.
    """
    for root, _, filenames in os.walk(directory_path, onerror=on_error):
        for filename in filenames:
            try:
                filepath = os.path.join(root, filename)
                stat = os.stat(filepath)
                unusual_permissions = permission_reporting_strategy.report_unusual_permissions(stat)
            except OSError as e:
                if on_error is not None:
                    on_error(e)
                continue
            if len(unusual_permissions) > 0:
                yield (filepath, unusual_permissions)
        
def yield_categories_sizes(directory_path:str, 
                           file_categorization_strategy: FileCategorizationStrategy = FileCategorizerByExtension(), 
                           on_error = None)->Generator[tuple[FileCategory, int], None, None]:
    """Generate the file categories and corresponding sizes contained in the 
    directory tree pointed by the path provided, one by one, by walking the tree
    top-down.
    
    Note that:
    - Symbolic links are ignored.
    - Directories names and sizes are not returned (only those of files).
    - For files at the same depth level of the tree, no assumptions are made 
        regarding the order by which filenames are returned.
    - if no on_error is provided, exceptions during walk are silently ignored.

    Args:
        directory_path (str): the path where the directory root of the tree resides.
        file_categorization_strategy (FileCategorizationStrategy, optional): the strategy by
            which to classify files. 
            Defaults to FileCategorizerByExtension.       
        on_error (_type_, optional): the handler for any errors happening during the walk.
            Defaults to None.
    Returns:
        Generator[tuple[FileCategory, int], None, None]: the generator of (file category, 
        file size) tuples.

    """
    sizes_by_categories = {}
    for root, _, filenames in os.walk(directory_path, onerror = on_error):
        for filename in filenames:
            try:
                filepath = os.path.join(root, filename)
                filesize = os.stat(filepath).st_size
                filecategory =  file_categorization_strategy.categorize_file(filepath)
                if filecategory in sizes_by_categories:
                    sizes_by_categories[filecategory]+=filesize
                else:
                    sizes_by_categories[filecategory]=filesize
            except OSError as e:
                if on_error is not None:
                    on_error(e)
    return  ((category, sizes) for category, sizes in sizes_by_categories.items())