from fs_analyzer.tests.utils import create_file


import os
import shutil
import time


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