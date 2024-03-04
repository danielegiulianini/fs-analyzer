import os
import pytest

from fs_analyzer.model.file_categorization_strategy import FileCategorizerByExtension
from fs_analyzer.model.file_category import *
from fs_analyzer.model.file_listing_generators import *
from fs_analyzer.tests.fixtures import DirectoryTreeScenario
from fs_analyzer.tests.utils import get_category, get_size, get_unusual_permissions

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testdir'))
directory_tree = DirectoryTreeScenario(TEST_PATH)


# could use the ad-hoc fixture https://docs.pytest.org/en/6.2.x/tmpdir.html 
# to raise the abstraction level and avoid boilerplate
def setup_module():
    directory_tree.setup()

    
def teardown_module():
    directory_tree.remove()


# check normal scenario
def test_categorized_files_report_returns_all_categorized_files():
    files_categories = {fp: get_category(fp) for fp in directory_tree.files_paths()}
    generated_files_categories = list(yield_file_categories(directory_path=directory_tree.root_path(),
                                                            file_categorization_strategy=FileCategorizerByExtension()))
    assert len(generated_files_categories) == len(files_categories)
    generated_files_categories = dict(generated_files_categories)
    assert generated_files_categories == files_categories


def test_size_report_returns_all_files_sizes():
    files_sizes = {fp: get_size(fp) for fp in directory_tree.files_paths()}
    generated_files_sizes = list(yield_files_sizes(directory_tree.root_path()))
    assert len(generated_files_sizes) == len(files_sizes)
    generated_files_sizes = dict(generated_files_sizes)
    assert generated_files_sizes == files_sizes
    

def test_permissions_report_returns_all_unusual_permissions():
    # Define the permission mode to make the file non-world-writable
    permission_mode = 0o644
    
    # set the first file to be NOT world writable (so, to not be reported)
    os.chmod(directory_tree.files_paths()[0], permission_mode)
    
    files_permissions = {fp: get_unusual_permissions(fp) for fp in directory_tree.files_paths()}    
    generated_files_permissions = list(yield_unusual_permissions(directory_path=directory_tree.root_path(), 
                                                                 permission_reporting_strategy=LooserPermissionsReporting()))
    
    assert len(generated_files_permissions) == len(files_permissions)
  
  
def test_large_files_report_returns_all_large_files():
    size_threshold_in_bytes = 10
    files_sizes = {fp: get_size(fp) for fp in directory_tree.files_paths() if get_size(fp) > size_threshold_in_bytes}
    generated_files_sizes = list(yield_files_larger_than(directory_tree.root_path(), size_threshold_in_bytes))
    assert len(generated_files_sizes) == len(files_sizes)
    generated_files_sizes = dict(generated_files_sizes)
    assert generated_files_sizes == files_sizes


def test_category_sizes_report_returns_all_categories_sizes():
    generated_categories_sizes = list(yield_categories_sizes(TEST_PATH, FileCategorizerByExtension()))

    categorized_files = {fp: get_category(fp) for fp in directory_tree.files_paths()}
    categoriessizes = {cat: 0 for (_, cat) in categorized_files.items()}
    for (fp, cat) in categorized_files.items():
        categoriessizes[cat] += get_size(fp)

    assert categoriessizes == dict(generated_categories_sizes)
    

# check empty directory scenario
empty_dir = os.path.join(TEST_PATH, 'emptydir')


def test_no_files_sizes_if_empty_directory():
    with pytest.raises(StopIteration):
        next(yield_files_sizes(empty_dir))


def test_no_categorized_file_if_empty_directory():
    with pytest.raises(StopIteration):
        next(yield_files_larger_than(empty_dir, 2))


def test_no_unusual_permissions_if_empty_directory():
    with pytest.raises(StopIteration):
        next(yield_unusual_permissions(empty_dir))


def test_no_categories_if_empty_directory():
    with pytest.raises(StopIteration):
        next(yield_categories_sizes(empty_dir))
