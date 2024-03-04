import os
import shutil
import time
from typing import Callable
from pytest import fail

from fs_analyzer.model.file_category import UNKNOWN_FILE_CATEGORY, FileCategory
from fs_analyzer.model.file_permission_reporting_strategy import LooserPermissionsReporting


def get_size(filepath):
    return os.stat(filepath).st_size


def get_category(filepath):
    category = UNKNOWN_FILE_CATEGORY
    _, extension = os.path.splitext(filepath)
    match extension:
        case '.txt':
            category = FileCategory("text/plain")
        case '.py':
            category = FileCategory("text/x-python")
    return category


def get_unusual_permissions(filepath):
    permission_strategy = LooserPermissionsReporting()
    return permission_strategy.report_unusual_permissions(os.stat(filepath))


def create_file(path, contents='1234'):
    with open(path, 'w') as f:
        f.write(contents)
    return path


class DirectoryTreeScenario:

    def __init__(self, root_path):
        self._files_paths = []
        self._root_path = root_path

    def setup(self):
        
        print("setting up directory tree...")
        join = os.path.join

        os.mkdir(self._root_path)
        os.mkdir(join(self._root_path, 'subdir'))
        
        self._files_paths.append(create_file(join(self._root_path, 'file1.txt')))
        self._files_paths.append(create_file(join(self._root_path, 'file2.txt'), contents='12345678'))

        os.mkdir(join(self._root_path, 'subdir', 'unidir\u018F'))
        self._files_paths.append(create_file(join(self._root_path, 'subdir', 'file1.txt'), contents="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb"))
        self._files_paths.append(create_file(join(self._root_path, 'subdir', 'unicod\u018F.py')))

        self._files_paths.append(create_file(join(self._root_path, 'subdir', 'unidir\u018F', 'file1.txt')))

        os.mkdir(join(self._root_path, 'emptydir'))
        
    def remove(self):
        print("setting down directory tree.")
        try:
            shutil.rmtree(self._root_path)
        except OSError:
            time.sleep(0.1)
            shutil.rmtree(self._root_path)
            
    def root_path(self):
        return self._root_path
    
    def files_paths(self):
        return self._files_paths
    
    
def assert_no_exception_raised(fun: Callable[[], None]):
    try:  
        fun()
    except Exception as excinfo:  
        fail(f"Unexpected exception raised: {excinfo}")


def assert_no_exception_raised_with_arg[T](fun:Callable[[T], None], arg: T):
    try:
        fun(arg)
    except Exception as excinfo:  
        fail(f"Unexpected exception raised: {excinfo}")
