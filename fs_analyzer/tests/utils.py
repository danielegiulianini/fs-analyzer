import os
import shutil
import time

from fs_analyzer.model.file_category import UNKNOWN_FILE_CATEGORY, FileCategory
from fs_analyzer.model.file_permission_reporting_strategy import LooserPermissionsReporting


def get_size(filepath):
    return os.stat(filepath).st_size


def group_by_dict_keys_and_sum(data):
    grouped_data = {}

    for key, value in data.items():
        if key in grouped_data:
            grouped_data[key] += value
        else:
            grouped_data[key] = value

    return grouped_data


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

    def __init__(self, test_path):
        self._files_paths = []
        self._test_path = test_path

    #called once for all the functions in the module
    def create_directory_tree(self):
        
        print("setting up directory tree")
        join = os.path.join

        os.mkdir(self._test_path)
        os.mkdir(join(self._test_path, 'subdir'))
        
        self._files_paths.append(create_file(join(self._test_path, 'file1.txt')))
        self._files_paths.append(create_file(join(self._test_path, 'file2.txt'), contents='12345678'))

        os.mkdir(join(self._test_path, 'subdir', 'unidir\u018F'))
        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'file1.txt'), contents="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb"))
        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'unicod\u018F.py')))

        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'unidir\u018F', 'file1.txt')))

        os.mkdir(join(self._test_path, 'emptydir'))
        

    #called once for all the functions in the module
    def remove_directory_tree(self):
        print("setting down directory tree.")
        try:
            shutil.rmtree(self._test_path)
        except OSError:
            time.sleep(0.1)
            shutil.rmtree(self._test_path)
            
    def test_path(self):
        return self._test_path
    
    def files_paths(self):
        return self._files_paths



class EmptyDirectoryTreeScenario:

    def __init__(self, test_path):
        self._files_paths = []
        self._test_path = test_path

    #called once for all the functions in the module
    def create_directory_tree(self):
        
        print("setting up directory tree")
        join = os.path.join

        os.mkdir(self._test_path)
        os.mkdir(join(self._test_path, 'subdir'))
        
        self._files_paths.append(create_file(join(self._test_path, 'file1.txt')))
        self._files_paths.append(create_file(join(self._test_path, 'file2.txt'), contents='12345678'))

        os.mkdir(join(self._test_path, 'subdir', 'unidir\u018F'))
        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'file1.txt'), contents="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb"))
        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'unicod\u018F.py')))

        self._files_paths.append(create_file(join(self._test_path, 'subdir', 'unidir\u018F', 'file1.txt')))

        os.mkdir(join(self._test_path, 'linkdir'))
        

    #called once for all the functions in the module
    def remove_directory_tree(self):
        print("setting down directory tree.")
        try:
            shutil.rmtree(self._test_path)
        except OSError:
            time.sleep(0.1)
            shutil.rmtree(self._test_path)
            
    def test_path(self):
        return self._test_path
    
    def files_paths(self):
        return self._files_paths
