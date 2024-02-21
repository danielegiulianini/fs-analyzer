import os
from unittest.mock import MagicMock
from pytest import fail

from fs_analyzer.tests.utils import DirectoryTreeScenario
from fs_analyzer.view.cli_view import *
from fs_analyzer.view_model.directory_analizer_factory import ExtensionDirectoryAnalizerFactory


TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testdir'))
directory_tree = DirectoryTreeScenario(TEST_PATH)

# could use the ad-hoc fixture https://docs.pytest.org/en/6.2.x/tmpdir.html 
# to raise the abstraction level and avoid boilerplate
def setup_module():
    directory_tree.create_directory_tree()
    
def teardown_module():
    directory_tree.remove_directory_tree()


def test_handle_provided_directory_not_found_gracefully():
    mock = MagicMock()
    directory_analizer = ExtensionDirectoryAnalizerFactory().create(directory_path = directory_tree.test_path() + "jsj", 
                                                                    directory_observer = mock) 
    try:  
        directory_analizer.categorize_files()
    except Exception as excinfo:  
        fail(f"Unexpected exception raised: {excinfo}") 

    mock.on_file_not_found.assert_called_once_with()


def test_handle_provided_directory_not_readable_gracefully():
    directory_analizer = ExtensionDirectoryAnalizerFactory().create(directory_path = directory_tree.test_path(), 
                                                                    directory_observer = MagicMock())
    
    #remove permission to open a directory
    no_read_permission_mode = 0o444
    os.chmod(directory_tree.test_path(), no_read_permission_mode)
    
    try:  
        directory_analizer.categorize_files()
    except Exception as excinfo:
        fail(f"Unexpected exception raised: {excinfo}")
    finally:
        # restore permissions for regular cleanup
        all_permission_mode = 0o777
        os.chmod(directory_tree.test_path(), all_permission_mode)



    
    
    


    

