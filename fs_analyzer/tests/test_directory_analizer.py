import os
from unittest.mock import Mock, patch
from pytest import fail

from fs_analyzer.model.file_categorization_strategy import FileCategorizationStrategy
from fs_analyzer.model.file_permission_reporting_strategy import FilePermissionsReportingStrategy
from fs_analyzer.tests.utils import DirectoryTreeScenario, \
    assert_no_exception_raised, assert_no_exception_raised_with_arg
from fs_analyzer.view.cli_view import *
from fs_analyzer.view_model.directory_analizer import DirectoryAnalizer
from fs_analyzer.view_model.directory_observer import DirectoryObserver


# test fixtures
TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testdir'))
directory_tree = DirectoryTreeScenario(TEST_PATH)


# could use the ad-hoc fixture https://docs.pytest.org/en/6.2.x/tmpdir.html
# to raise the abstraction level and avoid boilerplate
def setup_module():
    directory_tree.setup()


def teardown_module():
    directory_tree.remove()


def test_analyzer_gracefully_handle_not_found_provided_directory():
    mock = Mock()
    not_existing_directory_analizer = directory_analizer(directory_path=directory_tree.root_path() + "jsj",
                                                         directory_observer=mock)
    assert_no_exception_raised(not_existing_directory_analizer.categorize_files)
    mock.on_invalid_input.assert_called_once_with("The provided path does not point to a directory.")


def test_analyzer_gracefully_handle_not_readable_provided_directory():
    # remove permission to open a directory
    no_read_permission_mode = 0o444
    os.chmod(directory_tree.root_path(), no_read_permission_mode)

    try:
        directory_analizer(directory_tree.root_path()).categorize_files()
    except Exception as excinfo:
        fail(f"Unexpected exception raised: {excinfo}")
    finally:
        # restore permissions for regular cleanup
        all_permission_mode = 0o777
        os.chmod(directory_tree.root_path(), all_permission_mode)


def test_reporting_permissions_gracefully_handle_file_not_found():
    mock = Mock()
    mock.report_unusual_permissions.side_effect = FileNotFoundError('mocked error')
    assert_no_exception_raised(directory_analizer(permission_reporting_strategy=mock).report_permissions)


def test_categorizing_gracefully_handle_file_not_found():
    mock = Mock()
    mock.categorize_file.side_effect = FileNotFoundError('mocked error')
    assert_no_exception_raised(directory_analizer(file_categorization_strategy=mock).categorize_files)


@patch('os.stat')
def test_large_files_gracefully_handle_file_not_found(test_patch):
    test_patch.side_effect = FileNotFoundError('mocked error')
    assert_no_exception_raised_with_arg(directory_analizer().identify_large_files, 10)


def test_cat_sizes_gracefully_handle_file_not_found():
    mock = Mock()
    mock.categorize_file.side_effect = FileNotFoundError('mocked error')
    assert_no_exception_raised(directory_analizer(file_categorization_strategy=mock).analize_category_sizes)


def directory_analizer(directory_path: str = directory_tree.root_path(),
                       file_categorization_strategy: FileCategorizationStrategy = Mock(),
                       permission_reporting_strategy: FilePermissionsReportingStrategy = Mock(),
                       directory_observer: DirectoryObserver = Mock()) -> DirectoryAnalizer:

    return DirectoryAnalizer(directory_path,
                             file_categorization_strategy,
                             permission_reporting_strategy,
                             directory_observer)
