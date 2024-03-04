import os
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
